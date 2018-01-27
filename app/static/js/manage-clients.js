// Populating Pending Clients Table
$('.manage-clients-link, .pending-clients-link').click(function() {
   $('.pending-clients-table').html("");
   $.ajax({
      url: '/api/user/',
      method: 'GET',
      contentType: 'application/json',
      data: { role: 'client', status: 'False' },
      headers: {"x-access-token": localStorage.getItem('token')},
      success: function(res) {
         if (res != '') {
            $('.pending-clients-title').html("Pending Clients Table");
            $('.pending-clients-table').parent().show();
            res.map(client => {
               $('.pending-clients-table').append("<tr>\
               <td>"+ client.first_name +"</td>\
               <td>"+ client.last_name +"</td>\
               <td>"+ client.username +"</td>\
               <td>"+ client.email_address +"</td>\
               <td>"+ client.company +"</td>\
               <td><button type='button' id='approve-client' data-publicId="+client.public_id+" class='btn btn-info btn-sm'>Approve</button></td>\
               </tr>");
            });
         } else {
            $('.pending-clients-title').html("No Pending Clients");
            $('.pending-clients-table').parent().hide();
         }
      }
   });
});

// Populating Active Clients Table
$('.active-clients-link').click(function() {
   $('.active-clients-table').html("");
   $.ajax({
      url: '/api/user/',
      method: 'GET',
      contentType: 'application/json',
      data: { role: 'client', status: 'True' },
      headers: {"x-access-token": localStorage.getItem('token')},
      success: function(res) {
         if (res != '') {
            $('.active-clients-title').html("Active Clients Table");
            $('.active-clients-table').parent().show();
            res.map(user => {
               $('.active-clients-table').append("<tr>\
               <td>"+ user.first_name +"</td>\
               <td>"+ user.last_name +"</td>\
               <td>"+ user.username +"</td>\
               <td>"+ user.email_address +"</td>\
               <td>"+ user.company +"</td>\
               </tr>");
            });
         } else {
            $('.active-clients-title').html("No Active Clients");
            $('.active-clients-table').parent().hide();
         }
      }
   });
});

// Approving Clients
$(document).on("click", "#approve-client", function(){
   var userPublicId = $(this).attr('data-publicId');

   swal({
     title: "Are you sure?",
     text: "You want to approve as active this client!",
     icon: "info",
     buttons: true
   })
   .then(willApprove => {
     if (willApprove) {
      $(this).parent().parent().remove();
      var countRows = $('.pending-clients-table tr').length;
      if (countRows == 0) {
         $('.pending-clients-title').html("No Pending Clients");
         $('.pending-clients-table').parent().hide();
      }
      $.ajax({
         url: "/api/user/activate/"+userPublicId,
         method: "PUT",
         contentType: 'application/json',
         headers: {"x-access-token": localStorage.getItem('token')},
         success: function(res) {
            if(res.message == "The user has been activated!") {
               swal("Success!", "This client is approved!", "success")
            }
         }
      })

     } else {
      return false;
     }
   });
});
