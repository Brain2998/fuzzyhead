var spinner = $('#spinner');
$(document).ready(function() {
	spinner.hide();
	$('form').submit(function(e) {
		spinner.show();
	});
});
/*$(function() {
  $('form').submit(function(e) {
    e.preventDefault();
    spinner.show();
    $.ajax({
      url: 't2228.php',
      data: $(this).serialize(),
      method: 'post',
      dataType: 'JSON'
    }).done(function(resp) {
      spinner.hide();
      alert(resp.status);
    });
  });
});*/