
$(document).ready(function() {
	// bind event handlers
	$('#acc_upload').on('submit', {action: "upload_accessions"}, on_submit);
	$('#plant_upload').on('submit', {action: "upload_plants"}, on_submit);
	$('#create_db').on('submit', {action: "admin_create"}, on_submit);
    });


// submit event handler for admin POST
function on_submit(event) {
    event.preventDefault();
    filename = $(event.target).find('input').filter('[type="file"]').val();
    form_data = new FormData(event.target);
    form_data.append('file', filename);
    $.ajax({
	url: /admin'',
	data: form_data,
	cache: false,
	contentType: false,
	processData: false,
	type: 'POST',
	success: function(data){
            alert(data);
	}
    });
}