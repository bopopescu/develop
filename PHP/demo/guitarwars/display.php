<head>
<title>Display Score</title>
<link rel = 'stylesheet' type = "text/css" href = "static/style.css">
</head>

<body>
	<h1 align = "center">Display Score</h1>
	<?php
	    //define('GW_UPLOADPATH','images/');
		require_once("appvars.php");
		require_once("connectvars.php");
		//require("appvars.php");
		//include_once("appvars.php");
		//include("appvars.php");
		$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
		$query = "select * from guitarwars where approved = 1 order by score desc,date asc";
		$result = mysqli_query($dbc, $query) or die("query mysql error");
		mysqli_close($dbc);
		//echo "These are all high scores!<br />";
		//echo GW_UPLOADPATH;
		echo "<br /><br /><a href = 'add_score.php'>Back to add scores!</a><br />";
		echo "<table align = 'center' width = '100%' border = 'solid 3px red'>";
		//echo "<tr><td>id</td><td>name</td><td>score</td><td>screenshot</td><td>date</td></tr>";
		$i = 0;
		while($row = mysqli_fetch_array($result)){
			if($i == 0){
				//echo "<tr style = 'background-color:pink; font-size:3.0em'>";
				//echo "<td>".$row["score"]."</td></tr>";
				echo "<tr><td colspan='2' class = 'topscoreheader'>Top Score: " . $row["score"] . "</td></tr>";
			}
			echo "<tr><td class = 'scoreinfo'>";
			echo "<span class = 'score'>" .$row["score"]."</span><br />";
			echo "<strong>Id:</strong>".$row["id"]."<br />";
			echo "<strong>Name:</strong>".$row["name"]."<br />";
			echo "<strong>Date:</strong>".$row["date"]."</td>";
			
			//echo "<tr><td>" . $row['id'] . "</td>";
			//echo "<td>" . $row['name'] . "</td>";
			//echo "<td>" . $row['score'] . "</td>";
			if (is_file(GW_UPLOADPATH.$row['screenshot']) && filesize(GW_UPLOADPATH.$row['screenshot']) > 0){
				echo '<td><img src = "' . GW_UPLOADPATH.$row['screenshot'] . '" alt="Score image" /></td>';
			}
			else{
				echo '<td><img src = "unverfied.gif" alt="unverfied score" /></td>';
			}
			//echo "<td>" . $row['date'] . "</td></tr>";
			$i++;
		}
        echo "</table>";
		

	?>
</body>