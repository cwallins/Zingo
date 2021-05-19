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
    $("#score").val(score + time); //Så mycket tid som är kvar får du i poäng
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
  });
  
  /* When clicking "Start game" in lobby, när du klickar på starta spel göms div-elementet med knappen starta spel och första frågan i frågepaketet visas */
  $("#start-game").on("click", function() {
    $(".start-game-menu").hide();
    //$(".show-question").show();
    $(".show-question"+"#1").show()
    timer() //starta timer
});


var init_time; 
var time; //tiden som timer stannade på
//startar en tidtagning från 29sek
function timer(){
  time = 29;
  var timerDiv = document.getElementById('timer');
  timerDiv.innerHTML = "30 seconds remaining";

  init_time = setInterval(count, 1000);
  function count(){
    timerDiv.innerHTML = time + " seconds remaining";
    time--;
  }
}
//stoppar tidtagning och nollställer
function resetTimer(timer){
  clearInterval(timer)
  console.log(time)
}
//When clicked on an answer next question get shown
//.....$("#question-game-questions .show-question button").on("click", function() {




//$("show-question").first().fadeout(1000);

//Popover for 'Rules'-button 
/*$(document).ready(function(){
  $( "[data-toggle='popover'" ).popover( );
});

$( ".popover_dismiss" ).popover(
  {
    trigger: "focus"
}); */

/*
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
*/

/* Show one question at a time (??)*/





/*test
  var q = 1,
      qMax = 0;

  $(function () {
      qMax = $('.show-question').length;
      $('.show-question').hide();
      $('.show-question:nth-child(1)').show();
      $('#start-game').on('click', function (event) {
          event.preventDefault();
          handleClick();
      });
  });

  function handleClick() {
      if (q < qMax) 
        {
          $('.show-question:nth-child(' + q + ')').hide();
          $('.show-question:nth-child(' + (q + 1) + ')').show();
          if (q == (qMax - 1)) 
            {
              $('#start-game').html('Submit Answers');
            }
            
          q++;
        } 

      else 
        {
          alert('Submitting'); 
        }
  }});
*/