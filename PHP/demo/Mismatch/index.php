<?php
	//start session
	require_once("startsession.php");

	//insert the page header
	$page_title = "Home Page";
	require_once("header.php");
	
	//require_once("appvars.php");
	require_once("connectvars.php");
	
	//show the nav menu
	require_once("navmenu.php");
?>

<?php
	//connect to the database
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die(mysqli_error());
	$query = "select * from mismatch_user";
	$result = mysqli_query($dbc,$query) or die(mysqli_error());
	mysqli_close($dbc);
	
	echo "<h2>Last members</h2>";
	
	while ($row = mysqli_fetch_array($result)){
		$id = $row["id"];
		$username = $row["username"];
		if (isset($_SESSION["id"])){
			echo "<a href = 'view_profile.php?id=$id'>" . $username . "<a><br /><br />";
		}
		else{
			echo $username . "<br /><br />";
		}
	}
?>

<?php	
	//insert the page footer
	require_once("footer.php");
?>