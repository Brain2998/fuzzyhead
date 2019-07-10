$(document).ready(function() {
	$("#header").load("header.html");
	if ($('body').hasClass('index')){
		var spinner = $('#spinner');
		var fuzzingResult=$("#result");
		spinner.hide();
		$('form').submit(function(e) {
			fuzzingResult.empty();
			spinner.show();
			$.ajax({
				async: true,
		        type: "POST",
		        url: "/", 
		        data: new FormData($('form')[0]), 
		        cache: false,
			    contentType: false,
			    processData: false,
		        success: function(data){
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
			fuzzingResult.html(data);
			spinner.hide();
		}
	}
	if ($('body').hasClass('list')){
		var taskList=$('#task_list tr:last');
		$.ajax({
			async: true,
			type: "GET",
			url: "/getTaskList",
			data: {
				getDbData: true
			},
			success: function(data){
				var result = JSON.parse(data);
		        var htmlResult='';
		        console.log(result)
		        for (var i=0; i<result.length; ++i){
		        	htmlResult+='<tr>';
		        	htmlResult+='<td><label>'+result[i][1]+'</label></td>';
		        	htmlResult+='<td><label>'+result[i][0]+'</label></td>';
		        	htmlResult+='<td><label>'+result[i][2]+'</label></td>';
		        	htmlResult+='</tr>';
		        }
				showResult(htmlResult);
			},
			error: function(err){
				showResult(`ajax err: ${JSON.stringify(err,null,2)}`);
			}
		});
		function showResult(data){
			taskList.after(data);
		}
	}
});

