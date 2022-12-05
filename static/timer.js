// Constants
const WORK_MIN = 25;
const SHORT_BREAK_MIN = 5;
const LONG_BREAK_MIN = 20;

var reps = 0;

// DOM variables
var title = document.getElementById("title");
var timer = document.getElementById("timer");
var check_marks = document.getElementById("checkmarks");

var start_btn = document.getElementById("start");
var reset = document.getElementById("reset");

// Resets the timer by setting reps to 0 and reloading the page
function reset_timer() {
  reps = 0;
  location.reload();
}

// Starts timer
function start_timer() {
  var work_sec = WORK_MIN * 60;
  var short_break_sec = SHORT_BREAK_MIN * 60;
  var long_break_sec = LONG_BREAK_MIN * 60;

  check_marks.innerHTML = "0";

  reps += 1;

  // Checks if it's time to study or take a break
  if (reps % 2 == 1) {
    count_down(work_sec);
    title.innerHTML = "Study";
  } else if (reps == 8) {
    count_down(long_break_sec);
    title.innerHTML = "Break";
  } else {
    count_down(short_break_sec);
    title.innerHTML = "Break";
  }
}

// Updates DOM variables to count down a specified number of seconds
function count_down(count) {
  count_min = Math.floor(count / 60);
  count_sec = count % 60;

  // Formats the seconds with/without leading zeroes
  if (count_sec == 0) {
    count_sec = "00";
  } else if (count_sec < 10) {
    count_sec = "0" + count_sec;
  }

  // Formats the minutes with leading zero
  if (count_min < 10) {
    count_min = "0" + count_min;
  }

  // Updates the timer text
  timer.innerHTML = count_min + ":" + count_sec;

  // Creates a delay before recursively calling itself
  if (count > 0) {
    setTimeout(function () {
      count_down(count - 1);
    }, 1000);
  } else {
    // Count down finished, call start_timer() to update text
    start_timer();
    var mark = Number(check_marks.innerHTML);
    var work_sessions = Math.floor(reps / 2);

    // Adds up check marks
    for (let i = 0; i < work_sessions; i++) {
      mark++;
    }

    check_marks.innerHTML = mark;

    // Plays a sound effect to indicate completion
    var sound = new Audio("static/sessionCompleted.mp3");
    sound.play();
  }
}

// Add event listeners to buttons
start_btn.addEventListener("click", function () {
  start_timer();
  start_btn.disabled = true;
});

reset.addEventListener("click", function () {
  reset_timer();
});
