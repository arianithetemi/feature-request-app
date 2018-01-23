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
               if(result.message == 'User is not activated!') {
                  $('.sign-in-err').html(result.message);
               }
               if(result.message == 'Successfully login') {
                  $('.sign-in-err').html('');
                  localStorage.setItem('token', result.token);
                  console.log(localStorage.getItem('token'));

                  // $(function(){
                  //   var tokenValue = $("meta[name='X-CSRFToken']").attr(localStorage.getItem('token'));
                  //   $.ajaxSetup({
                  //     headers: {'x-access-token': tokenValue}
                  //   });
                  // });

                  // $.ajax({
                  //   url: "/dashboard",
                  //   type: 'GET',
                  //   headers: {"x-access-token": localStorage.getItem('token')},
                  //   success: function(data) {
                  //      document.write(data);
                  //      $.ajaxSetup({
                  //        headers: {"x-access-token": localStorage.getItem('token')}
                  //      });
                  //   }
                  // });
               }
            }
          });
       }
   };
   ko.applyBindings(SignInViewModel);


});
