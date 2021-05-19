
/* Playing a game */
$("#qa").hide();
$("#show-ca").hide();
$("#end-game").hide();

/* When clicking "Start game" in lobby */
$("#start-game").on("click", function() {
  $("#game-lobby").hide();
  $("#qa").show();
});

/* When clicking any answer show correct answer and current scores */
$(".col-md-6").on("click", function() {
  $("#qa").hide();
  $("#show-ca").show();
});

/* Score screen, on button-click show next question */ 
$("#next-q").on("click", function() {
  $("#qa").show();
  $("#show-ca").hide();
  var currentQuestion = $("#active");
  if (currentQuestion.next().length > 0 ){
    currentQuestion.next().attr("id", "active");
  } else {
    $("#next-q").hide();
    $("#end-game").show();
    }
  
  currentQuestion.removeAttr("id");
});

/* When there's no questions left, show total results */
$("#end-game").on("click", function() {
  

});