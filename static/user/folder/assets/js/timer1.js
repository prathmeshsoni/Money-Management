

/*=====================
  timer js
 ==========================*/
(function($) {
    "use strict";

//    Set the date we're counting down to
var countDownDate = new Date("feb 27, 2021 24:00:00").getTime();

//    Update the count down every 1 second
var x = setInterval(function() {

// Get todays date and time
    var now = new Date().getTime();

// Find the distance between now an the count down date
    var distance = countDownDate - now;

// Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

// Output the result in an element with id="demo"
    document.getElementById("demo").innerHTML = "<span>" + days + "<span class='timer-cal'>Days</span></span>" + "<span>" + hours + "<span class='timer-cal'>Hrs</span></span>"
        + "<span>" + minutes + "<span class='timer-cal'>Min</span></span>" + "<span>" + seconds + "<span class='timer-cal'>Sec</span></span> ";   

// If the count down is over, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("demo").innerHTML = "EXPIRED";
    }
}, 1000);
})(jQuery);