<?php
	//require_once("appvars.php");
	require_once("connectvars.php");
	//connect to the database
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die(mysqli_error());
	if (isset($_POST["submit"])){
		$username = mysqli_real_escape_string($dbc,$_POST["username"]);
		$password1 = mysqli_real_escape_string($dbc,$_POST["password1"]);
		$password2 = mysqli_real_escape_string($dbc,$_POST["password2"]);
		if (!empty($username) && !empty($password1) && !empty($password2) && ($password1 == $password2)){
			//make sure nobody registered this username
			$query = "select * from mismatch_user where username = '$username'";
			$result = mysqli_query($dbc, $query);
			if (mysqli_num_rows($result) == 0){
				//the username is unique,so insert the data into the database
				//$query = "insert into mismatch_user(username, password,join_date) values(". $username . ", SHA(" . $password1 . "),NOW())";
				$query = "insert into mismatch_user(username, password,join_date) values('$username', SHA($password1), NOW())";
				mysqli_query($dbc,$query) or die(mysqli_error());
				mysqli_close($dbc);
				//comfirm success register the user
				echo "<p>Register successfully!Now,you can log in and <a href = 'edit_profile.php'>edit your profile</a>!</p>";
				exit();
			}
			else{
				echo $username . " is already registered!Please use a different address!<br />";
				$username = "";
			}
		}
		else{
			echo "username and password can not empty or password is not equle repassword";
		}
	}
	else{
		echo "No submit!";
	}
?>
<html>
	<head>
		<title>Mismatch SignUp</title>
	</head>
	<body>
		<h1>Mismatch SignUp</h1>
		<h3>Please enter your username and desired password to sign up to Mismatch</h3>
		<form action = "<?php echo $_SERVER['PHP_SELF'];?>" method = "POST">
			<fieldset>
				Username:&nbsp;<input type = "text" name = "username" value = "<?php if (!empty($username))echo $username?>"/><br />
				Password:&nbsp;<input type = "password" name = "password1" /><br />
				Repassword:<input type = "password" name = "password2" /><br /><br />
			</fieldset>
			<input type = "submit" name = "submit" Value = "Submit" />
		</form>
	</body>
</html>





