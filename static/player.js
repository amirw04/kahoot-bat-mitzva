let playerId = localStorage.getItem("kahootPlayerId");
if (!playerId) {
  playerId = crypto.randomUUID();
  localStorage.setItem("kahootPlayerId", playerId);
}

let joined = false;
let playerName = localStorage.getItem("kahootPlayerName") || "";
let currentQuestionNumber = null;
let selectedAnswer = null;

const el = {
  joinPanel: document.getElementById("join-panel"),
  gamePanel: document.getElementById("game-panel"),
  playerName: document.getElementById("player-name"),
  gameCode: document.getElementById("game-code"),
  joinButton: document.getElementById("join-button"),
  joinMessage: document.getElementById("join-message"),
  playerTitle: document.getElementById("player-title"),
  playerStatus: document.getElementById("player-status"),
  playerTimer: document.getElementById("player-timer"),
  questionText: document.getElementById("question-text"),
  questionImage: document.getElementById("question-image"),
  answersList: document.getElementById("answers-list"),
  answerMessage: document.getElementById("answer-message"),
  scoreMessage: document.getElementById("score-message"),
};

el.playerName.value = playerName;
el.joinButton.onclick = joinGame;
el.gameCode.addEventListener("input", () => {
  el.gameCode.value = el.gameCode.value.toUpperCase();
});

async function joinGame() {
  playerName = el.playerName.value.trim();
  const code = el.gameCode.value.trim().toUpperCase();
  if (!playerName || !code) {
    el.joinMessage.textContent = "צריך למלא שם וקוד משחק.";
    return;
  }

  const response = await fetch("/api/player/join", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ playerId, name: playerName, code }),
  });
  const data = await response.json();

  if (!data.ok) {
    joined = false;
    el.joinMessage.textContent = data.message;
    return;
  }

  joined = true;
  localStorage.setItem("kahootPlayerName", playerName);
  el.joinPanel.classList.add("hidden");
  el.gamePanel.classList.remove("hidden");
  render(data.state);
}

async function loadState() {
  if (!joined) {
    return;
  }
  const response = await fetch("/api/state");
  render(await response.json());
}

function render(state) {
  const me = state.players.find((player) => player.id === playerId);
  if (!me) {
    joined = false;
    el.joinPanel.classList.remove("hidden");
    el.gamePanel.classList.add("hidden");
    return;
  }

  if (state.question && state.question.number !== currentQuestionNumber) {
    selectedAnswer = null;
    el.answerMessage.textContent = "";
  }
  currentQuestionNumber = state.question ? state.question.number : currentQuestionNumber;

  el.playerTimer.textContent = state.remainingSeconds ?? "--";
  el.scoreMessage.textContent = `הניקוד שלך: ${me.score}`;
  renderQuestion(state, me);
}

function renderQuestion(state, me) {
  const question = state.question;
  el.answersList.innerHTML = "";

  if (!question) {
    el.playerTitle.textContent = state.phase === "finished" ? "המשחק הסתיים" : "ממתינים למנחה";
    el.playerStatus.textContent = state.phase === "finished" ? "כל הכבוד!" : "עוד רגע מתחילים.";
    el.questionText.textContent = "";
    el.questionImage.classList.add("hidden");
    return;
  }

  el.playerTitle.textContent = `שאלה ${question.number}`;
  el.playerStatus.textContent = statusText(state, me);
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
    button.disabled = !isVisible || state.phase !== "timer" || me.answered || Boolean(selectedAnswer);

    if (!isVisible) {
      button.classList.add("hidden-answer");
    }
    if (me.answer === answer || selectedAnswer === answer) {
      button.classList.add("picked");
    }
    if (state.correctAnswer === answer) {
      button.classList.add("correct");
    }
    if ((me.answer === answer || selectedAnswer === answer) && state.correctAnswer && state.correctAnswer !== answer) {
      button.classList.add("wrong-picked");
    }

    button.onclick = () => chooseAnswer(answer, state);
    el.answersList.appendChild(button);
  });
}

async function chooseAnswer(answer, state) {
  selectedAnswer = answer;
  el.answerMessage.textContent = "התשובה נקלטה.";
  await fetch("/api/player/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ playerId, answer }),
  });
  renderQuestion(state, { answered: true, score: 0 });
}

function statusText(state, me) {
  if (state.phase === "review") {
    return `התשובה הנכונה: ${state.correctAnswer}`;
  }
  if (me.answered || selectedAnswer) {
    return "התשובה נקלטה.";
  }
  if (state.phase === "timer") {
    return "אפשר לענות עכשיו.";
  }
  if (state.phase === "timer_done") {
    return "הזמן נגמר.";
  }
  return "ממתינים שהמנחה יתחיל את הטיימר.";
}

setInterval(loadState, 500);
