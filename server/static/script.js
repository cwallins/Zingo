
/* Playing a game */
$("#qa").hide();
$("#show-ca").hide();

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
});