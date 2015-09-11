<?php
    //start session
	require_once("startsession.php");
	
	//insert into page header
	$page_title = "MyMismatch";
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
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die(mysqli_error());
	//$query = "select * from mismatch_response where user_id = '" . $_SESSION["id"] . "'";
	$query = "select mr.response_id, mr.topic_id, mr.response, mt.name as topic_name, mc.name as category_name from mismatch_response as mr ".
	"inner join mismatch_topic as mt using(topic_id) inner join mismatch_category as mc using(category_id) where user_id = '" . $_SESSION["id"] . "'";
	$result = mysqli_query($dbc, $query) or die("query mysql error1");
	if (mysqli_num_rows($result) != 0){
		$user_responses = array();
		while ($row = mysqli_fetch_array($result)){
			array_push($user_responses,$row);
		}
		//print_r(count($user_responses));
		//initialize the mismatch search results
		$mismatch_score = 0;
		$mismatch_user_id = -1;
		$mismatch_topics = array();
		
		//loop through the user table comparing other people's response to the user's response
		$query = "select id from mismatch_user where id != '" . $_SESSION["id"] . "'";
		$result = mysqli_query($dbc, $query) or die(mysqli_error());
		while ($row = mysqli_fetch_array($result)){
			//grab the response data for the user
			$query2 = "select response_id,topic_id, response from mismatch_response where user_id = '" . $row["id"] . "'";
			$result2 = mysqli_query($dbc, $query2) or die(mysqli_error());
			$mismatch_responses = array();
			while ($row2 = mysqli_fetch_array($result2)){
				array_push($mismatch_responses, $row2);
			}
			
			//compare each response and calculate a mismatch total
			$score = 0;
			$topics = array();
			for ($i = 0; $i < count($user_responses); $i++){
				if (((int)$user_responses[$i]["response"]) + ((int)$mismatch_responses[$i]["response"]) == 3){
					$score += 1;
					array_push($topics, $user_responses[$i]["topic_name"]);
					
				}
				else{
					//echo 9,"<br />";
				}
			}
			
			//check to see if this person is better than the best mismatch so far
			if ($score > $mismtach_score){
				//wo found a better mismatch, so update the best mismatch search results
				$mismatch_score = $score;
				$mismatch_user_id = $row["id"];
				$mismatch_topics = array_slice($topics,0);
			}
		}
		
		//make sure a mismatch was found
		if ($mismatch_user_id != -1){
			$query = "select * from mismatch_user where id = '" . $mismatch_user_id . "'";
			$query = "select * from mismatch_user where id = '$mismatch_user_id'";
			$result = mysqli_query($dbc, $query) or die(mysqli_error());
			if (mysqli_num_rows($result) == 1){
				//the user row for the mismatch was found,so display the user data
				$row = mysqli_fetch_array($result);
				if (!empty($row["first_name"]) && !empty($row["last_name"])){
					echo $row["first_name"] . " " . $row["last_name"] . "<br />";
				}
				if (!empty($row["city"]) && !empty($row["state"])){
					echo $row["city"] . " " . $row["state"] . "<br />";
				}
				if (!empty($row["picture"])){
					echo 222222,"<br />";
				}
				echo "<hr />";
				//display the mismatch topics
				echo "You are mismatched on the following " . count($mismatch_topics) . " topics:<br /><br />";
				foreach ($mismatch_topics as $topic){
					echo $topic, "<br /><br />";
				}
				
				//display a link to the mismatch user's profile
				echo "<a href = 'view_profile.php?id=". $mismatch_user_id. "'>". $row["first_name"] . "'s profile</a><br />";
			}
		}
	}
	else{
		echo "You must first <a href = 'questionnaire.php'>answer the questionnaire</a> before you can be mismatched!";
	}
?>

<?php
	require_once("footer.php");
?>