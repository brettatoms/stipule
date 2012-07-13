
$(document).ready(function() {
	// bind event handlers
	$('#acc_upload').on('submit', {action: "upload_accessions"}, on_submit);
	$('#plant_upload').on('submit', {action: "upload_plants"}, on_submit);
	$('#create_db').on('submit', {action: "admin_create"}, on_submit);
    });


// submit event handler for admin POST
function on_submit(event) {
    event.preventDefault();
    $.post('/admin', event.data,
	   function (data) {
	       $('#message').html(data).fadeIn();
	   });
}