// this document.ready() should only be called on the main.tpl
$(document).ready(function() {
	// bind event handlers
	$('#show-dead').on("onclick", show_dead);
    });

function show_dead(event) {
    //alert('show dead');
    $("div.dead").each(function (index, el) {
	    //alert(el);
	    $(el).css("display", "block");
	});
    $("#show-dead").css("display", "none");
}