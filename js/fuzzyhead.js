$(document).ready(function() {
	var spinner = $('#spinner');
	spinner.hide();
	$('form').submit(function(e) {
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
	          $("#result").html(data);
	          spinner.hide();
	        },
	        error: function(err){
	        	console.log(`ajax err: ${JSON.stringify(err,null,2)}`)
	        	spinner.hide();
	        }
        });
        e.preventDefault();
	}); 
});