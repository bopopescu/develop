<?php
    require_once("authorize.php");
?>

<?php/*
    require_once("connectvars.php");
    if (isset($_GET["id"])){
		$id = $_GET["id"];
		$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
		$query = "update guitarwars set approved = 1 where id = '$id'";
		mysqli_query($dbc,$query) or die("query mysql error");
		mysqli_close($dbc);
		echo "<h1><strong>Approved success</strong>!</h1><br />";
		echo "backup to <a href = 'admin.php'>admin page</a>!";
	}
*/?>

<?php
	require_once("connectvars.php");
	//以下的if条件语句判断是通过哪种请求来与服务器通信的
	if (isset($_GET["id"]) && isset($_GET["date"]) && isset($_GET["name"]) && isset($_GET["score"])){
		$id = $_GET["id"];
		$date = $_GET["date"];
		$name = $_GET["name"];
		$score = $_GET["score"];
		echo 111111111111111111, "<br />";
	}
	else if (isset($_POST["id"]) && isset($_POST["date"]) && isset($_POST["name"]) && isset($_POST["score"])){
		$id = $_POST["id"];
		$date = $_POST["date"];
		$name = $_POST["name"];
		$score = $_POST["score"];
		echo 222222222222222222,"<br />";
	}
	else{
		echo "Sorry, no high score was specified for approved.<br />";
	}
	if (isset($_POST["submit"])){
		if ($_POST["confirm"] == "Yes"){
			$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
			$query = "update guitarwars set approved = 1 where id = '$id'";
			mysqli_query($dbc,$query) or die("query mysql error");
			mysqli_close($dbc);
			echo "<h1><strong>Approved success!</strong></h1><br />";
			echo "Name: " . $name . ", Score: " . $score . "<br /><br />";
		}
		else {
			echo "Sorry,there was a problem approving the high score.<br />";
		}
	}
	else if (isset($id)){
		echo "<h2>Are you sure to approve the following high score?</h2><br />";
		echo "<strong>Name:</strong>" . $name. "<br /><strong>Date:</strong>" . $date . "<br /><strong>Score:</strong>" . $score . "<br />";	
		echo "<form method = 'POST' action = 'approved_score.php'>";
		echo "<input type = 'radio' name = 'confirm' value = 'Yes' />Yes";
		echo "<input type = 'radio' name = 'confirm' value = 'No' checked = 'checked' />No<br />";
		echo "<input type = 'submit' name = 'submit' value = 'Submit' />";
		echo "<input type = 'hidden' name = 'id' value = '" . $id . "' />";
		echo "<input type = 'hidden' name = 'date' value = '" . $date . "' />";
		echo "<input type = 'hidden' name = 'name' value = '" . $name . "' />";
		echo "<input type = 'hidden' name = 'score' value = '" . $score . "' />";
		echo "</form>";		
	}
	echo "<a href = 'admin.php'>backup to admin page</a>!";
?>