$('#add-approved-feature-request').click(function() {

  // Showing datepicker
  setTimeout(function(){
    $('.date').datepicker({
      autoclose: true,
      todayHighlight: true,
      toggleActive: true
    });
  }, 300);

  $.ajax({
     url: '/api/user/',
     method: 'GET',
     contentType: 'application/json',
     data: { role: 'client', status: 'True' },
     headers: {"x-access-token": localStorage.getItem('token')},
     success: function(res) {
        if (res != '') {
           // Populating the a selection array with active clients, then pass it to view model
           clientsSelectionArray = [];
           res.map(client => {
              console.log(client.first_name, client.public_id)
              clientsSelectionArray.push({"publicId": client.public_id,
                                     "fullNameCompany": client.first_name + ' ' + client.last_name + ' - ' + client.company,
                                     "parent": null});
           });

           // Populating the area selection array then pass it to view model
           areaSelectionArray = [{"areaName": "Policies", "parent": null},
                                 {"areaName": "Billing", "parent": null},
                                 {"areaName": "Claims", "parent": null},
                                 {"areaName": "Reports", "parent": null}];

           ko.cleanNode(document.getElementById('add-approved-feature-request-form'));

           // New approved feature request View Modal
           var approvedFeatureRequestViewModel = {
             clientsSelection: clientsSelectionArray,
             clientSelect: ko.observable().extend({required: {message: "Please select a client."}}),
             areaSelection: areaSelectionArray,
             areaSelect: ko.observable().extend({required: {message: "Please select an area."}}),
             title: ko.observable("").extend({required: true}),
             description: ko.observable("").extend({required: true}),
             clientPriority: ko.observable("").extend({required: true}),
             targetDate: ko.observable("").extend({required: true}),
              submit: function() {
                 if (approvedFeatureRequestViewModel.errors().length === 0) {
                    var jsonData = {
                       title: this.title(),
                       description: this.description(),
                       client_priority: this.clientPriority(),
                       target_date: this.targetDate()
                    };

                    // Ajax Call
                    console.log('submitted')
                 }
                 else {
                    approvedFeatureRequestViewModel.errors.showAllMessages();
                 }
              }
           };

           approvedFeatureRequestViewModel.errors = ko.validation.group(approvedFeatureRequestViewModel);

           approvedFeatureRequestViewModel.requireLocation = function() {
              approvedFeatureRequestViewModel.location.extend({required: true});
           };

           ko.applyBindings(approvedFeatureRequestViewModel, document.getElementById('add-approved-feature-request-form'));

        } else {
           console.log('No clients');
        }
     }
  });
});
