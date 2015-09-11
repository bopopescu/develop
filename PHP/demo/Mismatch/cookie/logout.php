<?php
	if (isset($_COOKIE["id"])){
		//delete id and username cookies by setting their expirations to an hour ago
		setcookie("id","",time() - 3600);
		setcookie("username", "",time() - 3600);
		//$home_url = "http://" . $_SERVER["HTTP_POST"] . dirname($_SERVER["PHP_SELF"]) . "/index.php";
		
	}
	//redirect to the home page
	$home_url = "http://10.10.2.11/mismatch/index.php";
	header("Location: " . $home_url);
?>