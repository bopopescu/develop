<head>
<title>Add Score</title>
</head>

<body>
	<h1 align = "center">Add Score</h1>
	<?php
	    //define('GW_UPLOADPATH','images/');
		require_once("appvars.php");
		require_once("connectvars.php");
		//if (is_numeric("")){echo 12345;}else{echo 54321;};
		if (isset($_POST['submit'])){
			$name = trim($_POST['name']);
			$score = trim($_POST['score']);
			$screenshot = trim($_FILES['screenshot']['name']);
			$screenshot_type = trim($_FILES['screenshot']['type']);
			$screenshot_size = trim($_FILES['screenshot']['size']);
			
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
		echo "<a href ='display.php'>Display scores</a>";
	?>
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
				<td></td><td><input type = "submit" name = "submit" value = "Submit" /></td>
			</tr>
		</table>
	</form>
</body>