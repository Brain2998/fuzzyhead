$(document).ready(function() {
	$("#header").load("header.html");
	//Create task page
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
	//Task list page
	if ($('body').hasClass('list')){
		var taskList=$('#task_list tr:last');
		getTaskList();
		$('#refresh').click(function(){
			getTaskList();
		});
		function getTaskList(){
			$('#task_list tr:gt(0)').empty();
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
			        for (var i=0; i<result.length; ++i){
			        	htmlResult+='<tr>';
			        	htmlResult+='<td><label>'+result[i].started_at+'</label></td>';
			        	htmlResult+='<td><label>'+result[i].name+'</label></td>';
			        	htmlResult+='<td><label>'+result[i].status+'</label></td>';
			        	htmlResult+="<td><a href=\"/getTaskDetails?id="+result[i].name+'_'+result[i].started_at+"&getDbData=false\" class=\"btn btn-default\">Details</a></td>";
			        	htmlResult+='</tr>';
			        }
					showResult(htmlResult);
				},
				error: function(err){
					showResult(`ajax err: ${JSON.stringify(err,null,2)}`);
				}
			});
		}
		function showResult(data){
			taskList.after(data);
		}
	}
	//Task details page
	if ($('body').hasClass('details')){
		var spinner = $('#spinner');
		var fuzzingResult=$("#result");
		spinner.hide();
		var args=window.location.search;
		var taskId=args.slice(4, args.indexOf('&'));
		$.ajax({
			async: true,
			type: "GET",
			url: "/getTaskDetails",
			data: {
				id: taskId,
				getDbData: true
			},
			success: function(data){
				console.log(data)
				result=JSON.parse(data);
				$('#name').text(result.name);
				$('#started_at').text(result.started_at);
				$('#fuzzer').text(result.fuzzer);
				$('#target_ip').text(result.target_ip);
				$('#dict').text(result.dict);
				$('#divide_number').text(result.divide_number);
				$('#cli_args').text(result.cli_args);
				var status=result.status;
				$('#status').text(status);
				if (status=='Running'){
					spinner.show();
				}
				else {
					showResult(result.result)
				}
			},
			error: function(err){
				showResult(`ajax err: ${JSON.stringify(err,null,2)}`);
			}
		});
		function showResult(data){
			fuzzingResult.html(data);
		}
	}
});

