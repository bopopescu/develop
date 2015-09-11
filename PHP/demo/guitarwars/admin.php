<?php
	require_once("authorize.php");
?>

<html>
<head>
<title>admin page</title>
</head>
<body style = "background-color:white">
<h1 align = "center">Admin Page</h1>
<h2>Below is a list of all Guitar Wars high scores. Use this page to remove scores as needed.</h2>
</body>
</html>
<?php
	require_once("appvars.php");
	require_once("connectvars.php");
	
	//connect the database
	$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
	
	$query = "select * from guitarwars order by score desc, date asc";
	$result = mysqli_query($dbc, $query) or die("query mysql error");
	mysqli_close($dbc);
	
	//loop through the array of score data, formatting it as HTML
	echo "<table width = '100%' border>";
	while ($row = mysqli_fetch_array($result)){
		//display the score data
		echo "<tr><td><strong>".$row["id"]."&nbsp;</strong></td>";
		echo "<td><strong>".$row["name"]."</strong></td>";
		echo "<td>".$row["date"]."</td>";
		echo "<td>".$row["score"]."</td>";
		echo '<td><a href = "removescore.php?id=' . $row["id"] . '&amp;date=' . $row["date"] . '&amp;name=' . $row["name"] 
		. '&amp;score=' . $row["score"] . '&amp;screenshot=' . $row["screenshot"] . '">Remove</a>';
		
		if ($row["approved"] == 0){
			echo '/<a href = "approved_score.php?id=' . $row["id"] . '&amp;date=' . $row["date"] . '&amp;name=' . 
			$row["name"]. '&amp;score=' . $row["score"] . '">Approved</a></td></tr>';
		}

	}
	echo "</table>";
	
?>