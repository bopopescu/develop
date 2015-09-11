<?php
	require_once("authorize.php");
	require_once("connectvars.php");
	//if(!isset($_SERVER["PHP_AUTH_USER"]) || !isset($_SERVER["PHP_AUTH_PW"])){
	//	header("HTTP/1.1 401 Unauthorized");
	//	header('WWW-Authenticate:Basic realm = "Mismatch"');
	//	exit("<h2>Mismatch</h2>Sorry,you must enter your username and password to login and access this page!");
	//}
	//connect to the database
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
	//验证表单可能有危险的串进行转义
	$user_username = mysqli_real_escape_string($dbc,trim($_SERVER["PHP_AUTH_USER"]));
	$user_password = mysqli_real_escape_string($dbc,trim($_SERVER["PHP_AUTH_PW"]));
	//look up the username and password in the database
	$query = "select id,username from mismatch_user where username = '$user_username' and password = SHA('$user_password')";
	$result = mysqli_query($dbc,$query);
	mysqli_close($dbc);
	
	if (mysqli_num_rows($result) == 1){
		//the log in is OK so set the user ID and username variables
		$row = mysqli_fetch_array($result);
		$id = $row["id"];
		$username = $row["username"];
	}
	else{
		//the username/password are incorrect so send the authentication headers
		//require_once("authorize.php");
		header("HTTP/1.1 401 Unauthorized");
		header('WWW-Authenticate:Basic realm = "Mismatch"');
		exit("<h2>Mismatch</h2>Sorry,you must enter your username and password to login and access this page!
		If you are not a registered user,please <a href = 'signup.php'>sign up</a>");
	}
	
	?>
	<?php
	//echo "<html><head><title>welcome to log in</title></head></html>";
	//confirm the successful log in
	echo "<p>you are logged in as <span style = 'font-size:2.5em'>". $username ."</span></p>";
	echo "<p>Go to <a href = 'index.php'>Main Page</a></p>";
	//echo "<p>Go to <a href = 'view_profile.php'>View Profile</a></p>";
	//echo "<p>Go to <a href = 'edit_profile.php'>Edit Profile</a></p>";
?>