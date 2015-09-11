<?php
	if (isset($_POST["submit"])){
		$first_name = $_POST["firstname"];
		$last_name = $_POST["lastname"];
		$email = $_POST["email"];
		$phone = $_POST["phone"];
		$job = $_POST["job"];
		$resume = $_POST["resume"];
		$output_form = "no";
		echo strlen("aaasdfg"),"<br />";
		if (empty($first_name)){
			echo "You forgot to enter your first name<br />";
			$output_form = "yes";
		}
		if (empty($last_name)){
			echo "You forgot to enter your last name<br />";
			$output_form = "yes";
		}
		if (empty($email)){
			echo "You forgot to enter your email<br />";
			$output_form = "yes";
		}
		if (empty($phone)){
			echo "You forgot to enter your phone<br />";
			$output_form = "yes";
		}
		else if(!is_numeric($phone)){
			echo "Not a phone number<br />";
		}
		if (empty($job)){
			echo "You forgot to enter your job<br />";
			$output_form = "yes";
		}
		if (empty($resume)){
			echo "You forgot to enter your resume<br />";
			$output_form = "yes";
		}
		
	}
	else{
		$output_form = "yes";
	}
	
	if ($output_form == "yes"){
?>
	<form method = "POST" action = "<?php echo $_SERVER['PHP_SELF'];?>">
		<table>
			<tr><td>First Name:</td><td><input type = "text" name = "firstname" value = "<?php echo $first_name?>"/></td></tr>
			<tr><td>Last Name:</td><td><input type = "text" name = "lastname" value = "<?php echo $last_name?>"/></td></tr>
			<tr><td>Email:</td><td><input type = "text" name = "email" value = "<?php echo $email?>"/></td></tr>
			<tr><td>Phone:</td><td><input type = "text" name = "phone" value = "<?php echo $phone?>"/></td></tr>
			<tr><td>Job:</td><td><input type = "text" name = "job" value = "<?php echo $job?>"/></td></tr>
			<tr><td>Resume:</td><td><input type = "text" name = "resume" value = "<?php echo $resume?>"/></td></tr>
		</table>
		<input type = "submit" name = "submit" value = "Submit">
	</form>

	
<?php
	}
?>