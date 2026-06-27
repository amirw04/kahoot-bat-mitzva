const el = {
  gameCode: document.getElementById("game-code"),
  phaseLabel: document.getElementById("phase-label"),
  quizSelect: document.getElementById("quiz-select"),
  timerLabel: document.getElementById("timer-label"),
  questionCount: document.getElementById("question-count"),
  questionText: document.getElementById("question-text"),
  questionImages: document.getElementById("question-images"),
  answersList: document.getElementById("answers-list"),
  playersTable: document.getElementById("players-table"),
  advance: document.getElementById("advance-button"),
  newGame: document.getElementById("new-game-button"),
  showQuestion: document.getElementById("show-question-button"),
  revealAnswer: document.getElementById("reveal-answer-button"),
  startTimer: document.getElementById("start-timer-button"),
  showCorrect: document.getElementById("show-correct-button"),
  nextQuestion: document.getElementById("next-question-button"),
};

const phaseText = {
  lobby: "ממתינים",
  question: "מציגים שאלה",
  timer: "טיימר",
  timer_done: "הזמן נגמר",
  review: "תשובה וניקוד",
  finished: "המשחק הסתיים",
};

el.newGame.onclick = () => postAction("/api/host/new-game");
el.showQuestion.onclick = () => postAction("/api/host/show-question");
el.revealAnswer.onclick = () => postAction("/api/host/reveal-answer");
el.startTimer.onclick = () => postAction("/api/host/start-timer");
el.showCorrect.onclick = () => postAction("/api/host/show-correct");
el.nextQuestion.onclick = () => postAction("/api/host/next-question");
el.advance.onclick = () => postAction("/api/host/advance");
el.quizSelect.onchange = () => postAction("/api/host/select-quiz", { quizKey: el.quizSelect.value });

document.addEventListener("keydown", (event) => {
  if (event.code === "Space" && event.target === document.body) {
    event.preventDefault();
    postAction("/api/host/advance");
  }
});

async function postAction(url, body = null) {
  const options = { method: "POST" };
  if (body) {
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  render(await response.json());
}

async function loadState() {
  const response = await fetch("/api/state");
  render(await response.json());
}

function render(state) {
  el.gameCode.textContent = state.code;
  renderQuizSelect(state);
  el.phaseLabel.textContent = phaseText[state.phase] || state.phase;
  el.timerLabel.textContent = state.remainingSeconds ?? "--";
  el.questionCount.textContent = `שאלה ${Math.min(state.questionIndex + 1, state.totalQuestions)} מתוך ${state.totalQuestions}`;

  renderQuestion(state);
  renderPlayers(state.players);
  updateButtons(state);
}

function renderQuizSelect(state) {
  const quizzes = Array.isArray(state.quizzes) ? state.quizzes : [];
  const currentKeys = Array.from(el.quizSelect.options).map((option) => option.value);
  const nextKeys = quizzes.map((quiz) => quiz.key);
  if (currentKeys.join("|") !== nextKeys.join("|")) {
    el.quizSelect.innerHTML = "";
    quizzes.forEach((quiz) => {
      const option = document.createElement("option");
      option.value = quiz.key;
      option.textContent = `${quiz.name} (${quiz.total})`;
      el.quizSelect.appendChild(option);
    });
  }
  el.quizSelect.value = state.quizKey || "";
  el.quizSelect.disabled = Boolean(state.question);
}

function renderQuestion(state) {
  const question = state.question;
  el.answersList.innerHTML = "";

  if (!question) {
    el.questionText.textContent =
      state.phase === "finished" ? "המשחק הסתיים." : "לחץ \"הצג שאלה\" כדי להתחיל.";
    renderQuestionImages(null);
    return;
  }

  el.questionText.textContent = question.text;
  renderQuestionImages(question);

  const correctAnswers = Array.isArray(state.correctAnswers) ? state.correctAnswers : [];

  question.answers.forEach((answer, index) => {
    const button = document.createElement("button");
    const isVisible = index < state.revealedAnswers;
    button.className = `answer-card answer-${index % 6}`;
    button.disabled = true;
    if (!isVisible) {
      button.textContent = `תשובה ${index + 1}`;
      button.classList.add("hidden-answer");
    } else {
      fillAnswerButton(button, question, answer);
    }
    if (correctAnswers.includes(answer)) {
      button.classList.add("correct");
    }
    el.answersList.appendChild(button);
  });
}

function renderQuestionImages(question) {
  el.questionImages.innerHTML = "";
  const images = question
    ? [...(question.questionImages || []), ...(question.image ? [question.image] : [])]
    : [];
  if (!images.length) {
    el.questionImages.classList.add("hidden");
    return;
  }
  images.forEach((imageName) => {
    const image = document.createElement("img");
    image.src = `/images/${imageName}`;
    image.alt = "תמונת שאלה";
    image.className = "question-image";
    el.questionImages.appendChild(image);
  });
  el.questionImages.classList.remove("hidden");
}

function fillAnswerButton(button, question, answer) {
  button.textContent = "";
  const imageName = question.answerImages ? question.answerImages[answer] : null;
  if (imageName) {
    const image = document.createElement("img");
    image.src = `/images/${imageName}`;
    image.alt = answer;
    image.className = "answer-image";
    button.appendChild(image);
  }
  const label = document.createElement("span");
  label.textContent = answer;
  button.appendChild(label);
}

function renderPlayers(players) {
  if (!players.length) {
    el.playersTable.innerHTML = "<tr><td colspan=\"4\">אין משתתפים עדיין</td></tr>";
    return;
  }

  el.playersTable.innerHTML = players
    .slice()
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name, "he"))
    .map((player, index) => `
      <tr>
        <td>${index + 1}</td>
        <td>${escapeHtml(player.name)}</td>
        <td>${formatScore(player.score)}</td>
        <td>${player.answered ? "כן" : "לא"}</td>
      </tr>
    `)
    .join("");
}

function updateButtons(state) {
  const hasQuestion = Boolean(state.question);
  const allAnswersVisible = hasQuestion && state.revealedAnswers >= state.question.answers.length;

  el.showQuestion.disabled = hasQuestion || state.phase === "finished";
  el.revealAnswer.disabled = !hasQuestion || allAnswersVisible || state.phase === "timer" || state.phase === "review";
  el.startTimer.disabled = !hasQuestion || !allAnswersVisible || state.phase === "timer" || state.phase === "review";
  el.showCorrect.disabled = !hasQuestion || state.phase === "review" || state.phase === "finished";
  el.nextQuestion.disabled = state.phase !== "review";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#039;");
}

function formatScore(score) {
  return Number.isInteger(score) ? String(score) : String(score).replace(/\.0$/, "");
}

loadState();
setInterval(loadState, 500);
