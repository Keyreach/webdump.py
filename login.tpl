<!doctype html>
<meta charset='utf-8' />
<title>Authorization required</title>
<style>
html, body {
	width: 100%;
	height: 100%;
	background: #CCC;
	margin: 0;
	font: 400 10pt "Open Sans", "Segoe UI", "Liberation Sans", sans-serif;
}
.wrapper {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100%;
}
.loginform {
	background: #FFF;
	color: #444;
	padding: 16px;
	width: 240px;
}
.loginform > input {
	display: block;
	padding: 8px;
	border: 1px solid #CCC;
	background: #EEE;
	margin-bottom: 16px;
	width: 100%;
	box-sizing: border-box;
	text-align: center;
}
.loginform > button {
	background: #777;
	border: 1px solid #333;
	color: #FFF;
	padding: 8px;
	display: block;
	width: 100%;
	max-width: 320px;
	margin: 0 auto;
	font-family: inherit;
}
</style>
<div class='wrapper'>
	<form action='{{ docroot }}/do/login' method='POST'>
	<div class='loginform'>
		<div>Authentication required</div>
		<input type='password' id='passphrase' name='pass' autofocus>
		<button type='submit'>Login</button>
	</div>
	</form>
</div>