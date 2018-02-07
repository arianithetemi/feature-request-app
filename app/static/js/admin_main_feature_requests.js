
// Ajax call for populating approved feature request
const populateApprovedFeatureRequests = function() {
  // Removing the content in the container
  $('.approved-feature-requests-cont').html("");

  // Ajax call to API
  $.ajax({
    url: '/api/feature-request/approved',
    contentType: 'application/json',
    dataType: 'json',
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    success: function(res) {
        // Looping in the all clients from API
        res.data.map(client => {
          // If there is any approved feature request
          if(client.approved_feature_requests.length > 0) {
              // Looping in all feature requests of all clients
              client.approved_feature_requests.map(feature_request => {
                var badge, acceptBtn;
                if (feature_request.status == "Approved") {
                  badge = '<span style="top: -2px; position:relative;" id="badge-'+feature_request.public_id+'" class="badge badge-success">Approved</span>';
                  acceptBtn = '<button data-requestPublicId='+feature_request.public_id+' class="btn btn-sm btn-warning float-right mark-in-progress">Set in progress</button>';

                  // Populating the feature requests in HTML
                  $('.approved-clients-title').hide();
                  $('.approved-feature-requests-cont').prepend('<div class="card mb-4">\
                    <div class="card-header"><h5 style="display:inline">'+ feature_request.title + "</h5> " + badge +' '+ acceptBtn +'</div> \
                    <div class="card-body">\
                      <p style="margin-bottom: 0px;" class="card-text"><b>Client:</b> '+ client.first_name +' '+client.last_name+' <br /> <b>Company:</b> '+client.company+' <br /> <b>Target Date: </b> '+feature_request.target_date+' <br/> <b>Client Priority: </b> '+feature_request.client_priority+' <br/> <b>Product Area:</b> '+feature_request.product_area+' <br /> <b>Description:</b> '+ feature_request.description +' </p>\
                    </div>\
                  </div>');
                }
              });
          } else {
            // If there is no feature request
            $('.approved-clients-title').html("No Approved Feature Requests!");
          }
      });
    }
  });
}
populateApprovedFeatureRequests();

// Ajax call for populating in progress approved feature requests
const populateInProgressApprovedFeatureRequests = function() {
  // Removing the content in the container
  $('.inprogress-feature-requests-cont').html("");

  // Ajax call to API
  $.ajax({
    url: '/api/feature-request/approved',
    contentType: 'application/json',
    dataType: 'json',
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    success: function(res) {
        // Looping in the all clients from API
        res.data.map(client => {
          // If there is any approved feature request
          if(client.approved_feature_requests.length > 0) {
              // Looping in all feature requests of all clients
              client.approved_feature_requests.map(feature_request => {
                var badge, acceptBtn;
                if (feature_request.status == "In Progress") {
                  badge = '<span style="top: -2px; position:relative;" id="badge-'+feature_request.public_id+'" class="badge badge-warning">In Progress</span>';
                  acceptBtn = '<button data-requestPublicId='+feature_request.public_id+' class="btn btn-sm btn-danger float-right mark-closed">Mark as Closed</button>';

                  $('.in-progress-clients-title').hide();
                  $('.inprogress-feature-requests-cont').prepend('<div class="card mb-4">\
                    <div class="card-header"><h5 style="display:inline">'+ feature_request.title + "</h5> " + badge +' '+ acceptBtn +'</div> \
                    <div class="card-body">\
                      <p style="margin-bottom: 0px;" class="card-text"><b>Client:</b> '+ client.first_name +' '+client.last_name+' <br /> <b>Company:</b> '+client.company+' <br /> <b>Target Date: </b> '+feature_request.target_date+' <br/> <b>Client Priority: </b> '+feature_request.client_priority+' <br/> <b>Product Area:</b> '+feature_request.product_area+' <br /> <b>Description:</b> '+ feature_request.description +' </p>\
                    </div>\
                  </div>');
                }
              });
          } else {
            // If there is no feature request in progress
            $('.in-progress-clients-title').html("No In Progress Approved Feature Requests!");
          }
      });
    }
  });
}

// Ajax call for populating closed approved feature requests
const populateClosedApprovedFeatureRequests = function() {
  // Removing the content in the container
  $('.closed-feature-requests-cont').html("");

  // Ajax call to API
  $.ajax({
    url: '/api/feature-request/approved',
    contentType: 'application/json',
    dataType: 'json',
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    success: function(res) {
        // Looping in the all clients from API
        res.data.map(client => {
          // If there is any approved feature request
          if(client.approved_feature_requests.length > 0) {
              // Looping in all feature requests of all clients
              client.approved_feature_requests.map(feature_request => {
                var badge, acceptBtn;
                if (feature_request.status == "Closed") {
                  badge = '<span style="top: -2px; position:relative;" class="badge badge-danger">Closed</span>';
                  $('.closed-clients-title').hide();
                  $('.closed-feature-requests-cont').prepend('<div class="card mb-4">\
                    <div class="card-header"><h5 style="display:inline">'+ feature_request.title + "</h5> " + badge +'</div> \
                    <div class="card-body">\
                      <p style="margin-bottom: 0px;" class="card-text"><b>Client:</b> '+ client.first_name +' '+client.last_name+' <br /> <b>Company:</b> '+client.company+' <br /> <b>Target Date: </b> '+feature_request.target_date+' <br/> <b>Client Priority: </b> '+feature_request.client_priority+' <br/> <b>Product Area:</b> '+feature_request.product_area+' <br /> <b>Description:</b> '+ feature_request.description +' </p>\
                    </div>\
                  </div>');
                }
              });
          } else {
            // If there is no feature request in progress
            $('.closed-clients-title').html("No Closed Approved Feature Requests!");
          }
      });
    }
  });
}

// populate The main feature requests when clicking on the link
$('.main-feature-requests-link').click(function() {
  // populateMainFeaturesRequests();
  populateApprovedFeatureRequests();
});

// populate in progress feature requests when clicking on the link
$('.in-progress-main-feature-requests-link').click(function() {
  populateInProgressApprovedFeatureRequests();
});

// populate closed feature requests when clicking on the link
$('.closed-main-feature-requests-link').click(function() {
  populateClosedApprovedFeatureRequests();
});

// Adding new approved feature request
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
             title: ko.observable("").extend({required: true, minLength: 10}),
             description: ko.observable("").extend({required: true}),
             clientPriority: ko.observable("").extend({required: true}),
             targetDate: ko.observable("").extend({required: true}),
              submit: function() {
                 if (approvedFeatureRequestViewModel.errors().length === 0) {
                    var jsonData = {
                       public_id: this.clientSelect(),
                       title: this.title(),
                       description: this.description(),
                       client_priority: this.clientPriority(),
                       target_date: this.targetDate(),
                       product_area: this.areaSelect()
                    };

                    $.ajax({
                       method: 'POST',
                       url: '/api/feature-request/admin/add/'+jsonData.public_id,
                       contentType: 'application/json',
                       dataType: 'json',
                       data: JSON.stringify(jsonData),
                       headers: {"x-access-token": localStorage.getItem('token')},
                       success: function(feature_request) {
                         swal("Success!", "Feature Request has been successfully added!", "success")
                          .then(function() {
                            $('#add-approved-feature-request-modal').modal('hide');
                            $('#add-approved-feature-request-form').trigger('reset');

                            populateApprovedFeatureRequests();

                          });
                       }
                    });
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
         swal("Warning!", "You cannot add feature request while there is no active client!", "warning")
          .then(function() {
            $('#add-approved-feature-request-modal').modal('hide');
          });
        }
     }
  });

  $('#add-approved-feature-request-modal').on('hidden.bs.modal', function () {
    $('.validationMessage').hide();
  });

});

// Setting in progress an approved feature request
$('body').on('click', '.mark-in-progress', function() {
  var clientRequestPublicId = $(this).attr('data-requestPublicId');
  swal({
    title: "Are you sure?",
    text: "You want to set this feature request in progress!",
    icon: "info",
    buttons: true
  })
  .then(willApprove => {
    if (willApprove) {
      $(this).parent().parent().fadeOut();
      $.ajax({
        url: '/api/feature-request/progress/'+clientRequestPublicId,
        method: 'PUT',
        contentType: 'application/json',
        headers: {"x-access-token": localStorage.getItem('token')},
        dataType: 'json',
        success: data => {
          if(data.message == 'Feature request successfully set in progress') {
            swal("Success!", "Feature request set in progress!", "success")
            populateInProgressApprovedFeatureRequests();
          }
        }
      });
    } else {
     return false;
    }
  });
});

// Marking as closed an approved feature request
$('body').on('click', '.mark-closed', function() {
  var clientRequestPublicId = $(this).attr('data-requestPublicId');

  swal({
    title: "Are you sure?",
    text: "You want to mark this feature as closed!",
    icon: "info",
    buttons: true
  })
  .then(willApprove => {
    if (willApprove) {
      $(this).parent().parent().fadeOut();
      $.ajax({
        url: '/api/feature-request/close/'+clientRequestPublicId,
        method: 'PUT',
        contentType: 'application/json',
        headers: {"x-access-token": localStorage.getItem('token')},
        dataType: 'json',
        success: data => {
          if(data.message == 'Feature request successfully marked as closed') {
            swal("Success!", "Feature request successfully marked as closed!", "success")
            populateClosedApprovedFeatureRequests();
          }
        }
      });
    } else {
     return false;
    }
  });
});
