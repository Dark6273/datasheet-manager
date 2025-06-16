var timer;
var startTime = 0;
var recordedtime = 0;
var pausetime = 0;
let isSaved = false;

function startTimer() {
  isSaved = false;
  console.log(isSaved);
  startTime = new Date(Date.now());
  pausetime = new Date(Date.now());
  timer = setInterval(updateTimer, 1000);
  document.getElementById("startButton").disabled = true;
  document.getElementById("pause").removeAttribute("disabled");
}

function stopTimer() {
  clearInterval(timer);
  document.getElementById("stopTimeInput").value =
    document.getElementById("timer").innerHTML;
  document.getElementById("startButton").disabled = false;
  document.getElementById("stopButton").disabled = true;
  isSaved = true;
  console.log(isSaved);
}

function onPause() {
  clearInterval(timer);
  console.log("pause clicked");
  let button = document.querySelector("#pause");
  button.innerText = "Resume";
  button.id = "Resume";
  button.classList = "btn btn-outline-info";
  button.setAttribute("onclick", "onResume()");
}

function onResume() {
  pausetime = new Date(Date.now() - recordedtime);
  console.log("resume clicked");
  let button = document.querySelector("#resume");
  button.innerText = "Pause";
  button.id = "Pause";
  button.classList = "btn btn-outline-danger";
  button.setAttribute("onclick", "onPause()");
  timer = setInterval(updateTimer, 1000);
}

function updateTimer() {
  var currentTime = new Date(Date.now());
  var elapsedTime = new Date(currentTime - pausetime);
  recordedtime = elapsedTime;
  var formattedTime = recordedtime.toISOString().substr(11, 8);

  document.getElementById("timer").innerHTML = formattedTime;
}

window.addEventListener("beforeunload", function (e) {
  if (!isSaved) {
    e.preventDefault();
    e.returnValue = ""; // فعال‌سازی هشدار خروج
  }
});

document
  .getElementById("timerForm")
  .addEventListener("submit", function (event) {
    clearInterval(timer);
    var stopTime = Date.now();
    pausetime = new Date(Date.now() - recordedtime);
    var temp = stopTime - pausetime;
    document.getElementById("id_time").value = temp;
  });

document.getElementById("startButton").addEventListener("click", startTimer);
document.getElementById("stopButton").addEventListener("click", stopTimer);
