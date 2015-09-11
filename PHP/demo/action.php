我叫<?php echo htmlspecialchars($_POST['name']); ?>,
我今年<?php echo (int)$_POST['age']; ?>岁了！

My name is: <?php echo htmlspecialchars($_POST['name']), ",<br />"; ?>

I am <?php echo (int)$_POST['age'] ;?> years old!



My name is: <?php echo "<br /><br /><br /><br /><br /><br />", htmlspecialchars($_REQUEST['name']), ",<br />"; ?>

I am <?php echo (int)$_REQUEST['age'] ;?> years old!




