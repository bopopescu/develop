<html>
	<head>
		<title>Aliens Abducted Me</title>
	</head>
	<body>
	    <h2>Aliens Abducted Me</h2>
		<?php
		    $when_it_happened = $_POST['when'];
			$how_long = $_POST['howlong'];
			$description = $_POST['description'];
			$test=null;
			$num = 99;
			$ha = $_POST['howlong']. ''.$_POST['description'];
			echo 'Thank\'s for submiting the form.<br />';
			echo "when it happend? ",$when_it_happened,"<br />";
			echo "how long? ".$how_long,"<br />";
			echo "description11: ".$description,"<br />";
			echo "test result is: ".$test,"nothing is found<br />";
			echo "xudedong is: $ha,<br />";
			echo "******************************".$num."<br />";
			echo $ha."<br />";
			echo "++++++++++++++++++++++++++++++++++++++++++<br />";
			$msg = "Thanks for submiting the form.\n" .
			       "when it happend? $when_it_happened\n" .
				   "how long? $how_long\n" .
				   "description11: $description";
			echo $msg."<br />";
			$to = "dedong.xu@goland.cn";
			$subject = "Aliens Abducted Me";
			$email = "1025977445@qq.com";
			//mail($to,$subject,$msg,"From: ".$email);
			//$xudedong = $how_long . ' ' . $description;
		?>
		<?php
		    $dbc = mysqli_connect("localhost","root","19890612","test") or die("Error connecting to MYSQL server");
			$query = "insert into emps (name)" .
			         " values ($how_long)";
			$result = mysqli_query($dbc,$query) or die("Error querying database");
			//mysqli_query($dbc,$query) or die("Error querying database");
			mysqli_close($dbc);
		?>
	</body>
</html>