<head>
<title>Add Score</title>
</head>

<body>
	<h1 align = "center">Add Score</h1>
	<?php
		//开始一个会话，必须由session_start()开始
	    session_start();
		
		require_once("appvars.php");
		require_once("connectvars.php");
		echo $_SESSION["pass_phrase"];
		//if (is_numeric("")){echo 12345;}else{echo 54321;};
		if (isset($_POST['submit'])){
			$name = trim($_POST['name']);
			$score = trim($_POST['score']);
			$screenshot = trim($_FILES['screenshot']['name']);
			$screenshot_type = trim($_FILES['screenshot']['type']);
			$screenshot_size = trim($_FILES['screenshot']['size']);
			
			//check the CAPTCHA pass-phrase for verification
			$user_pass_phrase = sha1($_POST["verifity"]);
			$user_pass_phrase = $_POST["verifity"];
			echo $_POST["verifity"];
			if ($_SESSION["pass_phrase"] == $user_pass_phrase){
				echo "OK";			
				if(!empty($name) && !empty($score) && !empty($screenshot)){
					if (is_numeric($score)){
						if ((($screenshot_type == "image/gif") || ($screenshot_type == "image/jpeg") || ($screenshot_type == "image/pjpeg") 
							|| ($screenshot_type == "image/png")|| ($screenshot_type == "image/bmp")) && ($screenshot_size > 0) &&($screenshot_size <= GW_MAXFILESIZE)){   
							if ($_FILES["file"]["error"] == 0){
								$screenshot = time().trim($_FILES['screenshot']['name']);
								$target = GW_UPLOADPATH.$screenshot;
								if (move_uploaded_file($_FILES['screenshot']['tmp_name'],$target)){
									$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
									$name = mysqli_real_escape_string($dbc,trim($_POST['name']));
									$score = mysqli_real_escape_string($dbc,trim($_POST['score']));
									$screenshot = mysqli_real_escape_string($dbc,time().trim($_FILES['screenshot']['name']));
									//echo $score;
									$query = "insert into guitarwars (name,date, score, screenshot) values ('$name',NOW(),'$score','$screenshot')";
									mysqli_query($dbc, $query) or die("query mysql error");
									mysqli_close($dbc);
									
									echo "Thanks for adding your new high score!<br />";
									echo "Your name is: " . $name . "<br />";
									echo "Your score is: " . $score . "<br />";
									echo '<img src = "' . $target . '"alt = Score image"/><br />';
									echo "<a href = 'display.php'>Back to high scores!</a><br />";
									//echo time();
								}
								else{
									echo "file moved failed!<br />";
								}
							}
							else{
								echo "file uploaded failed!<br />";
							}
						}
						else{
							echo "must be a gif,  jpeg, pjpeg, png file, and no bigger than " . (GW_MAXFILESIZE/1024) . "KB in size<br />";
						}
					}
					else{
						echo "$score is not a number!<br />";
					}
					//try to delete the temporary screent dhot image fle;
					@unlink($_FILES['screenshot']['tmp_name']);
				}
				else{
					echo "All blankes must be filled!<br />";
				}
			}
			else{
				echo "Please enter the verification pass-phrase exactly as shown<br />";
			}
		}
		echo "<a href ='display.php'>Display scores</a>";
		
		
	?>
	<p>
	<a href = "newsfeed.php"><img scr = "" alt = "link">Click to syndicate the abduction newsfeed feed<br /></a>
	</p>
	<form enctype = "multipart/form-data" method = "POST" action = "<?php echo $_SERVER['PHP_SELF'];?>">
	<!--<form enctype = "multipart/form-data" method = "POST" action = "display.php">-->
	    <input type = "hidden" name = "max_file_size">
		<table align = "center">
			<tr>
				<td>Name:</td><td><input type = "text" name = "name" value = "<?php if(!empty($name)){echo $name;} ?>"/></td>
			</tr>
			<tr>
				<td>Score:</td><td><input type = "text" name = "score" value = "<?php if(!empty($score)) echo $score; ?>" /></td>
			</tr>
			<tr>
				<td>Screen Shot:</td><td><input type = "file" name = "screenshot" /></td>
			</tr>
			<tr>
				<td>Verifity:</td><td><input type = "text" name = "verifity" />&nbsp;<img src = "captcha.php" alt = "验证码"></td>
			</tr>
			<tr>
				<td></td><td><input type = "submit" name = "submit" value = "Submit" /></td>
			</tr>
		</table>
	</form>
</body>

<?php
	//require_once("youtube.php");
	class Song
	{
		var $title;
		var $lyrics;
		function Song($title,$lyrics){
			$this -> title = $title;
			$this -> lyrics = $lyrics;
		}
		function sing(){
			echo "This is called " . $this -> title . "<br />";
			echo "One two " . $this -> lyrics."<br />";
		}
	}
	$shoes_song = new Song("Blue Suede Shoes", "Well it os one for the money");
	$shoes_song -> sing();
	
	$aa = (4-2-1);
	echo $aa;
?>