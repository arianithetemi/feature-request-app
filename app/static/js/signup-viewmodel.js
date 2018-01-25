$(document).ready(function() {

   ko.validation.rules.pattern.message = 'Invalid.';

   ko.validation.init({
       registerExtenders: true,
       messagesOnModified: true,
       insertMessages: true,
       parseInputAttributes: true,
       messageTemplate: null
   }, true);

   var mustEqual = function(val, other) {
      return val == other;
   };

   var signUpViewModel = {
      firstName: ko.observable("").extend({required: true}),
      lastName: ko.observable("").extend({required: true}),
      username: ko.observable("").extend({required: true, minLength: 5, maxLength: 20}),
      emailAddress: ko.observable("").extend({required: true}),
      company: ko.observable("").extend({required: true}),
      password: ko.observable(""),
      confirmPassword: ko.observable(""),
      submit: function() {
         if (signUpViewModel.errors().length === 0) {
            var jsonData = {
               first_name: this.firstName(),
               last_name: this.lastName(),
               username: this.username(),
               email_address: this.emailAddress(),
               company: this.company(),
               password: this.password(),
               confirm_password: this.confirmPassword(),
               role: "client"
            };

            $.ajax({
               method: 'POST',
               url: '/api/user/add',
               contentType: 'application/json',
               dataType: 'json',
               data: JSON.stringify(jsonData),
               success: function(data) {
                  if(data.message == 'Username is taken!') {
                     $('.username-err').html('This ' + data.message.toLowerCase());
                  } else if (data.message == 'Password and Confirm Password do not match!') {
                     $('.pass-up-err').html(data.message);
                  } else {
                     swal("Success!", "Your account has been created!", "success")
                        .then(function() {
                           window.location.href = '/';
                        });
                  }
               }
            })
         }
         else {
            signUpViewModel.errors.showAllMessages();
         }
      }
   };

   $('#username').keyup(function() {
      $('.username-err').html('');
   });

   signUpViewModel.confirmPassword = ko.observable().extend({
      validation: {
         validator: mustEqual,
         message: 'Passwords do not match.',
         params: signUpViewModel.password
      }
   });

   signUpViewModel.errors = ko.validation.group(signUpViewModel);

   signUpViewModel.requireLocation = function() {
      signUpViewModel.location.extend({required: true});
   };

   ko.applyBindings(signUpViewModel, document.getElementById('sign-up'));

});
