<?php
    session_start();
    //require_once("appvars.php");
	define("CAPTCHA_NUMCHARS",6);
	define("CAPTCHA_WIDTH",100);
	define("CAPTCHA_HEIGHT",20);
	
	//generate the random pass-phrase
	$pass_phrase = "";
	for($i=0;$i<CAPTCHA_NUMCHARS;$i++){
		$pass_phrase .= chr(rand(97,122));
	}
	
	//store the encrypted pass-phrase in a session variable
	$_SESSION["pass_phrase"] = sha1($pass_phrase);
	$_SESSION["pass_phrase"] = $pass_phrase;

	//create the image  创建一个空的图像
	$img = imagecreatetruecolor(CAPTCHA_WIDTH,CAPTCHA_HEIGHT);
	
	//set a white background with black text and gray graphics
	$bg_color = imagecolorallocate($img,255,255,255);       //white
	$text_color = imagecolorallocate($img,0,0,0);           //black
	$graphic_color = imagecolorallocate($img,64,64,64);     //dark gray
	
	//fill the background to white color
	imagefilledrectangle($img,0,0,CAPTCHA_WIDTH,CAPTCHA_HEIGHT,$bg_color);
	
	//draw some random lines
	for ($i=0;$i<5;$i++){
		imageline($img,0,rand() % CAPTCHA_HEIGHT,CAPTCHA_WIDTH,rand() % CAPTCHA_HEIGHT,$graphic_color);
	}
	
	//sprinkle in some random dots
	for($i=0;$i<50;$i++){
		imagesetpixel($img,rand() % CAPTCHA_WIDTH,rand() % CAPTCHA_HEIGHT,$graphic_color);
	}
	//imagestringup($img,3,0,0,"Sample text",$graphic_color);
	//draw the pass-phrase string
	imagettftext($img,18,0,5,CAPTCHA_HEIGHT - 5, $text_color,"C:\Windows\Fonts\Gisha.ttf",$pass_phrase);
	
	
	//output the image as a PNG using a header
	//因为是直接在内存中生成的PNG图像，所以需要调用header函数通过一个首部把他传送到浏览器
	header("Content-type: image/png");
	imagepng($img);
	
	//destroy the created picture  clean up
    imagedestroy($img);
?>