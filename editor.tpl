<!doctype html>
<html>
<head>
<meta charset='utf-8' />
<title>webdumpy - edit {{ filename }}</title>
<link rel='stylesheet' href='/res/webdumpy.css' type='text/css'>
<script>
function SaveAs(){
 var NameIn = document.getElementsByName('filename')[0];
 var name = prompt('Enter filename', NameIn.value);
 if(name.trim() != ''){ 
  NameIn.value = name;
  document.forms[0].submit();
 }
}
</script>
</head>
<body>
<form action='{{ docroot }}/do/update' method='POST'>
<div class='layout-bar layout-bar_regular'>
	<div class='layout-bar__fixed'>
		<a href='{{ docroot }}/' class='form-button form-button_regular'>&laquo; back</a>
		<input type='submit' class='form-button form-button_regular' value='Save'>
		<input type='button' class='form-button form-button_regular' value='Save As' onclick='SaveAs()'>
		<input type='hidden' value='{{ filename }}' name='filename'>
	</div>
	<div class='layout-bar__fluid'>
	</div>
	<div class='layout-bar__fixed'>
		{{ filename }}
	</div>
</div>
<div>
<textarea name='text' spellcheck="false">{{ data }}</textarea>
</div>
</form>
</body>
</html>
