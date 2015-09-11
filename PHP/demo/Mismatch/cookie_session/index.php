<html>
	<head>
		<title>Main Page</title>
	</head>

	<body>
	<h1 align = 'center'>Main Page</h1>
	<h1>Mismatch Home Page</h1>
	<?php
	//if (!isset($_SESSION['id'])){
	//if (empty($_SESSION['id'])){
	session_start();
	//if the session is not set, try to set them with a cookie
	if (!isset($_SESSION["id"])){
		if (isset($_COOKIE["id"]) && isset($_COOKIE["username"])){
			$_SESSION["id"] = $_COOKIE["id"];
			$_SESSION["username"] = $_COOKIE["username"];
		}
	}

	if (empty($_SESSION['username'])){
		echo '<p>&#10084; <a href = "signup.php">Sign Up</a>&nbsp;&nbsp;&#10084; <a href = "login.php">Log in</a></p>';
	}
	else{
		echo "&#10084; Welcome " . $_SESSION["username"] . "&nbsp;||&nbsp;<a href = 'logout.php'>Logout(" . $_SESSION['username'] . ")</a><br />";
		//echo "<a href = 'edit_profile.php?id=" . $_SESSION["id"] . "'>Edit Profile</a>";
		$id = $_SESSION["id"];
		echo "&#10084; <a href = 'view_profile.php?id=".$_SESSION["id"]."'>View Profile</a><br />";
		echo "&#10084; <a href = 'edit_profile.php?id=$id'>Edit Profile</a><br />";
	}
	
	?>
	<h1>Last members</h1>
	<hr />
<?php
	require_once("connectvars.php");
	//connect to the database
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
	$query = "select * from mismatch_user";
	$result = mysqli_query($dbc,$query);
	mysqli_close($dbc);
	
	while ($row = mysqli_fetch_array($result)){
		$id = $row["id"];
		$username = $row["username"];
		if (isset($_SESSION["id"])){
			echo "<a href = 'view_profile.php?id=$id'>".$username."</a><br /><br />";
		}
		else{
			echo $username."<br /><br />";
		}
		
	}	
?>
	</body>
	<script>
function out(count){
	for(var i=0;i<count;i++){
		alert(i);
	}
	var i;
	alert(i);
};
//out(5);

	</script>
</html>



<?php
 for($index = 0; $index <1; ++$index)
 {
	//echo $index; 
?>
   //<br />
<?php

 }
?>

