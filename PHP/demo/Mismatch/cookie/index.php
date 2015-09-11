<html>
	<head>
		<title>Main Page</title>
	</head>

	<body>
	<h1 align = 'center'>Main Page</h1>
	<?php
	//if (!isset($_COOKIE['id'])){
	//if (empty($_COOKIE['id'])){
	if (empty($_COOKIE['username'])){
		echo '<p><a href = "signup.php">Sign Up</a>&nbsp;&nbsp;<a href = "login.php">Log in</a></p>';
	}
	else{
		echo "Welcome " . $_COOKIE["username"] . "&nbsp;||&nbsp;<a href = 'logout.php'>Logout(" . $_COOKIE['username'] . ")</a><br /><br />";
		//echo "<a href = 'edit_profile.php?id=" . $_COOKIE["id"] . "'>Edit Profile</a>";
		$id = $_COOKIE["id"];
		echo "<a href = 'edit_profile.php?id=$id'>Edit Profile</a>";
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
		echo "<a href = 'view_profile.php?id=$id'>".$username."</a><br /><br />";
	}	
?>
	</body>
	<script>
function out(count){
	for(var i=0;i<count;i++){
		alert(i);
	}
	var i;
	alert(i)
};
//out(5);

	</script>
</html>
