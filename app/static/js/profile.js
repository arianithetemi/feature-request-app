// Populating profile info
$('.profile-link').click(function() {
  var publicId = $(this).attr('data-publicId');
  $.ajax({
    url: '/api/user/'+publicId,
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    contentType: 'application/json',
    success: function(data) {
      $('#p-first-name').html(data.user.first_name);
      $('#p-last-name').html(data.user.last_name);
      $('#p-username').html(data.user.username);
      $('#p-email').html(data.user.email_address);
      $('#p-company').html(data.user.company);
    }
  });
});

// Public id of current user
var publicId = $('.profile-link').attr('data-publicId');

ko.validation.rules.pattern.message = 'Invalid.';
ko.validation.init({
    registerExtenders: true,
    messagesOnModified: true,
    insertMessages: true,
    parseInputAttributes: true,
    messageTemplate: null
}, true);

// Populating input in edit profile form
$('#edit-profile-link').click(function() {
  ko.cleanNode(document.getElementById('edit-profile'));
  $.ajax({
    url: '/api/user/'+publicId,
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    contentType: 'application/json',
    success: function(data) {
      var updateProfileViewModel = {
         firstName: ko.observable(data.user.first_name).extend({required: true}),
         lastName: ko.observable(data.user.last_name).extend({required: true}),
         emailAddress: ko.observable(data.user.email_address).extend({required: true, email: true}),
         company: ko.observable(data.user.company).extend({required: true}),
         submit: function() {
            if (updateProfileViewModel.errors().length === 0) {
               var jsonData = {
                  first_name: this.firstName(),
                  last_name: this.lastName(),
                  email_address: this.emailAddress(),
                  company: this.company()
               };

               $.ajax({
                  method: 'PUT',
                  url: '/api/user/update/'+publicId,
                  contentType: 'application/json',
                  dataType: 'json',
                  data: JSON.stringify(jsonData),
                  headers: {"x-access-token": localStorage.getItem('token')},
                  success: function(data) {
                    swal("Success!", "Profile updated successfully", "success")
                     .then(function() {
                        $('#edit-profile-modal').modal('hide');
                        $('#p-first-name').html(data.user.first_name);
                        $('#p-last-name').html(data.user.last_name);
                        $('#p-username').html(data.user.username);
                        $('#p-email').html(data.user.email_address);
                        $('#p-company').html(data.user.company);
                     });
                    }
               });
            }
            else {
               updateProfileViewModel.errors.showAllMessages();
            }
         }
      };

      updateProfileViewModel.errors = ko.validation.group(updateProfileViewModel);

      updateProfileViewModel.requireLocation = function() {
         updateProfileViewModel.location.extend({required: true});
      };

      ko.applyBindings(updateProfileViewModel, document.getElementById('edit-profile'));
    }
  });
});

var mustEqual = function(val, other) {
   return val == other;
};
