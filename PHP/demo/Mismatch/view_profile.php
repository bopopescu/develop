<?php
	require_once("login.php");

	//start sessin
	require_once("startsession.php");

	require_once("connectvars.php");
	
	//insert the page header
	$page_title = "View Profile";
	require_once("header.php");
	
	//show the nav enu
	require_once("navmenu.php");
?>


<?php
	if (isset($_GET["id"])){
		$id = $_GET["id"];
		$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die(mysqli_error());
		$query = "select * from mismatch_user where id = $id";
		$result = mysqli_query($dbc,$query) or die(mysqli_error());
		mysqli_close($dbc);	
		$row = mysqli_fetch_array($result);
		echo "<h2>Current user details</h2><br />";
		echo "<strong>id</strong>: ",$row["id"]."<br />";
		echo "<strong>Username</strong>: ",$row["username"]."<br />";
		echo "<strong>Firstname</strong>: ",$row["first_name"]."<br />";
		echo "<strong>lastname</strong>: ",$row["last_name"]."<br />";
		echo "<strong>Gender</strong>: ",$row["gender"]."<br />";
		echo "<strong>Birthdate</strong>: ",$row["birthdate"]."<br />";
		echo "<strong>City</strong>: ",$row["city"]."<br />";
		//if ($_SERVER["PHP_AUTH_USER"] == $row["username"]){
		if (($_SESSION["username"] == $row["username"]) || ($_COOKIE["username"] == $row["username"])){
			echo "<br /><br />Would you like to <a href = 'edit_profile.php?id=$id'>edit your profile</a>?<br />";

		}
	}
	
?>

<?php
	require_once("footer.php");
?>