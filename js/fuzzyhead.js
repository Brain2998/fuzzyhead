$(document).ready(function() {
	$("#header").load("header.html");
	var spinner = $('#spinner');
	var fuzzingResult=$("#result");
	var stop=$("#stop");
	
	//Create task page
	if ($('body').hasClass('index')){
		hideSpinner();
		var fuzzer=$("select[name='fuzzer']");
		var target_ip=$("input[name='target_ip']");
		var cli_args=$("input[name='cli_args']")
		createCli();
		$("select[name='fuzzer'], input[name='target_ip']").on('input', function(){
			console.log()
			createCli();
		});
		$('form').submit(function(e) {
			fuzzingResult.empty();
			showSpinner();
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
		        	showResult(statsTemplate(result.match, result.hits, result.done, result.skip, 
		        		result.fail, result.size, result.avg, result.time));
		        },
		        error: function(err){
		        	showResult(`ajax err: ${JSON.stringify(err,null,2)}`);
		        }
	        });
	        e.preventDefault();
		}); 
		function createCli(){
			switch (fuzzer.val()){
				case "dirsearch":
					cli_args.val(`--url ${target_ip.val()} -e html --wordlist=wordlist.txt --simple-report=/dirsearch/result.txt`);
					break;
				case "patator":
					cli_args.val(`ssh_login host=${target_ip.val()} user=victim password=FILE0 0=passwords.txt -x ignore:mesg='Authentication failed.'`)
			}
		}

		function showResult(data){
			fuzzingResult.html(data);
			hideSpinner();
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
		hideSpinner();
		var args=window.location.search;
		var taskId=args.slice(4, args.indexOf('&'));
		getTaskDetails();
		$('#refresh').click(function(){
			getTaskDetails();
		});

		function getTaskDetails(){
			$.ajax({
				async: true,
				type: "GET",
				url: "/getTaskDetails",
				data: {
					id: taskId,
					getDbData: true
				},
				success: function(data){
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
					switch (status)
					{
						case ('Running'):
							showSpinner();
							break;
						case ('Finished'):
							statsResult=JSON.parse(result.result);
						showResult(statsTemplate(statsResult.match, statsResult.hits, statsResult.done, statsResult.skip, 
			        		statsResult.fail, statsResult.size, statsResult.avg, statsResult.time));
							break;
						case ('Failed'):
							break;
					}
					
				},
				error: function(err){
					showResult(`ajax err: ${JSON.stringify(err,null,2)}`);
				}
			});
		}
		function showResult(data){
			fuzzingResult.html(data);
		}
	}
	function showSpinner(){
		spinner.show();
		stop.show();
	}
	function hideSpinner(){
		spinner.hide();
		stop.hide();
	}
	function statsTemplate(match, hits, done, skip, fail, size, avg, time){
		return `<tr>
		<td><label>Matches: </label></td>
		<td><label>${match}</label></td>
		</tr>
		<tr>
		<td><label>Hits: </label></td>
		<td><label>${hits==undefined ? '' : hits}</label></td>
		</tr>
		<tr>
		<td><label>Done: </label></td>
		<td><label>${done==undefined ? '' : done}</label></td>
		</tr>
		<tr>
		<td><label>Skip: </label></td>
		<td><label>${skip==undefined ? '' : skip}</label></td>
		</tr>
		<tr>
		<td><label>Fail: </label></td>
		<td><label>${fail==undefined ? '' : fail}</label></td>
		</tr>
		<tr>
		<td><label>Size: </label></td>
		<td><label>${size==undefined ? '' : size}</label></td>
		</tr>
		<tr>
		<td><label>Average requests/second: </label></td>
		<td><label>${avg==undefined ? '' : avg}</label></td>
		</tr>
		<tr>
		<td><label>Fuzzing time: </label></td>
		<td><label>${time}</label></td>
		</tr>`;
	}
});

