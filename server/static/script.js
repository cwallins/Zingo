
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

/* Koden till timerquizet om ni vill kolla */
var question001 = ["There are 9 continents in the world.", //Här kanske vi kan connecta vår DB-paket//
      "There is no islands on Earth.",
      "Blue whales are mammals.",
      "Tomatoes are vegetables.",
      "The Blue Whale feeds on Tuna fish.",
      "Fifa World Cup tournaments are played every 4 years.",
      "The north side of the Equator Line has more countries than the south side.",
      "Madagascar is the largest island in the world.",
      "Helium is the lightest gas element out of all gas elements.",
      "The hottest planet in the solar system is Mercury."
    ];

    var options001 = ["<button class=buttons001 onclick=q1i()>True</button><br /><br /><button class=buttons001 onclick=q1c()>False</button>"];
    var options002 = ["<button class=buttons001 onclick=q2c()>False</button><br /><br /><button class=buttons001 onclick=q2i()>True</button>"];
    var options003 = ["<button class=buttons001 onclick=q3c()>True</button><br /><br /><button class=buttons001 onclick=q3i()>False</button>"];
    var options004 = ["<button class=buttons001 onclick=q4i()>True</button><br /><br /><button class=buttons001 onclick=q4c()>False</button>"];
    var options005 = ["<button class=buttons001 onclick=q5c()>False</button><br /><br /><button class=buttons001 onclick=q5i()>True</button>"];
    var options006 = ["<button class=buttons001 onclick=q6i()>False</button><br /><br /><button class=buttons001 onclick=q6c()>True</button>"];
    var options007 = ["<button class=buttons001 onclick=q7c()>True</button><br /><br /><button class=buttons001 onclick=q7i()>False</button>"];
    var options008 = ["<button class=buttons001 onclick=q8c()>False</button><br /><br /><button class=buttons001 onclick=q8i()>True</button>"];
    var options009 = ["<button class=buttons001 onclick=q9c()>True</button><br /><br /><button class=buttons001 onclick=q9i()>False</button>"];
    var options010 = ["<button class=buttons001 onclick=q10i()>True</button><br /><br /><button class=buttons001 onclick=q10c()>False</button>"];

    var a = 0;
    a++;
    var b = 0;
    b++;

    function begin001() {
      c = 20;
      disappear001.innerHTML = "";
      message001.innerHTML = question001[0];
      message002.innerHTML = options001;
      number001.innerHTML = a++;
    }

    function q1c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct. There are 7 continents in the world.";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q1i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. There are 7 continents in the world.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q2c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct. There is a lot of islands on Earth.";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q2i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. There is a lot of islands on Earth.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q3c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q3i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. They do have 2 toes in each leg.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q4c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct. Tomatoes are classified under fruits.";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q4i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. Tomatoes are classified under fruits.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q5c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct. The blue whale feeds on small shrimp-like fish called Krills.";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q5i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. The Blue Whale feeds on small shrimp-like fish called Krills.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q6c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q6i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. Fifa World Cup tournaments are played every 4 years.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q7c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q7i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. More countries on the north side than there are on the south side.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q8c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct. Greenland is the largest island in the world.";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q8i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. Greenland is the largest island in the world.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q9c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q9i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. Helium is the lightest gas of all gas elements.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q10c() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Correct. Venus is the hottest planet. That is because its atmosphere contains 95% of Carbon dioxide.";
      message002.innerHTML = "";
      score001.innerHTML = b++;
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function q10i() {
      window.clearInterval(update);
      c = "-";
      message003.innerHTML = "Incorrect. Venus is the hottest planet. That is because its atmosphere contains 95% of Carbon dioxide.";
      message002.innerHTML = "";
      message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
    }

    function next001() {
      if (a == "2") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[1];
        message002.innerHTML = options002;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "3") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[2];
        message002.innerHTML = options003;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "4") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[3];
        message002.innerHTML = options004;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "5") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[4];
        message002.innerHTML = options005;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "6") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[5];
        message002.innerHTML = options006;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "7") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[6];
        message002.innerHTML = options007;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "8") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[7];
        message002.innerHTML = options008;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "9") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[8];
        message002.innerHTML = options009;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      }

      else if (a == "10") {
        update = setInterval("timer001()", 1000);
        c = 20;
        time001.innerHTML = 20;
        message001.innerHTML = question001[9];
        message002.innerHTML = options010;
        message003.innerHTML = "";
        number001.innerHTML = a++;
        message004.innerHTML = "";
      } else {
        window.clearInterval(update);
        c = "-";
        message001.innerHTML = "End of Quiz";
        message002.innerHTML = "";
        message003.innerHTML = "";
        message004.innerHTML = "<button class=buttons002 onclick=repeat001()>Repeat</button>";
      }
    }

    function timer001() {
      c = c - 1;
      if (c < 200) {
        time001.innerHTML = c;
      }

      if (c < 1) {
        window.clearInterval(update);
        message001.innerHTML = "Tiden är ute!";
        message002.innerHTML = "";
        message003.innerHTML = "";
        message004.innerHTML = "<button class=buttons002 onclick=next001()>Next</button>";
      }
    }

    update = setInterval("timer001()", 1000);

    function repeat001() {
      location.reload();
    }

