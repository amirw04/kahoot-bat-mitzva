const el = {
  gameCode: document.getElementById("game-code"),
  phaseLabel: document.getElementById("phase-label"),
  timerLabel: document.getElementById("timer-label"),
  questionCount: document.getElementById("question-count"),
  questionText: document.getElementById("question-text"),
  questionImage: document.getElementById("question-image"),
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

document.addEventListener("keydown", (event) => {
  if (event.code === "Space" && event.target === document.body) {
    event.preventDefault();
    postAction("/api/host/advance");
  }
});

async function postAction(url) {
  const response = await fetch(url, { method: "POST" });
  render(await response.json());
}

async function loadState() {
  const response = await fetch("/api/state");
  render(await response.json());
}

function render(state) {
  el.gameCode.textContent = state.code;
  el.phaseLabel.textContent = phaseText[state.phase] || state.phase;
  el.timerLabel.textContent = state.remainingSeconds ?? "--";
  el.questionCount.textContent = `שאלה ${Math.min(state.questionIndex + 1, state.totalQuestions)} מתוך ${state.totalQuestions}`;

  renderQuestion(state);
  renderPlayers(state.players);
  updateButtons(state);
}

function renderQuestion(state) {
  const question = state.question;
  el.answersList.innerHTML = "";

  if (!question) {
    el.questionText.textContent =
      state.phase === "finished" ? "המשחק הסתיים." : "לחץ \"הצג שאלה\" כדי להתחיל.";
    el.questionImage.classList.add("hidden");
    return;
  }

  el.questionText.textContent = question.text;
  if (question.image) {
    el.questionImage.src = `/images/${question.image}`;
    el.questionImage.classList.remove("hidden");
  } else {
    el.questionImage.classList.add("hidden");
  }

  question.answers.forEach((answer, index) => {
    const button = document.createElement("button");
    const isVisible = index < state.revealedAnswers;
    button.className = `answer-card answer-${index}`;
    button.textContent = isVisible ? answer : `תשובה ${index + 1}`;
    button.disabled = true;
    if (!isVisible) {
      button.classList.add("hidden-answer");
    }
    if (state.correctAnswer === answer) {
      button.classList.add("correct");
    }
    el.answersList.appendChild(button);
  });
}

function renderPlayers(players) {
  if (!players.length) {
    el.playersTable.innerHTML = "<tr><td colspan=\"3\">אין משתתפים עדיין</td></tr>";
    return;
  }

  el.playersTable.innerHTML = players
    .slice()
    .sort((a, b) => b.score - a.score)
    .map((player) => `
      <tr>
        <td>${escapeHtml(player.name)}</td>
        <td>${player.score}</td>
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

loadState();
setInterval(loadState, 500);
