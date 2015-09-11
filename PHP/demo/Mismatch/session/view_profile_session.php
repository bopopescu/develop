<?php
	require_once("login.php");
?>
<html>
	<head>
		<title>View Page</title>
	</head>
</html>
<?php
	require_once("connectvars.php");
	if (isset($_GET["id"])){
		$id = $_GET["id"];
		$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
		$query = "select * from mismatch_user where id = $id";
		$result = mysqli_query($dbc,$query) or die("query mysql error");
		mysqli_close($dbc);	
		$row = mysqli_fetch_array($result);
		echo "<h1>Mismatch View Profile</h1>";
		echo "<strong>id</strong>: ",$row["id"]."<br />";
		echo "<strong>Username</strong>: ",$row["username"]."<br />";
		echo "<strong>Firstname</strong>: ",$row["first_name"]."<br />";
		echo "<strong>lastname</strong>: ",$row["last_name"]."<br />";
		echo "<strong>Gender</strong>: ",$row["gender"]."<br />";
		echo "<strong>Birthdate</strong>: ",$row["birthdate"]."<br />";
		echo "<strong>City</strong>: ",$row["city"]."<br />";
		//if ($_SERVER["PHP_AUTH_USER"] == $row["username"]){
		if ($_SESSION["username"] == $row["username"]){
			echo "<br /><br />Would you like to <a href = 'edit_profile.php?id=$id'>edit your profile</a>?<br />";

		}
	}
	
?>