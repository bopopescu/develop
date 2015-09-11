<?php
	//generate the nav menu
	echo "<hr />";
	if (!isset($_SESSION["username"])){
		echo '<p>&#10084; <a href = "signup.php">Sign Up</a>&nbsp;&nbsp;&#10084; <a href = "login.php">Log in</a></p>';
	}
	else{
		echo "&#10084; Welcome " . $_SESSION["username"] . "&nbsp;||&nbsp;<a href = 'logout.php'>Logout(" . $_SESSION["username"] . ")</a><br />";
		$id = $_SESSION["id"];
		echo "&#10084; <a href = 'index.php'>Home Page</a><br />";
		echo "&#10084; <a href = 'view_profile.php?id=" . $_SESSION["id"] . "'>View Profile</a><br />";
		echo "&#10084; <a href = 'edit_profile.php?id=$id'>Edit Profile</a><br />";
		echo "&#10084; <a href = 'questionnaire.php'>Questionnaire</a><br />";
		echo "&#10084; <a href = 'mymismatch.php'>MyMismatch</a><br />";
	}
	echo "<hr />";
?>