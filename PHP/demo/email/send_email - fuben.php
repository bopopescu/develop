﻿<head><title>Use PHP Send Email Success</title></head>
<body style = "background-color:white">
	<h1 align = "center">Use PHP Send Email Success</h1>
	<!--<form action = "send_email.php" method = "POST">-->
	<form action = "<?php echo $_SERVER['PHP_SELF'] ?>" method = "POST">
		<table align = "center">
			<tr>
				<td>Subject:</td><td><input style = "width:420px" type = "text" name = "subject" /></td>
			</tr>
			<tr>
				<td>Content:</td><td><textarea cols = "50" rows = "8" name = "content"></textarea></td>
			</tr>
			<tr>
				<td></td><td><input type = "submit" value = "Submit" /></td>
			</tr>
		</table>
	</form>
	<?php
		function test(){
			$output_form = false;
			if (!empty($_POST)){
			//if (!empty($_POST["subjects"]) && !empty($_POST["content"])){
			//if (isset($_POST["subjects"]) && isset($_POST["content"])){
				$subject = $_POST["subject"];
				$content = $_POST["content"];
			}
			
			if (!(empty($subject) || empty($content))){
			    $dbc = mysqli_connect("localhost","root","19890612","test") or die("connect mysql error");
				$query = "select * from email_list";
				$result = mysqli_query($dbc,$query) or die("query mysql error");
				mysqli_close($dbc);
				$row = mysqli_fetch_array($result);
				//echo $row["name"] . " " . $row["age"]. " " . " " . $row["email"];
				echo "<table align = 'center' border = 'solid red 3px'>";
				echo "<tr><td>id</td><td>name</td><td>age</td><td>email</td><td>Subject</td><td>Content</td></tr>";
				while ($row = mysqli_fetch_array($result)){
					echo "<tr><td>".$row['id']."</td>";
					echo "<td>".$row['name']."</td>";
					echo "<td>".$row['age']."</td>";
					echo "<td>".$row['email']."</td>";
					echo "<td>".$subject."</td>";
					echo "<td>".$content."</td></tr>";
				}	
				echo "</table>";
				
				if(isset($_POST)){echo "xudeong is a good man!";}
				$a = "xudedong";
				$b = $a;
				if ($a == '$b'){echo "1111111111111111111<br />";}
				if ($a == "$b"){echo "222223322222222222222<br />".$b."<br />";}
				if ($a == $b)  {echo "{$b}<br />"; echo '{$b}';echo "{$b}<br />";}
				if (0 == ''){echo "零和单引号空串是相等的<br />";}
				if (0 == ""){echo "零和双引号空串是相等的<br />";}
            }
			else{
				//echo "you forgot the email subject or content!";
				if (empty($subject) && empty($content)){
					echo "you forgot the email subject and content!<br />";
					$output_form = true;
					echo "11111111111111111111111111111111111111111111111111111";
				?>
				<div>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</div>
				<?php
				}
				if (empty($subject) && !empty($content)){
					echo "you forgot the email subject!<br />";
					$output_form = true;
				}
				if (!empty($subject) && empty($content)){
					echo "you forgot the email content!<br />";
					$output_form = true;
				}
				if (!empty($subject) && !empty($content)){
					echo "everything is ok,send the email!<br />";
				}
			}
			if ($output_form){
				?>
				<form action = "<?php echo $_SERVER['PHP_SELF'] ?>" method = "POST">
				<table align = "center">
				<tr>
					<td>Subject:</td><td><input style = "width:420px" type = "text" name = "subject" /></td>
				</tr>
				<tr>
					<td>Content:</td><td><textarea cols = "50" rows = "8" name = "content"></textarea></td>
				</tr>
				<tr>
					<td></td><td><input type = "submit" value = "Submit" /></td>
				</tr>
				</table>
				</form>
				<?php
			}
		}
		test();
	?>
	
	<?php
	function foo(){
		function bar(){
			echo "<br /><br /><br /><br /><br />xudedong is a good man!!!!!!!!!!";
		}
	?>
	<?php
	}
	/* 现在还不能调用bar()函数，因为它还不存在 */
	foo();
	/* 现在可以调用bar()函数了，因为foo()函数
   的执行使得bar()函数变为已定义的函数 */
	bar();
	?>
<br /><br />
<div align = "center"><a href = "add_email.html" target = "_blank">继续添加</a></div>
<div align = "center"><a href = "remove_email.html" target = "_blank">删除</a></div>
</body>

<script>
function test(){
var num = 0;
test: 
for (i=0;i<10;i++){
	for(j=0;j<10;j++){
		if (i==5&&j==5){
			continue test
		}
	num++;	
	}
	
}
alert(num)
var num = 0;
test: 
for (i=0;i<10;i++){
	for(j=0;j<10;j++){
		if (i==5&&j==5){
			break test
		}
	num++;	
	}
	
}
alert(num)
}
</script>