<?php
	//header("Location:http://www.baidu.com");
	//header("Refresh: 3; url=http://www.baidu.com");
	$username = "xdd";
	$password = "123";
	if (!isset($_SERVER["PHP_AUTH_USER"]) || !isset($_SERVER["PHP_AUTH_PW"]) || ($_SERVER["PHP_AUTH_USER"] != $username) || ($_SERVER["PHP_AUTH_PW"] != $password)){
		header("HTTP/1.1 401 Unauthorized");
		header('WWW-Authenticate:Basic realm = "Guitar wars"');
		exit("<h2>Guitar wars</h2>Sorry,you must enter a valid user name and password to access this page!");
	}
?>