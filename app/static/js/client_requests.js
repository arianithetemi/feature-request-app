$('.feature-requests-link').click(function() {

  $('.client-feature-requests-cont').html("");
  $.ajax({
    url: '/api/feature-request/client',
    contentType: 'application/json',
    dataType: 'json',
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    success: function(res) {
      if (res.data.length > 0) {
        res.data.map(feature_request => {

          var badge;
          if (feature_request.status == "Pending") {
            badge = '<span class="badge badge-warning">Pending</span>';
          } else {
            badge = '<span class="badge badge-success">Accepted</span>';
          }

          $('.feature-clients-title').hide();
          $('.client-feature-requests-cont').prepend('<div class="card mb-4">\
            <h5 class="card-header">'+ feature_request.subject + " " + badge +'</h5> \
            <div class="card-body">\
              <p class="card-text">'+ feature_request.description +'</p>\
              <button type="button" data-toggle="collapse" data-target="#'+feature_request.correspondence+'" data-correspondence='+feature_request.correspondence+' class="btn open-conversation btn-sm btn-secondary float-right">Open Conversation</button>\
            </div>\
            <div class="collapse" id="'+ feature_request.correspondence +'">\
            <hr />\
              <div class="messaging-container" style="padding: 1.25rem;">\
                <div class="messages" id="messages-'+feature_request.correspondence+'">\
                </div>\
                <form id="'+ feature_request.correspondence +'-message-form" class="text-right">\
                  <div class="form-group">\
                     <textarea class="form-control" required="" placeholder="Write a message" data-bind="textInput: message" rows="2"></textarea>\
                  </div>\
                  <button type="submit" data-bind="click: submit" class="btn btn-primary">Send</button>\
                </form>\
              </div>\
            </div>\
          </div>');
        });
      } else {
        $('.feature-clients-title').html("No Feature Requests!");
      }
    }
  });
});

ko.validation.rules.pattern.message = 'Invalid.';
ko.validation.init({
    registerExtenders: true,
    messagesOnModified: true,
    insertMessages: true,
    parseInputAttributes: true,
    messageTemplate: null
}, true);

$('body').on('click', '.close-conversation', function(){
  var correspondence_id = $(this).data('correspondence');
  $(this).removeClass('close-conversation').addClass('open-conversation').text('Open Conversation');

  // setTimeout(function(){
  $('#messages-'+correspondence_id).html("");
  // }, 700);
})


$('body').on('click', '.open-conversation', function(){
  var correspondence_id = $(this).data('correspondence');

  $(this).removeClass('open-conversation').addClass('close-conversation').text("Close Conversation");

  ko.cleanNode(document.getElementById(correspondence_id+'-message-form'));
  // New message View Modal
  var messageViewModel = {
     message: ko.observable("").extend({required: true}),
     submit: function() {
        if (messageViewModel.errors().length === 0) {
           var jsonData = {
              message: this.message()
           };

           $.ajax({
              method: 'POST',
              url: '/api/feature-request/add/message/'+correspondence_id,
              contentType: 'application/json',
              dataType: 'json',
              data: JSON.stringify(jsonData),
              headers: {"x-access-token": localStorage.getItem('token')},
              success: function(data) {
                swal("Success!", "Message sent!", "success")
                   .then(function() {
                      $('#'+correspondence_id+'-message-form').trigger('reset');

                      $('#messages-'+correspondence_id).find('.no-messages').remove();

                      var floatSide, bgColor;
                      if (data.user_role == 'client') {
                        floatSide = 'float-left';
                        bgColor = 'message-client';
                      } else {
                        floatSide = 'float-right';
                        bgColor = 'message-admin';
                      }

                      $('#messages-'+correspondence_id).append('<div class="message-wrapper"><div class="message '+floatSide+' '+bgColor+'">\
                        <p><b>'+ data.user_first_name + ' ' + data.user_last_name +'</b></p>\
                        '+ data.message +' <br/>  <span style="font-size: 9px;float:right;">'+data.created_date+'</span>\
                      </div></div>')
                    });
               }
           })
        }
        else {
           messageViewModel.errors.showAllMessages();
        }
     }
  };

  messageViewModel.errors = ko.validation.group(messageViewModel);

  messageViewModel.requireLocation = function() {
     messageViewModel.location.extend({required: true});
  };

  ko.applyBindings(messageViewModel, document.getElementById(correspondence_id+'-message-form'));

  $.ajax({
    url: '/api/feature-request/messages/'+correspondence_id,
    contentType: 'application/json',
    dataType: 'json',
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    success: function(res) {
      if(res.messages.length == 0) {
        $('#messages-'+correspondence_id).html("<h3 style='margin-top: 0px' class='title no-messages text-center'>No Messages</h3>")
      } else {
        res.messages.map(message => {

          $('#messages-'+correspondence_id).find('.no-messages').remove();
          var floatSide, bgColor, userType;
          if (message.user_role == 'client') {
            floatSide = 'float-left';
            bgColor = 'message-client';
            userType = '';
          } else {
            floatSide = 'float-right';
            bgColor = 'message-admin';
            userType = '(Staff)'
          }

          $('#messages-'+correspondence_id).append('<div class="message-wrapper"><div class="message '+floatSide+' '+bgColor+'">\
            <p><b>'+ message.user_first_name + ' ' + message.user_last_name + userType +'</b></p>\
            '+ message.message +' <br/>  <span style="font-size: 9px;float:right;">'+message.created_date+'</span>\
          </div></div>')

        });
      }
    }
  });

});


// Client feature request View Modal
var addFeatureRequestViewModel = {
   subject: ko.observable("").extend({required: true}),
   description: ko.observable("").extend({required: true}),
   submit: function() {
      if (addFeatureRequestViewModel.errors().length === 0) {
         var jsonData = {
            subject: this.subject(),
            description: this.description()
         };

         $.ajax({
            method: 'POST',
            url: '/api/feature-request/client/add',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(jsonData),
            headers: {"x-access-token": localStorage.getItem('token')},
            success: function(feature_request) {
              swal("Success!", "Feature request has been successfully saved!", "success")
                 .then(function() {
                    $('#add-feature-request-modal').modal('hide');
                    $('#add-feature-request-form').trigger('reset');

                    var badge;
                    if (feature_request.status == "Pending") {
                      badge = '<span class="badge badge-warning">Pending</span>';
                    } else {
                      badge = '<span class="badge badge-success">Approved</span>';
                    }

                    $('.feature-clients-title').hide();
                    $('.client-feature-requests-cont').prepend('<div class="card mb-4">\
                      <h5 class="card-header">'+ feature_request.subject + " " + badge +'</h5> \
                      <div class="card-body">\
                        <p class="card-text">'+ feature_request.description +'</p>\
                        <button type="button" data-toggle="collapse" data-target="#'+feature_request.correspondence+'" data-correspondence='+feature_request.correspondence+' class="btn open-conversation btn-sm btn-secondary float-right">Open Conversation</button>\
                      </div>\
                      <div class="collapse" id="'+ feature_request.correspondence +'">\
                      <hr />\
                        <div class="messaging-container" style="padding: 1.25rem;">\
                          <div class="messages" id="messages-'+feature_request.correspondence+'">\
                          </div>\
                          <form id="'+ feature_request.correspondence +'-message-form" class="text-right">\
                            <div class="form-group">\
                               <textarea class="form-control" required="" placeholder="Write a message" data-bind="textInput: message" rows="2"></textarea>\
                            </div>\
                            <button type="submit" data-bind="click: submit" class="btn btn-primary">Send</button>\
                          </form>\
                        </div>\
                      </div>\
                    </div>');



                  });
             }
         })
      }
      else {
         addFeatureRequestViewModel.errors.showAllMessages();
      }
   }
};

addFeatureRequestViewModel.errors = ko.validation.group(addFeatureRequestViewModel);

addFeatureRequestViewModel.requireLocation = function() {
   addFeatureRequestViewModel.location.extend({required: true});
};

ko.applyBindings(addFeatureRequestViewModel, document.getElementById('add-feature-request-form'));
