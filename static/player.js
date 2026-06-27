let playerId = localStorage.getItem("kahootPlayerId");
if (!playerId) {
  playerId = crypto.randomUUID();
  localStorage.setItem("kahootPlayerId", playerId);
}

let joined = false;
let playerName = localStorage.getItem("kahootPlayerName") || "";
let currentQuestionNumber = null;
let selectedAnswers = [];

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
  questionImages: document.getElementById("question-images"),
  answersList: document.getElementById("answers-list"),
  submitAnswer: document.getElementById("submit-answer"),
  answerMessage: document.getElementById("answer-message"),
  scoreMessage: document.getElementById("score-message"),
};

el.playerName.value = playerName;
el.joinButton.onclick = joinGame;
el.submitAnswer.onclick = submitAnswer;
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
    selectedAnswers = [];
    el.answerMessage.textContent = "";
  }
  currentQuestionNumber = state.question ? state.question.number : currentQuestionNumber;

  el.playerTimer.textContent = state.remainingSeconds ?? "--";
  el.scoreMessage.textContent = `הניקוד שלך: ${formatScore(me.score)}`;
  renderQuestion(state, me);
}

function renderQuestion(state, me) {
  const question = state.question;
  el.answersList.innerHTML = "";

  if (!question) {
    el.playerTitle.textContent = state.phase === "finished" ? "המשחק הסתיים" : "ממתינים למנחה";
    el.playerStatus.textContent = state.phase === "finished" ? "כל הכבוד!" : "עוד רגע מתחילים.";
    el.questionText.textContent = "";
    renderQuestionImages(null);
    el.submitAnswer.classList.add("hidden");
    return;
  }

  el.playerTitle.textContent = `שאלה ${question.number}`;
  el.playerStatus.textContent = statusText(state, me);
  el.questionText.textContent = question.text;
  renderQuestionImages(question);

  const savedAnswers = normalizeAnswers(me.answer);
  const correctAnswers = normalizeAnswers(state.correctAnswers);

  question.answers.forEach((answer, index) => {
    const button = document.createElement("button");
    const isVisible = index < state.revealedAnswers;
    const isPicked = savedAnswers.includes(answer) || selectedAnswers.includes(answer);
    button.className = `answer-card answer-${index % 6}`;
    button.disabled = !isVisible || state.phase !== "timer" || me.answered;

    if (!isVisible) {
      button.textContent = `תשובה ${index + 1}`;
      button.classList.add("hidden-answer");
    } else {
      fillAnswerButton(button, question, answer);
    }
    if (isPicked) {
      button.classList.add("picked");
    }
    if (correctAnswers.includes(answer)) {
      button.classList.add("correct");
    }
    if (isPicked && correctAnswers.length && !correctAnswers.includes(answer)) {
      button.classList.add("wrong-picked");
    }

    button.onclick = () => toggleAnswer(answer, question.allowMultiple);
    el.answersList.appendChild(button);
  });

  if (state.phase === "timer" && !me.answered) {
    el.submitAnswer.classList.remove("hidden");
    el.submitAnswer.disabled = selectedAnswers.length === 0;
    el.submitAnswer.textContent = question.allowMultiple ? "שלח תשובות" : "שלח תשובה";
  } else {
    el.submitAnswer.classList.add("hidden");
  }
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

function toggleAnswer(answer, allowMultiple) {
  if (allowMultiple) {
    if (selectedAnswers.includes(answer)) {
      selectedAnswers = selectedAnswers.filter((item) => item !== answer);
    } else {
      selectedAnswers = [...selectedAnswers, answer];
    }
  } else {
    selectedAnswers = [answer];
  }
  loadState();
}

async function submitAnswer() {
  if (!selectedAnswers.length) {
    return;
  }
  el.answerMessage.textContent = "התשובה נקלטה.";
  await fetch("/api/player/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ playerId, answers: selectedAnswers }),
  });
  selectedAnswers = [];
  loadState();
}

function statusText(state, me) {
  const correctAnswers = normalizeAnswers(state.correctAnswers);
  if (state.phase === "review") {
    return `תשובה נכונה: ${correctAnswers.join(", ")}`;
  }
  if (me.answered) {
    return "התשובה נקלטה.";
  }
  if (state.phase === "timer") {
    return state.question.allowMultiple ? "אפשר לבחור כמה תשובות ואז לשלוח." : "אפשר לבחור תשובה ולשלוח.";
  }
  if (state.phase === "timer_done") {
    return "הזמן נגמר.";
  }
  return "ממתינים שהמנחה יתחיל את הטיימר.";
}

function normalizeAnswers(value) {
  if (!value) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
}

function formatScore(score) {
  return Number.isInteger(score) ? String(score) : String(score).replace(/\.0$/, "");
}

setInterval(loadState, 500);
