

/*Popover for 'Rules' --> Works when executed in base.html */


  /*Popover for 'Rules' --> Works when executed in base.html */
var show_rules
$(document).ready(function(){
  $( "[data-toggle='popover'" ).popover( );
});

$( "#popover_dismiss" ).popover( 
{
    trigger: "focus"
});


/*Prov-kod till show_and_hide --> First variable is proven to work when executed in base.html but crash immediately after. The rest in untested.*/

var hide_when_guest
$(document).ready(function() {
  $('#logout, .nav-link-signed-in').hide();
});

var show_hide_when_signed_in
$(document).ready(function() {
  if 'loggedin' in session: /* quote-python-kod (checks if the user is a registered user)--> How rewrite this to work here? */
    $('#sign_in_button').on('click', function() {
      $('#logout, .nav-link-signed-in').show();
      $('.nav-link-guest').hide();

    })
  else
    $('#logout, .nav-link-signed-in').hide(); /* Lazy code, may not work. */
});

var show_hide_When_reg_user_turned_to_guest
$(document).ready(function() {
  $('#logout').on('click', function() {
    $('#logout, .nav-link-signed-in, nav-link-guest ').toggle();
  });
});

/* End of code for show_hide */


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


