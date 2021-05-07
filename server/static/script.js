
/*Popover for 'Rules--> DENNA FUNKAR INTE ÄN'

var popover = new bootstrap.Popover(document.querySelector('.popover-dismiss'), {
  trigger: 'focus'
})
END OF POPOVER-CODE

*/

/*Time-progress

/*This part is maybe superfluous
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


