var spinner = $('#spinner');
$(document).ready(function() {
	spinner.hide();
	$('form').submit(function(e) {
		$("#result").empty();
		spinner.show();
		$.ajax({
	        type: "POST",
	        url: "/", 
	        data: new FormData($('form')[0]), 
	        cache: false,
		    contentType: false,
		    processData: false,
	        success: function(data)
	        {
	        	result(data)
	        },
	        error: function(err){
	        	result(`ajax err: ${JSON.stringify(err,null,2)}`);
	        }
        });
        e.preventDefault();
	}); 
});

function result(data){
	$("#result").html(data);
	spinner.hide();
}