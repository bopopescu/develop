<?php
	require_once("authorize.php");
?>

<?php 
	require_once("appvars.php");
	require_once("connectvars.php");
	//以下的if条件语句判断是通过哪种请求来与服务器通信的
	if (isset($_GET["id"]) && isset($_GET["date"]) && isset($_GET["name"]) && isset($_GET["score"]) && isset($_GET["screenshot"])){
		$id = $_GET["id"];
		$date = $_GET["date"];
		$name = $_GET["name"];
		$score = $_GET["score"];
		$screenshot = $_GET["screenshot"];
		echo 111111111111111111, "<br />";
	}
	else if (isset($_POST["id"]) && isset($_POST["name"]) && isset($_POST["score"])){
		$id = $_POST["id"];
		$name = $_POST["name"];
		$score = $_POST["score"];
		$screenshot = $_POST["screenshot"];
		//echo 222222222222222222,"<br />";
	}
	else{
		echo "Sorry, no high score was specified for removal.<br />";
	}
	
	//判断是不是POST请求
	if (isset($_POST['submit'])){
		if ($_POST["confirm"] == "Yes"){
			//delete the screen shot from web server
			@unlink(GW_UPLOADPATH . $screenshot);
			//connect to the database
			$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
			//delete the score data from the database
			$query = "delete from guitarwars where id= $id limit 1";
			//echo $query;
			$result = mysqli_query($dbc, $query) or die("query mysql error");
			mysqli_close($dbc);
			
			//comfirm success with the user
			echo "The high score of " . $score . " for " . $name . " was successfully removed!<br />";
		}
		else{
			echo "Nothing removed!<br />";
		}
	}
	else if (isset($id) && isset($date) && isset($name) && isset($score) && isset($screenshot)){
		echo "Are you sure to delete the following high score?<br />";
		echo "<strong>Name:</strong>" . $name. "<br /><strong>Date:</strong>" . $date . "<br /><strong>Score:</strong>" . $score . "<br />";
		
		$phpself = $_SERVER['PHP_SELF'];		
		echo "<form method = 'POST' action = 'removescore.php'>";
		echo "<input type = 'radio' name = 'confirm' value = 'Yes' />Yes";
		echo "<input type = 'radio' name = 'confirm' value = 'No' checked = 'checked' />No<br />";
		echo "<input type = 'submit' name = 'submit' value = 'Submit' />";
		echo "<input type = 'hidden' name = 'id' value = '" . $id . "' />";
		echo "<input type = 'hidden' name = 'name' value = '" . $name . "' />";
		echo "<input type = 'hidden' name = 'score' value = '" . $score . "' />";
		echo "<input type = 'hidden' name = 'screenshot' value = '" . $screenshot . "' />";
		echo "</form>";		
	}
	
	//echo "delete ". $id . " " . $name . " " . $score . "<br />";
	
	echo "<a href = 'admin.php'>backup to admin page</a>";
?>