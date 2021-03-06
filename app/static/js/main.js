$(document).ready(function() {
   $('#sign-up-btn').click(function() {
      $('#sign-in').hide();
      $('#sign-up').show()
   });
   $('#sign-in-btn').click(function() {
      $('#sign-in').show();
      $('#sign-up').hide();
   });

   var SignInViewModel = {
       username_email: ko.observable(""),
       password: ko.observable(""),
       submit: function() {
          $.ajax({
             method: "POST",
             url: "/api/auth",
             contentType: "application/json",
             dataType: "json",
             data: ko.toJSON(this),
             success: function(result) {
                if(result.message == 'Username or Email is invalid!') {
                  $('.sign-in-err').html(result.message);
               }
               if(result.message == 'Password is invalid!') {
                  $('.sign-in-err').html(result.message);
               }
               if(result.message == 'Your account is not activated yet!') {
                  $('.sign-in-err').html(result.message);
               }
               if(result.message == 'Successfully login') {
                  $('.sign-in-err').html('');
                  localStorage.setItem('token', result.token);
                  // localStorage.setItem('isLogged', true);

                  $.ajax({
                    url: "/dashboard",
                    type: 'GET',
                    headers: {"x-access-token": localStorage.getItem('token')},
                    success: function(data) {
                      $(".se-pre-con").show().delay(700).fadeOut('slow');

                      setTimeout(function(){
                        document.write(data);
                        setTimeout(() => {
                          window.stop();
                        }, 750);
                      }, 700);
                    }
                  });
               }
            }
          });
       }
   };
   ko.applyBindings(SignInViewModel, document.getElementById('sign-in'));

   $('#username-email, #password').keypress(function(event) {
    var keycode = event.keyCode || event.which;
    if(keycode == '13') {
      $('.sign-in-button').trigger('click');
    }
});

   if(localStorage.getItem('token') !== null) {
      $.ajax({
         url: "/dashboard",
         type: 'GET',
         headers: {"x-access-token": localStorage.getItem('token')},
         success: function(data) {
            if (typeof data == 'string') {
              setTimeout(function() {
                document.write(data);
                setTimeout(function(){
                  window.stop();
                }, 600);
              }, 300);

            } else {
               localStorage.removeItem('token');
               window.location.href = '/';
            }
         }
      });
   }

});
