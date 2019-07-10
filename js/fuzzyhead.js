$(document).ready(function() {
	$("#header").load("header.html");
	if ($('body').hasClass('index')){
		var spinner = $('#spinner');
		spinner.hide();
		$('form').submit(function(e) {
			$("#result").empty();
			spinner.show();
			$.ajax({
				async: true,
		        type: "POST",
		        url: "/", 
		        data: new FormData($('form')[0]), 
		        cache: false,
			    contentType: false,
			    processData: false,
		        success: function(data)
		        {
		        	var result = JSON.parse(data);
		        	var htmlResult='';
		        	htmlResult += '<tr>';
	        		htmlResult += '<td><label>Matches: </label></td>';
	        		htmlResult += '<td><label>'+result.match+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Hits: </label></td>';
	        		htmlResult += '<td><label>'+(result.hits==undefined ? '' : result.hits)+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Done: </label></td>';
	        		htmlResult += '<td><label>'+(result.done==undefined ? '' : result.done)+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Skip: </label></td>';
	        		htmlResult += '<td><label>'+(result.skip==undefined ? '' : result.skip)+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Fail: </label></td>';
	        		htmlResult += '<td><label>'+(result.fail==undefined ? '' : result.fail)+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Size: </label></td>';
	        		htmlResult += '<td><label>'+(result.size==undefined ? '' : result.size)+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Average requests/second: </label></td>';
	        		htmlResult += '<td><label>'+(result.avg==undefined ? '' : result.avg)+'</label></td>';
	        		htmlResult += '</tr>';
	        		htmlResult += '<tr>';
	        		htmlResult += '<td><label>Fuzzing time: </label></td>';
	        		htmlResult += '<td><label>'+result.time+'</label></td>';
	        		htmlResult += '</tr>';
		        	showResult(htmlResult);
		        },
		        error: function(err){
		        	showResult(`ajax err: ${JSON.stringify(err,null,2)}`);
		        }
	        });
	        e.preventDefault();
		}); 
		function showResult(data){
			$("#result").html(data);
			spinner.hide();
		}
	}
	if ($('body').hasClass('list')){
	}
});

