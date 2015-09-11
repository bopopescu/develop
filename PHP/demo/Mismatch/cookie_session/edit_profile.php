<?php
	require_once("login.php");
?>
<html>
	<head>
		<title>Edit Page</title>
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
		$id = $row["id"];
		$first_name = $row["first_name"];
		$last_name = $row["last_name"];
		$gender = $row["gender"];
		$birthdate = $row["birthdate"];
		$city = $row["city"];
	}
		?>
		<html>
			<body>
				<h1>Mismatch Edit Profile</h1>
				<form action = "<?php echo $_SERVER['PHP_SELF']?>" method = "POST">
				<strong>id</strong>: <input type = 'text' value = "<?php echo $id;?>"/><br />
				<strong>Username</strong>: <input type = 'text' value = "<?php echo $username;?>" /><br />
				<strong>Firstname</strong>: <input type = 'text' value = "<?php echo $first_name; ?>"/><br />
				<strong>lastname</strong>: <input type = 'text' value = "<?php echo $last_name;?>"/><br />
				<strong>Gender</strong>: <input type = 'text' value = "<?php echo $gender;?>"/><br />
				<strong>Birthdate</strong>: <input type = 'text' value = "<?php echo $birthdate;?>"/><br />
				<strong>City</strong>: <input type = 'text' value = "<?php echo $city;?>"/><br />
				<input type = "submit" name = "submit" value = "Submit">
				</form>
			</body>
		</html>
		
		<?php
		//if ($_SERVER["PHP_AUTH_USER"] == $row["username"]){
		//	echo "<br /><br />Would you like to <a href = 'edit_profile.php?id=$id'>edit your profile</a>?<br />";
		//}
	//}
	
?>