import random
import socket
import string
import time
import os

from flask import Flask, jsonify, render_template, request, send_from_directory

from DataQuestions import questionnaires


app = Flask(__name__)
DEFAULT_QUIZ_KEY = next(iter(questionnaires))


def make_game_code():
    letters = string.ascii_uppercase.replace("I", "").replace("O", "")
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
    return as_list(question.AnsT)


def quiz_options():
    return [
        {"key": key, "name": quiz.name, "total": len(quiz.questions)}
        for key, quiz in questionnaires.items()
    ]


def questions_for(quiz_key):
    return questionnaires[quiz_key].questions


def current_questions():
    return questions_for(game["quiz_key"])


def arrange_answers(answers, mandatory_position):
    random.shuffle(answers)
    if not mandatory_position:
        return answers

    arranged = [None] * len(answers)
    answer_pool = list(answers)

    for answer, position in sorted(mandatory_position.items(), key=lambda item: item[1]):
        if answer not in answer_pool:
            continue
        index = int(position) - 1
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
    answers = list(question.AnsF) + correct_answers
    answers = arrange_answers(answers, question.MandatoryPosition)
    return {
        "number": number,
        "text": question.Qstn,
        "answers": answers,
        "answerImages": question.AnswerImages,
        "allowMultiple": len(correct_answers) > 1,
        "image": question.Image,
        "questionImages": question.QuestionImages,
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

    correct_set = set(game["correct_answers"])
    points_per_correct = 1 / len(correct_set) if correct_set else 0
    for player in game["players"].values():
        selected = set(as_list(player["answer"]))
        player_points = len(selected & correct_set) * points_per_correct
        player["score"] = round(player["score"] + min(1, player_points), 2)
    game["scored"] = True


@app.route("/")
def index():
    return render_template("host.html")


@app.route("/host")
def host():
    return render_template("host.html")


@app.route("/player")
def player():
    return render_template("player.html")


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
    print(f"Phones on Wi-Fi: http://{ip}:{port}/player")
    app.run(host="0.0.0.0", port=port, debug=False)
