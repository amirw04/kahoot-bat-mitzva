const el = {
  gameCode: document.getElementById("game-code"),
  phaseLabel: document.getElementById("phase-label"),
  timerLabel: document.getElementById("timer-label"),
  questionTitle: document.getElementById("question-title"),
  questionImages: document.getElementById("question-images"),
  answersList: document.getElementById("answers-list"),
  topPlayers: document.getElementById("top-players"),
};

const phaseText = {
  lobby: "ממתינים",
  question: "שאלה",
  timer: "עונים",
  timer_done: "הזמן נגמר",
  review: "תשובה נכונה",
  finished: "הסתיים",
};

const publicCode = new URLSearchParams(window.location.search).get("code");

async function loadState() {
  const url = publicCode ? `/api/state?code=${encodeURIComponent(publicCode)}` : "/api/state";
  const response = await fetch(url);
  if (!response.ok) {
    el.questionTitle.textContent = "קוד משחק לא נמצא";
    el.answersList.innerHTML = "";
    el.topPlayers.innerHTML = "<li class=\"empty-place\">בדוק את הקישור למסך הציבורי</li>";
    return;
  }
  render(await response.json());
}

function render(state) {
  el.gameCode.textContent = state.code;
  el.phaseLabel.textContent = phaseText[state.phase] || state.phase;
  el.timerLabel.textContent = state.remainingSeconds ?? "--";
  renderQuestion(state);
  renderTopPlayers(state.players || []);
}

function renderQuestion(state) {
  const question = state.question;
  el.answersList.innerHTML = "";

  if (!question) {
    el.questionTitle.textContent =
      state.phase === "finished" ? "המשחק הסתיים" : "ממתינים לשאלה הבאה";
    renderQuestionImages(state, null);
    return;
  }

  el.questionTitle.textContent = question.text;
  renderQuestionImages(state, question);

  const correctAnswers = Array.isArray(state.correctAnswers) ? state.correctAnswers : [];
  question.answers.forEach((answer, index) => {
    const item = document.createElement("div");
    const isVisible = index < state.revealedAnswers;
    item.className = `answer-card answer-${index % 6}`;
    if (!isVisible) {
      item.textContent = `תשובה ${index + 1}`;
      item.classList.add("hidden-answer");
    } else {
      fillAnswer(item, question, answer);
      applyAnswerColor(item, question, answer);
    }
    if (correctAnswers.includes(answer)) {
      item.classList.add("correct");
    }
    el.answersList.appendChild(item);
  });
}

function renderQuestionImages(state, question) {
  el.questionImages.innerHTML = "";
  const images = question
    ? [
        ...(question.questionImages || []),
        ...(question.image ? [question.image] : []),
        ...(state.phase === "review" ? question.correctImages || [] : []),
      ]
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

function fillAnswer(item, question, answer) {
  item.textContent = "";
  const imageName = question.answerImages ? question.answerImages[answer] : null;
  if (imageName) {
    item.classList.add("has-answer-image");
    const image = document.createElement("img");
    image.src = `/images/${imageName}`;
    image.alt = answer;
    image.className = "answer-image";
    item.appendChild(image);
  }
  const label = document.createElement("span");
  label.textContent = answer;
  item.appendChild(label);
}

function applyAnswerColor(element, question, answer) {
  const color = question.answerColors ? question.answerColors[answer] : null;
  if (!Array.isArray(color) || color.length !== 3) {
    return;
  }

  const [red, green, blue] = color.map((value) => Math.round(Number(value) * 255));
  if (element.classList.contains("has-answer-image")) {
    element.style.borderColor = `rgb(${red}, ${green}, ${blue})`;
    element.style.setProperty("--answer-accent", `rgb(${red}, ${green}, ${blue})`);
    element.style.color = "#111827";
    return;
  }

  element.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`;
  element.style.color = textColorForRgb(red, green, blue);
}

function textColorForRgb(red, green, blue) {
  const luminance = (0.299 * red + 0.587 * green + 0.114 * blue) / 255;
  return luminance > 0.58 ? "#111827" : "#ffffff";
}

function renderTopPlayers(players) {
  const topPlayers = players
    .slice()
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name, "he"))
    .slice(0, 5);

  if (!topPlayers.length) {
    el.topPlayers.innerHTML = "<li class=\"empty-place\">אין משתתפים עדיין</li>";
    return;
  }

  el.topPlayers.innerHTML = topPlayers
    .map((player) => `
      <li>
        <span>${escapeHtml(player.name)}</span>
        <strong>${formatScore(player.score)}</strong>
      </li>
    `)
    .join("");
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
