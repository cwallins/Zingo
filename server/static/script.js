
/* Playing a game */


$("#qa").hide();
$("#show-ca").hide();
$("#end-game").hide();

$("#start-game").on("click", function() {
  $("#game-lobby").hide();
  $("#qa").show();
});

$(".col-md-6").on("click", function() {
  $("#qa").hide();
  $("#show-ca").show();
});

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

$("#end-game").on("click", function() {
  

});


