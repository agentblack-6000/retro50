// Constants
const WORK_MIN = 1
const SHORT_BREAK_MIN = 1
const LONG_BREAK_MIN = 1

// DOM variables
var reps = 0
var title = document.getElementById("title");
var timer = document.getElementById("timer");
var check_marks = document.getElementById("checkmarks")

var start_btn = document.getElementById("start");
var reset = document.getElementById("reset");

function reset_timer() {
    reps = 0;
    // timer.innerHTML = "00 : 00";
    // check_marks.innerHTML = "0";
    location.reload()
}

function start_timer() {
    var work_sec = WORK_MIN * 60;
    var short_break_sec = SHORT_BREAK_MIN * 60;
    var long_break_sec = LONG_BREAK_MIN * 60;

    check_marks.innerHTML = "0";

    reps += 1;

    if (reps % 2 == 1) {
        count_down(work_sec);
        title.innerHTML = "Work";
    }
    else if (reps == 8) {
        count_down(long_break_sec);
        title.innerHTML = "Break";
    }
    else {
        count_down(short_break_sec);
        title.innerHTML = "Break";
    }
}

function count_down(count) {
    count_min = Math.floor(count / 60)
    count_sec = count % 60

    if (count_sec == 0) {
        count_sec = "00";
    }
    else if (count_sec < 10) {
        count_sec = "0" + count_sec;
    }

    if (count_min < 10) {
        count_min = "0" + count_min;
    }

    timer.innerHTML =  count_min + ":" + count_sec;

    if (count > 0) {
        setTimeout(function () {
            count_down(count - 1)
        }, 1000);
    }
    else {
        start_timer();
        var mark = Number(check_marks.innerHTML);
        var work_sessions = Math.floor(reps / 2);

        for (let i = 0; i < work_sessions; i++)
        {
            mark++;
        }

        check_marks.innerHTML = mark;
        var sound = new Audio('static/sessionCompleted.mp3');
        sound.play();
    }
}

start_btn.addEventListener('click', function() {
    start_timer();
    start_btn.disabled = true;
});

reset.addEventListener('click', function() {
    reset_timer();
});
