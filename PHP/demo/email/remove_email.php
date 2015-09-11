<head>
	<title>Display Records</title>
</head>

<body>
    <h1 align = "center">Display Records</h1>
	<form method = "POST" action = "<?php echo $_SERVER['PHP_SELF'] ?>">
		<?php
			$dbc =  mysqli_connect("localhost","root","19890612","test") or die("connect mysql error");
			if (isset($_POST["submit"])){
				//$dbc =  mysqli_connect("localhost","root","19890612","test") or die("connect mysql error");
				if (isset($_POST["todelete"])){
					foreach ($_POST["todelete"] as $each_id){
						$query = "delete from email_list where id = $each_id";
						mysqli_query($dbc,$query) or die("query mysql error");
					}
					echo "removed!!";
				}
			}
			
			//display the customer rows with checkboxes for deleting
			$query = "select * from email_list";
			$result = mysqli_query($dbc,$query) or die("query mysql error");
			//mysqli_close($dbc);
			$row = mysqli_fetch_array($result);
			//echo $row["name"] . " " . $row["age"]. " " . " " . $row["email"];
			echo "<table width = '40%' align = 'center' border = 'solid red 3px'>";
			echo "<tr><td>СЎПо</td><td>id</td><td>name</td><td>age</td><td>email</td></tr>";
			while ($row = mysqli_fetch_array($result)){
				echo "<tr><td><input type = 'checkbox' value = '".$row['id']."' name='todelete[]'/></td>";
				echo "<td>".$row['id']."</td>";
				echo "<td>".$row['name']."</td>";
				echo "<td>".$row['age']."</td>";
				echo "<td>".$row['email']."</td>";
			}	
			echo "</table>";
			//$array = [1,2,3,4,9,7,56];
			//foreach($array as $each_record){
			//	echo $each_record."<br />";
			//}
			mysqli_close($dbc);
		?>
		<p align = "center"><input type = "submit" name = "submit" value = "Remove" /></p>
	</form>
</body>