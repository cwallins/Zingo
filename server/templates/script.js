function myFunction() {
    /* Get the text field */
    var copyText = document.getElementById("Invite_player_url");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("Copy URL");
  
    /* Alert the copied text */
    alert("Copied URL: " + copyText.value);
  }