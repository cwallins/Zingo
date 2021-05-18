$("#question-game-questions .show-question button").on("click", function() {
  const answer = $(this).text();
  const correctAnswer = $(this).parent().attr("data-correct-answer");
  const score = parseInt($("#score").val());

  if (answer === correctAnswer) {
    console.log("Rätt!");
    $("#score").val(score + 1);
  } else {
    console.log("FEL!");
  }
});

//When clicked on an answer next question get shown
$("#question-game-questions .show-question button").on("click", function() {
//.....



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


/* Playing a game */
$(document).ready(function(){
$(".show-question").hide();
});

/* When clicking "Start game" in lobby */
$("#start-game").on("click", function() {
  $(".start-game-menu").hide();
  $(".show-question").show();
});


/*test*/
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