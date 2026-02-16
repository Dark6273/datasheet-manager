let timer = null;
let startTimestamp = 0;
let elapsedMs = 0;

const startButton = document.getElementById("startButton");
const pauseButton = document.getElementById("pauseButton");
const timerDisplay = document.getElementById("timer");
const timeInput = document.getElementById("id_time");
const timerForm = document.getElementById("timerForm");
const backgroundToggle = document.getElementById("backgroundToggle");
const ring = document.querySelector(".timer-ring__progress");
const hand = document.querySelector(".timer-hand");
const resetButton = document.getElementById("resetButton");

const STORAGE_KEY = "timerState";
const BACKGROUND_KEY = "timerBackground";
const RING_CIRCUMFERENCE = 2 * Math.PI * 68;

function setPauseButton(state) {
  pauseButton.dataset.state = state;
  if (state === "pause") {
    pauseButton.innerHTML =
      '<span class="icon material-symbols-rounded" aria-hidden="true">pause</span>Pause';
    pauseButton.classList.remove("btn--resume");
    pauseButton.classList.add("btn--pause");
  } else {
    pauseButton.innerHTML =
      '<span class="icon material-symbols-rounded" aria-hidden="true">play_arrow</span>Resume';
    pauseButton.classList.remove("btn--pause");
    pauseButton.classList.add("btn--resume");
  }
}

function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${hours.toString().padStart(2, "0")}:${minutes
    .toString()
    .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}

function render() {
  timerDisplay.textContent = formatTime(elapsedMs);
  if (ring) {
    const seconds = Math.floor(elapsedMs / 1000);
    const progress = (seconds % 60) / 60;
    const offset = RING_CIRCUMFERENCE * (1 - progress);
    ring.style.strokeDasharray = `${RING_CIRCUMFERENCE}`;
    ring.style.strokeDashoffset = `${offset}`;
    if (hand) {
      const angle = progress * 360;
      hand.style.transform = `rotate(${angle}deg)`;
      const strength = 0.35 + progress * 0.65;
      hand.style.setProperty("--hand-strength", strength.toFixed(2));
      hand.style.setProperty("--hand-glow", (0.15 + progress * 0.35).toFixed(2));
    }
  }
}

function tick() {
  elapsedMs = Date.now() - startTimestamp;
  render();
}

function persistState(running) {
  const payload = {
    running,
    startTimestamp,
    elapsedMs,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function startTimer() {
  startTimestamp = Date.now() - elapsedMs;
  timer = setInterval(tick, 1000);
  startButton.disabled = true;
  pauseButton.disabled = false;
  setPauseButton("pause");
  persistState(true);
}

function pauseTimer() {
  clearInterval(timer);
  setPauseButton("resume");
  persistState(false);
}

function resumeTimer() {
  startTimestamp = Date.now() - elapsedMs;
  timer = setInterval(tick, 1000);
  setPauseButton("pause");
  persistState(true);
}

pauseButton.addEventListener("click", () => {
  if (pauseButton.dataset.state === "pause") {
    pauseTimer();
  } else {
    resumeTimer();
  }
});

startButton.addEventListener("click", startTimer);

resetButton.addEventListener("click", () => {
  clearInterval(timer);
  timer = null;
  elapsedMs = 0;
  startTimestamp = 0;
  render();
  startButton.disabled = false;
  pauseButton.disabled = true;
  setPauseButton("pause");
  localStorage.removeItem(STORAGE_KEY);
});

timerForm.addEventListener("submit", () => {
  clearInterval(timer);
  timeInput.value = elapsedMs;
  elapsedMs = 0;
  startTimestamp = 0;
  render();
  startButton.disabled = false;
  pauseButton.disabled = true;
  setPauseButton("pause");
  localStorage.removeItem(STORAGE_KEY);
});

if (backgroundToggle) {
  const savedBackground = localStorage.getItem(BACKGROUND_KEY) === "true";
  backgroundToggle.checked = savedBackground;
  backgroundToggle.addEventListener("change", () => {
    localStorage.setItem(BACKGROUND_KEY, backgroundToggle.checked ? "true" : "false");
  });
}

function restoreTimer() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return;
  }
  try {
    const data = JSON.parse(raw);
    elapsedMs = data.elapsedMs || 0;
    startTimestamp = data.startTimestamp || Date.now() - elapsedMs;
    render();
    if (data.running) {
      timer = setInterval(tick, 1000);
      startButton.disabled = true;
      pauseButton.disabled = false;
      setPauseButton("pause");
    } else {
      setPauseButton("resume");
    }
  } catch (error) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

restoreTimer();

window.addEventListener("beforeunload", (event) => {
  const raw = localStorage.getItem(STORAGE_KEY);
  const allowBackground = localStorage.getItem(BACKGROUND_KEY) === "true";
  if (!raw || allowBackground) {
    return;
  }
  event.preventDefault();
  event.returnValue = "";
});
