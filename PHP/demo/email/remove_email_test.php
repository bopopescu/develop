<head>
	<title>Use PHP Add Email Success</title>
</head>

<body>
	<h1 align = "center">Use PHP Add Email Success</h1>
	<?php
		$email = $_POST['email'];
			
	    $dbc = mysqli_connect("localhost","root","19890612","test") or die("connect mysql error");
	    $query = "delete from email_list where email = '$email'";
		$result = mysqli_query($dbc,$query) or die("query mysql error");
		mysqli_close($dbc);	
		echo "Remove ",$email;

	?>
	<br />
	<div align = "center"><a href = "remove_email.html" target = "_blank">删除</a></div>

</body>