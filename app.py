import random
import importlib.util
import socket
import time
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__)
DATAQ_PATTERN = "DataQ_*.py"
"""
DEFAULT_ANSWER_COLORS = [
    [0.835, 0.247, 0.247],  # red
    [0.137, 0.455, 0.671],  # blue
    [0.851, 0.604, 0.118],  # gold
    [0.180, 0.616, 0.345],  # green
    [0.486, 0.227, 0.929],  # purple
    [0.059, 0.463, 0.431],  # teal
]
"""
DEFAULT_ANSWER_COLORS = [
    [0.8, 0.1, 0.0], # red  
    [0.0, 0.1, 0.8], # blue   
    [1.0, 1.0, 0.0], # yellow 
    [0.0, 0.7, 0.0], # green
    [0.0, 0.4, 0.4], # teal
    [0.9, 0.0, 0.9], # purple
    [0.85, 0.85, 0.85], # gray
    [0.0, 0.0, 0.0], # black
]


def load_questionnaires():
    loaded_questionnaires = {}
    base_path = Path(__file__).resolve().parent

    for dataq_path in sorted(base_path.glob(DATAQ_PATTERN)):
        module_name = dataq_path.stem
        spec = importlib.util.spec_from_file_location(module_name, dataq_path)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module_questionnaires = getattr(module, "questionnaires", None)
        if not module_questionnaires:
            continue

        for key, quiz in module_questionnaires.items():
            unique_key = key
            if unique_key in loaded_questionnaires:
                unique_key = f"{module_name}_{key}"
            loaded_questionnaires[unique_key] = quiz

    if not loaded_questionnaires:
        raise RuntimeError(f"No questionnaires were found in {DATAQ_PATTERN}")

    return loaded_questionnaires


questionnaires = load_questionnaires()
DEFAULT_QUIZ_KEY = next(iter(questionnaires))


def make_game_code():
    return "".join(random.choice("123456789") for _ in range(2))


def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
        sock.close()
        return ip_address
    except OSError:
        return "localhost"


def as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def correct_answers_for(question):
    return [answer.Text for answer in question.Answers if answer.IsCrct]


def quiz_options():
    return [
        {"key": key, "name": quiz.name, "total": len(quiz.questions)}
        for key, quiz in questionnaires.items()
    ]


def questions_for(quiz_key):
    return questionnaires[quiz_key].questions


def current_questions():
    return questions_for(game["quiz_key"])


def arrange_answers(answers):
    random.shuffle(answers)
    if not any(answer.MandatoryPosition is not None for answer in answers):
        return answers

    arranged = [None] * len(answers)
    answer_pool = list(answers)

    positioned_answers = sorted(
        (answer for answer in answers if answer.MandatoryPosition is not None),
        key=lambda answer: answer.MandatoryPosition,
    )
    for answer in positioned_answers:
        index = int(answer.MandatoryPosition) - 1
        if index < 0 or index >= len(arranged) or arranged[index] is not None:
            continue
        arranged[index] = answer
        answer_pool.remove(answer)

    for index, existing_answer in enumerate(arranged):
        if existing_answer is None and answer_pool:
            arranged[index] = answer_pool.pop(0)

    return arranged


def make_question_payload(question, number):
    correct_answers = correct_answers_for(question)
    answers = arrange_answers(list(question.Answers))
    answer_colors = {}
    for index, answer in enumerate(answers):
        answer_colors[answer.Text] = (
            answer.Color
            if answer.Color is not None
            else DEFAULT_ANSWER_COLORS[index % len(DEFAULT_ANSWER_COLORS)]
        )

    return {
        "number": number,
        "text": question.Qstn,
        "answers": [answer.Text for answer in answers],
        "answerImages": {
            answer.Text: answer.Image for answer in answers if answer.Image is not None
        },
        "answerColors": answer_colors,
        "allowMultiple": len(correct_answers) > 1,
        "image": question.Image,
        "questionImages": question.QuestionImages,
        "correctImages": question.CorrectImages,
        "timer": question.Timer,
    }


def new_game(quiz_key=None):
    selected_quiz_key = quiz_key if quiz_key in questionnaires else DEFAULT_QUIZ_KEY
    return {
        "quiz_key": selected_quiz_key,
        "code": make_game_code(),
        "players": {},
        "question_index": 0,
        "question": None,
        "revealed_answers": 0,
        "phase": "lobby",
        "correct_answers": [],
        "timer_end": None,
        "scored": False,
    }


game = new_game()


def remaining_seconds():
    if game["timer_end"] is None:
        return None
    return max(0, int(game["timer_end"] - time.time()))


def refresh_timer():
    if game["phase"] == "timer" and remaining_seconds() == 0:
        game["phase"] = "timer_done"
        game["timer_end"] = None


def public_state():
    refresh_timer()
    quiz_key = game["quiz_key"]
    quiz = questionnaires[quiz_key]
    return {
        "code": game["code"],
        "quizKey": quiz_key,
        "quizName": quiz.name,
        "quizzes": quiz_options(),
        "phase": game["phase"],
        "questionIndex": game["question_index"],
        "totalQuestions": len(quiz.questions),
        "question": game["question"],
        "revealedAnswers": game["revealed_answers"],
        "correctAnswer": game["correct_answers"][0] if len(game["correct_answers"]) == 1 else None,
        "correctAnswers": game["correct_answers"],
        "remainingSeconds": remaining_seconds(),
        "players": [
            {
                "id": player_id,
                "name": player["name"],
                "score": player["score"],
                "answered": player["answer"] is not None,
                "answer": player["answer"],
            }
            for player_id, player in game["players"].items()
        ],
    }


def reset_player_answers():
    for player in game["players"].values():
        player["answer"] = None


def show_question():
    questions = current_questions()
    if game["question_index"] >= len(questions):
        game["phase"] = "finished"
        game["question"] = None
        return

    question = questions[game["question_index"]]
    game["question"] = make_question_payload(question, game["question_index"] + 1)
    game["revealed_answers"] = 0
    game["phase"] = "question"
    game["correct_answers"] = []
    game["timer_end"] = None
    game["scored"] = False
    reset_player_answers()


def show_correct_answer():
    if not game["question"]:
        return

    question = current_questions()[game["question_index"]]
    game["phase"] = "review"
    game["timer_end"] = None
    game["correct_answers"] = correct_answers_for(question)

    if game["scored"]:
        return

    for player in game["players"].values():
        if player["answer"] is None:
            continue

        question_score = score_player_answer(question, player["answer"])
        player["score"] = round(player["score"] + question_score, 2)
    game["scored"] = True


def score_player_answer(question, player_answer):
    selected = set(as_list(player_answer))
    correct_set = set(correct_answers_for(question))

    if len(correct_set) <= 1:
        return 1 if selected == correct_set else 0

    answer_keys = [answer.Text for answer in question.Answers]
    if not answer_keys:
        return 0

    correct_decisions = 0
    for answer in answer_keys:
        should_select = answer in correct_set
        did_select = answer in selected
        if should_select == did_select:
            correct_decisions += 1

    return correct_decisions / len(answer_keys)


@app.route("/")
def index():
    return render_template("host.html")


@app.route("/host")
def host():
    return render_template("host.html")


@app.route("/player")
def player():
    return render_template("player.html")




@app.route("/public")
def public():
    return render_template("public.html")
@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory("images", filename)


@app.get("/api/state")
def api_state():
    return jsonify(public_state())


@app.post("/api/host/new-game")
def api_new_game():
    data = request.get_json(silent=True) or {}
    quiz_key = data.get("quizKey") or game["quiz_key"]
    game.clear()
    game.update(new_game(quiz_key))
    return jsonify(public_state())


@app.post("/api/host/select-quiz")
def api_select_quiz():
    data = request.get_json(force=True)
    quiz_key = data.get("quizKey")
    if quiz_key not in questionnaires:
        return jsonify({"ok": False, "message": "שאלון לא מוכר."}), 400
    game.clear()
    game.update(new_game(quiz_key))
    return jsonify(public_state())


@app.post("/api/host/show-question")
def api_show_question():
    show_question()
    return jsonify(public_state())


@app.post("/api/host/reveal-answer")
def api_reveal_answer():
    if game["question"] and game["phase"] not in ("timer", "review", "finished"):
        total_answers = len(game["question"]["answers"])
        game["revealed_answers"] = min(total_answers, game["revealed_answers"] + 1)
    return jsonify(public_state())


@app.post("/api/host/start-timer")
def api_start_timer():
    if game["question"] and game["phase"] not in ("timer", "review", "finished"):
        game["phase"] = "timer"
        game["timer_end"] = time.time() + int(game["question"]["timer"])
    return jsonify(public_state())


@app.post("/api/host/show-correct")
def api_show_correct():
    show_correct_answer()
    return jsonify(public_state())


@app.post("/api/host/next-question")
def api_next_question():
    questions = current_questions()
    game["question_index"] += 1
    game["question"] = None
    game["revealed_answers"] = 0
    game["correct_answers"] = []
    game["timer_end"] = None
    game["scored"] = False
    game["phase"] = "finished" if game["question_index"] >= len(questions) else "lobby"
    return jsonify(public_state())


@app.post("/api/host/advance")
def api_advance():
    refresh_timer()
    if not game["question"]:
        show_question()
    elif game["revealed_answers"] < len(game["question"]["answers"]):
        if game["phase"] not in ("timer", "review", "finished"):
            total_answers = len(game["question"]["answers"])
            game["revealed_answers"] = min(total_answers, game["revealed_answers"] + 1)
    elif game["phase"] not in ("timer", "timer_done", "review"):
        game["phase"] = "timer"
        game["timer_end"] = time.time() + int(game["question"]["timer"])
    elif game["phase"] in ("timer", "timer_done"):
        show_correct_answer()
    else:
        questions = current_questions()
        game["question_index"] += 1
        game["question"] = None
        game["revealed_answers"] = 0
        game["correct_answers"] = []
        game["timer_end"] = None
        game["scored"] = False
        game["phase"] = "finished" if game["question_index"] >= len(questions) else "lobby"
    return jsonify(public_state())


@app.post("/api/player/join")
def api_player_join():
    data = request.get_json(force=True)
    player_id = (data.get("playerId") or "").strip()
    name = (data.get("name") or "").strip()
    code = (data.get("code") or "").strip().upper()

    if not player_id or not name:
        return jsonify({"ok": False, "message": "צריך להכניס שם."}), 400
    if code != game["code"]:
        return jsonify({"ok": False, "message": "קוד המשחק לא נכון."}), 400

    game["players"][player_id] = {
        "name": name,
        "score": game["players"].get(player_id, {}).get("score", 0),
        "answer": None,
    }
    return jsonify({"ok": True, "state": public_state()})


@app.post("/api/player/answer")
def api_player_answer():
    refresh_timer()
    data = request.get_json(force=True)
    player_id = (data.get("playerId") or "").strip()
    answers = data.get("answers")
    if answers is None:
        answers = as_list(data.get("answer"))
    player = game["players"].get(player_id)

    if not player or game["phase"] != "timer" or player["answer"] is not None:
        return jsonify(public_state())

    visible_answers = game["question"]["answers"][: game["revealed_answers"]]
    selected_answers = []
    for answer in as_list(answers):
        if answer in visible_answers and answer not in selected_answers:
            selected_answers.append(answer)

    if selected_answers:
        player["answer"] = selected_answers

    return jsonify(public_state())


if __name__ == "__main__":
    ip = get_local_ip()
    port = int(os.environ.get("PORT", 5000))
    print("Host screen:   http://localhost:5000/host")
    print("Player screen: http://localhost:5000/player")
    print("Public screen: http://localhost:5000/public")
    print(f"Phones on Wi-Fi: http://{ip}:{port}/player")
    app.run(host="0.0.0.0", port=port, debug=False)
