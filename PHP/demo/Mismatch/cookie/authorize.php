<?php
    if(!isset($_SERVER["PHP_AUTH_USER"]) || !isset($_SERVER["PHP_AUTH_PW"])){
		header("HTTP/1.1 401 Unauthorized");
		header('WWW-Authenticate:Basic realm = "Mismatch"');
		exit("<h2>Mismatch</h2>Sorry,you must enter your username and password to login and access this page!
		If you are not a registered user,please <a href = 'signup.php'>sign up</a>");
	}
?>