

/*Popover for 'Rules' --> Works when executed in base.html */


  /*Popover for 'Rules' --> Works when executed in base.html */
  $(document).ready(function(){
    $( "[data-toggle='popover'" ).popover( );
  });

  $( ".popover_dismiss" ).popover(
      {
        trigger: "focus"
      } 
    ); 


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
/*Time-progress --> Not tested!!

This part may be superfluous
var bar = document.getElementById('progress'),
    time = 0, max = 5,
    int = setInterval(function() {
        bar.style.width = Math.floor(100 * time++ / max) + '%';
        time - 1 == max && clearInterval(int);
    }, 1000);
*/
/*End of superflouous part

THE REAL CODE
function countdown(callback) {
  var bar = document.getElementById('progress'),
  time = 0, max = 5,
  int = setInterval(function() {
      bar.style.width = Math.floor(100 * time++ / max) + '%';
      if (time - 1 == max) {
          clearInterval(int);
          // 600ms - width animation time
          callback && setTimeout(callback, 600);
      }
  }, 1000);
}

countdown(function() {
  alert('Redirect');
});

END OF REAL CODE

*/