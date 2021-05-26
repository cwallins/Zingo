$("#question-game-questions .show-question button").on("click", function() {
  const answer = $(this).text();
  const correctAnswer = $(this).parent().attr("data-correct-answer");
  const score = parseInt($("#score").val());
  console.log($(this).parent().next().hasClass('show-question'))
  $(this).parent().hide() //Hides current parent 
  $(this).parent().next().show() //Shows the next parent
  resetTimer(init_time) //Resets the timer

  if (answer === correctAnswer) {
    $("#score").val(score + time ); //Amount of time left genereates your points
  } 

//If there are no more questions, print the points and hide the timer, otherwise start the time again
  if (!$(this).parent().next().hasClass('show-question')){
    $(".scoretest").text("Your final score: " + $("#score").val())
    $(".timer").empty()
  } else{
    timer()
  }
});

// Playing a game, hide the questions wihtin the question package 
$(document).ready(function(){
  $(".show-question").hide();
  $(".end-game").hide();
  });
  
  //When you click on start game in lobby
  $("#start-game").on("click", function() {
    $(".start-game-menu").hide();
    $(".show-question"+"#1").show()
    $(".end-game").show();
    timer() //Start timer
});

var init_time; 
var time; 
function timer(){
  time = 19;
  var timerDiv = document.getElementById('timer');
  timerDiv.innerHTML = " 20 seconds remaining";

  init_time = setInterval(count, 1000);
  function count(){
    if (time >= 0){
      timerDiv.innerHTML = time + " seconds remaining";
      time--;
      if (time === -1) {
        time = 0;
      }     
    }   
  }
}

//Stops the time and resets
function resetTimer(timer){
  clearInterval(timer)
}

$(".read_more-link").on("click", function(){
  alert("It's your lucky day, we don't have any terms and conditions, they are for loosers! Have fun!")
});

mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

$(document).ready(function(){
  $("#feedback-popup").hide();
});

$("#feedback-send").on("click", function(){
  $("#feedback-popup").show();
  $("#feedback-comment").val("");
})

$(document).ready(function () {
  const currentLocation = location.href;
  const menuItem = document.querySelectorAll('a');
  const menuLength = menuItem.length
  for (let i = 0; i<menuLength; i++){
    if(menuItem[i].href === currentLocation){
      menuItem[i].className += " " + "active"
    }
  }
});