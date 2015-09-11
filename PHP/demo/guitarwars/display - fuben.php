<head>
<title>Display Score</title>
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
		$query = "select * from guitarwars order by score desc,date asc";
		$result = mysqli_query($dbc, $query) or die("query mysql error");
		mysqli_close($dbc);
		//echo "These are all high scores!<br />";
		echo GW_UPLOADPATH;
		echo "<table align = 'center' width = '100%' border = 'solid 3px red'>";
		echo "<tr><td>id</td><td>name</td><td>score</td><td>screenshot</td><td>date</td></tr>";
		$i = 0;
		while($row = mysqli_fetch_array($result)){
			if($i == 0){
				echo "<tr style = 'background-color:pink; font-size:3.0em'><td>"."</td>";
				echo "<td></td>";
				echo "<td>".$row["score"]."</td>";
				echo "<td></td>";
				echo "<td></td></tr>";
			}
			echo "<tr><td>" . $row['id'] . "</td>";
			echo "<td>" . $row['name'] . "</td>";
			echo "<td>" . $row['score'] . "</td>";
			if (is_file(GW_UPLOADPATH.$row['screenshot']) && filesize(GW_UPLOADPATH.$row['screenshot']) > 0){
				echo '<td><img src = "' . GW_UPLOADPATH.$row['screenshot'] . '" alt="Score image" /></td>';
			}
			else{
				echo '<td><img src = "unverfied.gif" alt="unverfied score" /></td>';
			}
			echo "<td>" . $row['date'] . "</td></tr>";
			$i++;
		}
        echo "</table>";
		echo "<br /><br /><a href = 'add_score.php'>Back to add scores!</a><br />";

	?>
</body>