$(document).ready(function() {
   $('#sign-up-btn').click(function() {
      $('#sign-in').hide();
      $('#sign-up').show()
      $('.sign-up').css({'margin-top': '6%'});
   });
   $('#sign-in-btn').click(function() {
      $('#sign-in').show();
      $('#sign-up').hide();
      $('.sign-up').css({'margin-top': '17%'});
   });
});
