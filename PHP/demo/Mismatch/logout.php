<?php
    session_start();
	if (isset($_SESSION["id"])){
		//clear session array
		$_SESSION = array();
		//delete cookie if exists!
		if(isset($_COOKIE[session_name()])){
			setcookie(session_name(),"",time() - 3600);
		}
		//destroy session
		session_destroy();		
	}
	
	if (isset($_COOKIE["id"])){
		//delete the user id and username cookies by setting their expirations to an hour ago
		setcookie("id", "", time() - 3600);
		setcookie("username","", time() - 3600);
	}
	//redirect to the home page
	//$home_url = "http://" . $_SERVER["HTTP_POST"] . dirname($_SERVER["PHP_SELF"]) . "/index.php";
	$home_url = "http://10.10.2.11/mismatch/index.php";
	header("Location: " . $home_url);
?>