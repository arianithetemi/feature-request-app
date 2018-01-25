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
      submit: function() {
         if (signUpViewModel.errors().length === 0) {
            alert('Thank you.');
         }
         else {
            signUpViewModel.errors.showAllMessages();
         }
      }
   };

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
