$('.feature-requests-link').click(function() {

  $('.client-feature-requests-cont').html("");
  $.ajax({
    url: '/api/feature-request/clients',
    contentType: 'application/json',
    dataType: 'json',
    method: 'GET',
    headers: {"x-access-token": localStorage.getItem('token')},
    success: function(res) {
      if (res.data.length > 0) {

        res.data.map(client => {

          client.feature_requests.map(feature_request => {

          var badge, acceptBtn;
          if (feature_request.status == "Pending") {
            badge = '<span style="top: -2px; position:relative;" id="badge-'+feature_request.public_id+'" class="badge badge-warning">Pending</span>';
            acceptBtn = '<button data-requestPublicId='+feature_request.public_id+' class="btn btn-sm btn-link float-right mark-accepted">Mark as Accepted</button>';
          } else {
            badge = '<span class="badge badge-success">Accepted</span>';
            acceptBtn = ''
          }

          $('.feature-clients-title').hide();
          $('.client-feature-requests-cont').prepend('<div class="card mb-4">\
            <div class="card-header"><h5 style="display:inline">'+ feature_request.subject + "</h5> " + badge +' '+ acceptBtn +'</div> \
            <div class="card-body">\
              <p style="margin-bottom: 0px;" class="card-text"><b>Client:</b> '+ client.first_name +' '+client.last_name+' <br /> <b>Company:</b> '+client.company+' <br /> <b>Description:</b> '+ feature_request.description +'</p>\
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


$('body').on('click', '.mark-accepted', function() {
  var clientRequestPublicId = $(this).attr('data-requestPublicId');

  swal({
    title: "Are you sure?",
    text: "You want to accept this feature request of this client!",
    icon: "info",
    buttons: true
  })
  .then(willApprove => {
    if (willApprove) {
      $(this).fadeOut();
      $('#badge-'+clientRequestPublicId).removeClass('badge-warning').addClass("badge-success").text("Accepted");
      $.ajax({
        url: '/api/feature-request/accept/'+clientRequestPublicId,
        method: 'PUT',
        contentType: 'application/json',
        headers: {"x-access-token": localStorage.getItem('token')},
        dataType: 'json',
        success: data => {
          if(data.message == 'Client request successfully accepted') {
            $(this).fadeOut();
            swal("Success!", "Client feature request accepted!", "success")
          }
        }
      });

    } else {
     return false;
    }
  });


});


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
                        '+ data.message +'\
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
            userType = '(Client)';
          } else {
            floatSide = 'float-right';
            bgColor = 'message-admin';
            userType = '';
          }

          $('#messages-'+correspondence_id).append('<div class="message-wrapper"><div class="message '+floatSide+' '+bgColor+'">\
            <p><b>'+ message.user_first_name + ' ' + message.user_last_name + ' ' + userType +'</b></p>\
            '+ message.message +' <br/>  <span style="font-size: 9px;float:right;">'+message.created_date+'</span>\
          </div></div>')

        });
      }
    }
  });

});
