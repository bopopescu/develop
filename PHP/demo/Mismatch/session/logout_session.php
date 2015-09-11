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
	//redirect to the home page
	//$home_url = "http://" . $_SERVER["HTTP_POST"] . dirname($_SERVER["PHP_SELF"]) . "/index.php";
	$home_url = "http://10.10.2.11/mismatch/index.php";
	header("Location: " . $home_url);
?>