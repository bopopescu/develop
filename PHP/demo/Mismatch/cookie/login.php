<?php
	require_once("connectvars.php");
	//clear the error message
	$error_message = "";
	
	//if the user is not log in, try to log in
	
	if (!isset($_COOKIE["id"])){
		if (isset($_POST["submit"])){
			//connect the database
			$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
			//grab the user entered log in data
			$user_username = mysqli_real_escape_string($dbc, trim($_POST["username"]));
			$user_password = mysqli_real_escape_string($dbc, trim($_POST["password"]));
			if (!empty($user_username) && !empty($user_password)){
				//look up the username and password in the database
				$query = "select id ,username from mismatch_user where username = '$user_username' and password = SHA('$user_password')";
				$result = mysqli_query($dbc,$query);
				
				if (mysqli_num_rows($result) == 1){
					//the log in is OK so set the user id and username cookies, and redirect to the home page
					$row = mysqli_fetch_array($result);
					setcookie("id", $row["id"]);
					setcookie("username",$row["username"]);
					//$home_url = 'http://' . $_SERVER['HTTP_POST'] . dirname($_SERVER['PHP_SELF']) . '/index.php';
					$home_url = "http://10.10.2.11/mismatch/cookie/index.php";
					header("Location: " . $home_url);
				}
				else{
					//the username/password are incorrect so set an error message
					$error_message = "Sorry, you must enter a valid username and password to log in";
				}
			}
			else{
				//the username/password are incorrect so set an error message
				$error_message = "Sorry, you must enter your username and password to log in";
			}
		}
	}
?>
		
<?php
	//if the cookie is empty ,show an error message and the log-in form, otherwise confirm the login
	if (empty($_COOKIE["id"])){
		echo $error_message;
	
?>
		
<html>
	<head>
		<title>Mismatch Log In</title>
	</head>
	<body>
		<h3>Mismatch Log In</h3>
		<form method = "POST" action = "<?php echo $_SERVER["PHP_SELF"];?>">
			<fieldset>
			    <legend>Log In</legend>
				<label for = "username">Username:</label> 
	<input type = "text" name = "username" value = "<?php if (!empty($user_username)) {echo $user_username;}?>"/><br />
				<label for = "username">Password:</label> 
				<input type = "password" name = "password" /><br />
			</fieldset>
			<input type = "submit" name = "submit" value = "Log In">
		</form>
	</body>
</html>
<?php	
	}
	else{
		//confirm the successful login
		//echo "You are log in as " . $_COOKIE["username"];
		//$home_url = "http://10.10.2.11/mismatch/index.php";
		//header("Location: " . $home_url);
	}
?>




