$("#question-game-questions .question button").on("click", function() {
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

//Popover for 'Rules'-button 
  $(document).ready(function(){
    $( "[data-toggle='popover'" ).popover( );
  });

  $( ".popover_dismiss" ).popover(
      {
        trigger: "focus"
  }); 


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