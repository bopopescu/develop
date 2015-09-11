<?php
    //start the session
	require_once("startsession.php");
	
	//insert the page header
	$page_title = "Questionnaire";
	require_once("header.php");
	
	//make sure the is logged in before going any further
	if (!isset($_SESSION["id"])){
		echo "Please <a href = 'login.php'>log in</a> to access the page!";
		exit();
	}
	
	//show the nav menu
	require_once("navmenu.php");
	
	require_once("connectvars.php");
?>

<?php
	//connect to the database
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
	//第一次访问，插入空响应
	//if this user has never answered the questionnaire, insert empty response into the database
	$query = "select * from mismatch_response where user_id = '" . $_SESSION["id"] . "'";
	$result = mysqli_query($dbc, $query) or die("query mysql error1");
	if (mysqli_num_rows($result) == 0){
		//first grab the list of topic ids from topic table
		$query = "select topic_id,name,category_id from mismatch_topic";
		$result = mysqli_query($dbc,$query) or die("query mysql error2");
		$topicIDs = array();
		while ($row = mysqli_fetch_array($result)){
			//echo $row["topic_id"],"<br />".$row["name"]."<br />",$row["category"],"<br />";
			array_push($topicIDs,$row["topic_id"]);
		}
		
		//insert into empty response rows into the response table, one per topic
		foreach($topicIDs as $topic_id){
			$query = "insert into mismatch_response(user_id, topic_id) values ('" . $_SESSION["id"] . "','$topic_id')";
			mysqli_query($dbc, $query) or die("query mysql error3");
		}
	}
	
	//提交用户回答的问题，更新数据库内容
	//if the questionnaire form has been submitted,write the form response to the database 
	if (isset($_POST["submit"])){
		//write the questionnaire response rows to the response table
		foreach ($_POST as $response_id => $response){
			$query = "update mismatch_response set response = '$response' where response_id = '$response_id'";
			mysqli_query($dbc, $query);
		}
		echo "Your responses have been saved!";
	}
	
	//grab the response data from the database to generate the form
	$query = "select response_id, topic_id, response from mismatch_response where user_id = '" . $_SESSION["id"] . "'";
	$result = mysqli_query($dbc, $query) or die("query mysql error4");
	$responses = array();
	while ($row = mysqli_fetch_array($result)){
		//look up the topic name for the response from the topic table
		$query2 = "select name, category_id from mismatch_topic where topic_id = '" . $row["topic_id"] . "'";
		$result2 = mysqli_query($dbc, $query2) or die("query mysql error5");
		if (mysqli_num_rows($result2) == 1){
			$row2 = mysqli_fetch_array($result2);
			//get category name from mismatch_category table
			$query3 = "select name from mismatch_category where category_id = '" . $row2["category_id"] . "'";
			$result3 = mysqli_query($dbc, $query3) or die("query mysql error6");
			if (mysqli_num_rows($result3) == 1){
				$row3 = mysqli_fetch_array($result3);
				//topic name
				$row["topic_name"] = $row2["name"];
				//cate gory name
				$row["category_name"] = $row3["name"];
				array_push($responses,$row);
				//array(name,category)
			}
			else{
				echo "No such category!<br />";
			}
		}
	}
	mysqli_close($dbc);
	
	//generate the questionnaire form by looping through the response array
	echo '<form method = "POST" action ="' .$_SERVER['PHP_SELF'] . '">';
	echo "How do you feel about each topic?<br />";
	$category = $responses[0]['category_name'];
	echo '<fieldset><legend>' . $category . '</legend>';
	foreach ($responses as $response){
		//only start a new fieldset if the category has changed
		if ($category != $response["category_name"]){
			$category = $response["category_name"];
			echo '</fieldset><fieldset><legend>' . $category . '</legend>';
		}
		
		//display the topic form field
		echo '<label ' . ' for="' . $response["response_id"] . '">' . $response["topic_name"] . ':</label>';
		echo '<input type = "radio" id ="'.$response["response_id"] .'" name = "' . $response["response_id"] . 
		     '" value = "1"'. ($response["response"] == 1 ? "checked=checked":"") .'/>Love';
		echo '<input type = "radio" id ="'.$response["response_id"] .'" name = "' . $response["response_id"] . 
		     '" value = "2"'. ($response["response"] == 2 ? "checked=checked":"") .'/>Hate<br /><br />';
	}
	echo "</fieldset>";
	echo '<input type = "submit" name = "submit" value = "Submit" />';
	echo "</form>";
	$array_name = array();
	$array_element["a"] = "xudedong";
	$array_element["b"] = "xdd";
	array_push($array_name,$array_element);
	echo $array_name[0]["b"];
?>

<?php
	require_once("footer.php");
	1==2? $a=5:$a=6;
	echo $a;
?>








