<head>
	<title>Use PHP Add Email Success</title>
</head>

<body>
	<h1 align = "center">Use PHP Add Email Success</h1>
	<?php
	    $username = $_POST['username'];
		$age = $_POST['age'];
		$email = $_POST['email'];
			
	    $dbc = mysqli_connect("localhost","root","19890612","test") or die("connect mysql error");
	    $query = "insert into email_list(name,age,email) values('$username','$age','$email')";
		//$query = "insert into emial_list(name,age,email) values($_POST['username'],$_POST['age'],$_POST['email'])";
		//$query = "insert into emial_list(name,age,email) values('xdd',18,'1@qq.com')";
		$result = mysqli_query($dbc,$query) or die("query mysql error");
		mysqli_close($dbc);	
	    echo "<table align = 'center' border = 'solid red 3px'>";
		echo "<tr><td>Your name</td><td><span style = 'font-size:2.0em'>".$_POST["username"]."</span></td></tr>";
		echo "<tr><td>Your age  </td><td><span style = 'font-size:2.0em'>".$_POST["age"]."</span></td></tr>";
		echo "<tr><td>Your email  </td><td><span style = 'font-size:2.0em'>".$_POST["email"]."</span></td></tr>";
		echo "</table>";

		
	?>
	<?php
		function recursion($a){
			if($a < 10){
				echo "$a<br />";
				recursion($a+1);
			}
		}
		recursion(1);
	?>
	<?php
		$array12=array("7"=>"编","6"=>"程","9"=>"词","8"=>"典");
		print_r($array12);
		echo "<br>*******************************<br />";
		echo $array12[7]; //注意：下标默认是从1开始       
		echo $array12[6];        
		echo $array12[9];        
		echo $array12[8]."<br />*****************************<br />";        
	?>
	<?php
		$arraytest[1] = "I";
		$arraytest[2] = "love";
		$arraytest[3] = "you";
		$arraytest[4] = "much";
		print_r($arraytest);
	?>

	<br />
	<div align = "center"><a href = "add_email.html" target = "_blank">返回</a></div>
	<div align = "center">去<a href = "send_email.html" target = "_blank">发送邮件</a>吧</div>
</body>