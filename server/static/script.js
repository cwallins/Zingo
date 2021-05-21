$("#question-game-questions .show-question button").on("click", function() {
  const answer = $(this).text();
  const correctAnswer = $(this).parent().attr("data-correct-answer");
  const score = parseInt($("#score").val());
  console.log($(this).parent().next().hasClass('show-question'))
  $(this).parent().hide() //gömmer nuvarande parent
  $(this).parent().next().show() //visar nästa parent
  resetTimer(init_time) //Reset av timer

  if (answer === correctAnswer) {
    console.log("Rätt!");
    $("#score").val(score + time ); //Så mycket tid som är kvar får du i poäng
  } else {
    console.log("FEL!");
  }
//om det inte finns en ny fråga skriv ut poäng och göm timer annars starta tiden igen
  if (!$(this).parent().next().hasClass('show-question')){
    $(".scoretest").text("Final score: " + $("#score").val())
    $(".timer").empty()
  } else{
    timer()
  }
});

/* Playing a game, göm frågorna i frågepaketet */
$(document).ready(function(){
  $(".show-question").hide();
  $(".end-game").hide();
  });
  
  /* When clicking "Start game" in lobby, när du klickar på starta spel göms div-elementet med knappen starta spel och första frågan i frågepaketet visas */
  $("#start-game").on("click", function() {
    $(".start-game-menu").hide();
    //$(".show-question").show();
    $(".show-question"+"#1").show()
    $(".end-game").show();
    timer() //starta timer
});


var init_time; 
var time; //tiden som timer stannade på
//startar en tidtagning från 29sek
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
        console.log("#yougonegoofed");
        time = 0;
      }     
    }   
  }
}
//stoppar tidtagning och nollställer
function resetTimer(timer){
  clearInterval(timer)
  console.log(time)
}

$("#delete-btn").on("click", function(){
  // console closest element with class=".created_question_packages"
  console.log($(this).closest('.created_question_packages'))
  // hide this selected element
  $(this).closest('.created_question_packages').hide()
});

$(".read_more-link").on("click", function(){
  alert("This is where our terms and conditions are. How fun!")
});


//Popover for 'Rules'-button 
/*$(document).ready(function(){
  $( "[data-toggle='popover'" ).popover( );
});

$( ".popover_dismiss" ).popover(
  {
    trigger: "focus"
}); */


//Get the button:
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

//Testar knappjävel
