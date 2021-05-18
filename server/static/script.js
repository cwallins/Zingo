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