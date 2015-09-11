<div>1111111</div>
<?php
echo "Hello world";

// ... more code

// 脚本至此结束，并无 PHP 结束标记 
//脚本至此结束，并无 PHP 结束标记 
//脚本至此结束，并无 PHP 结束标记 
//脚本至此结束，并无 PHP 结束标记 
#脚本至此结束，并无 PHP 结束标记 
#脚本至此结束，并无 PHP 结束标记 
#脚本至此结束，并无 PHP 结束标记 
#脚本至此结束，并无 PHP 结束标记
?>

 

<p>This is going to be ignored by PHP and displayed by the browser.</p>
<?php echo 'While this is going to be parsed.'; ?>
<p>This will also be ignored by PHP and displayed by the browser.</p> 




<h3>This is an <?php  echo 'xudedong';?> 111</h3>
<p>The header above will say 'This is an  example'.</p> 


<?php
$a_bool = TRUE;   // a boolean
$a_str  = "foo";  // a string
$a_str2 = 'foo';  // a string
$an_int = -14;     // an integer

echo gettype($a_bool); // prints out:  boolean
echo "<br />",12345,"<br />";
echo gettype($a_str);  // prints out:  string
echo "<br />",67890,"<br />";
echo gettype($an_int);  // prints out:  string
echo "<br />",$an_int, " aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

// If this is an integer, increment it by four
if (is_int($an_int)) {
    $an_int += 4;
	echo "<br />","fushu";
	echo "<br />",$an_int;
}

if (is_string($a_str)){
	echo "<br />", $a_str,"<br />", 33;
}
if (is_bool($a_bool)){
	echo "<br />", $a_bool,"<br />", 44;
}
// If $bool is a string, print it out
// (does not print out anything)
if (is_string($a_bool)) {
    echo "String: $a_bool";
}

echo "<br />","****************************************";
settype($an_int, "boolean");
echo "<br />",$an_int;
echo "<br />",gettype($an_int);
?> 

<?php
$foo = True; // assign the value TRUE to $foo
if (1!=1){echo "aaaaaaaa";}
$foo = '6';
$foo += 2;
echo "<br />",$foo;
$foo += 1.3;
$foo = $foo + 1.9;
echo "<br />",$foo;
$foo = 5 + "10 Little Pig";
echo "<br />",$foo;

$foo = 5 + "10 Small Pig";
echo "<br />",$foo;

?> 

<?php
var_dump((bool) "");        // bool(false)
var_dump((bool) 1);         // bool(true)
var_dump((bool) -2);        // bool(true)
var_dump((bool) "foo");     // bool(true)
var_dump((bool) 2.3e5);     // bool(true)
var_dump((bool) array(12)); // bool(true)
var_dump((bool) array());   // bool(false)
var_dump((bool) "false");   // bool(true)
var_dump((bool) false);   // bool(true)
?> 

<?php
$var = 1/2;
settype($var,"boolean");
echo "<br />",gettype(1/2);
echo "<br />",intval(1/2);
echo "<br />",(int)(1.23);
echo "<br />",(int)(( 0.1+0.7)*10);
echo "<br />",(int)(( 0.1+0.8)*10);
echo "<br />",(int)(( 0.1+0.6)*10);
echo "<br />",(int)(( 0.1+0.9)*10);
?>

<?php
$a = 1.23456789;
$b = 1.23456780;
$ep = 0.00001;
if (abs($a-$b) < $ep){
	echo "<br />","true";
}

if ($a!=$b){
	echo "<br />","11111111111111";
}
?>

<?php
$nan = acos(8);
var_dump($nan, is_nan($nan));
echo "*****************************<br />";
echo rand(),"<br />";
echo log10(1000),"<br />";
echo log1p(1+0.000000000000000000000000000000001),"<br />";
echo log(16,2),"<br />";
?>

<?php
echo "+++++++++++++++++++++++++++++++++++++++++<br />";
echo max(1,2,3,4,5),"<br />";
echo max(array(1,2,3,4,5,5,4,7,3)),"<br />";
echo gettype(array(12,34,5)),"<br />";
echo max('42',3,"lit","qqq",'aaa','n'),"<br />";
echo max('hello', 0),"<br />";
echo max(0,'hello'),"<br />";
echo count(array(1,2,3,4,5,7,6,5,4,2,1)),"<br />";
echo "+++++++++++++++++++++++++++++++++++++++++<br />";
$val = max('string', array(2, 5, 7), 42);
echo $val;
echo max(0,"hello"),"<br />";
?>

<?php
function randomFloat($min = 0, $max = 1){
	return $min + mt_rand()/mt_getrandmax() * ($max - $min);
}
var_dump(randomFloat());
var_dump(randomFloat(2,20));
echo mt_rand(),"<br />";

for($i=0;$i<=10;$i++){
	echo $i,"<br />";
	echo "<BR>";
}
echo octdec('77');
echo "<BR>";
echo bindec('11');
echo "<BR>";
echo hexdec('11');
echo "<BR>";
//echo base_convert('77');
echo "<BR>";
echo octdec(decoct(45));
?>
<?php
$array = array(
"foo" => "bar",
"bar" => "foo",
);
echo var_dump($array);

$array1 = [
"foo" => "bar",
"bar" => "foo",
];
?>

<?php
$array = array(
    1    => "a",
    "1"  => "b",
    1.5  => "c",
    true => "d",
);
var_dump($array);
?> 

<?php
$array = array(
"1" => "test",
1 => "ddd",
"1.5" => "aaa",
1.5 => "www",
1 => "ttt",
);
var_dump($array);
echo $array[1],"qqqqqqqqqqqqqqq","<br />";
?>


<!--通过引用传递参数-->
<?php
function add_some_extra(&$string)
{
	$string .= '<>add something extra.';
}
$str = 'This is a string!';
add_some_extra($str);
echo $str;
?>

<!--在函数中使用默认参数-->
<?php
function makecoffee1($type = "cappuccino")
{
	return "Making a cup of $type.\n";
	
}
echo makecoffee1();
echo makecoffee1(null);
echo makecoffee1("xudedong"),"<BR>";
?>

<!--PHP 还允许使用数组 array 和特殊类型 NULL 作为默认参数，使用非标量类型作为默认参数,
默认值必须是常量表达式，不能是诸如变量，类成员，或者函数调用等。-->
<?php
function makecoffee($types = array("aaaaa"), $coffeeMaker = NULL)
{
	$device = is_null($coffeeMaker) ? "null":"hands,$coffeeMaker";
	return "Making a cup of ".join(",", $types)." with $device.\n";
}
echo makecoffee(),"<BR>";
echo 1111111111111111111111111111,"<BR>";
echo makecoffee(array("aaaaa", "bbbbb","ccc"), 'ttt');
?>

<!--注意当使用默认参数时，任何默认参数必须放在任何非默认参数的右侧；否则，函数将不会按照预期的情况工作。-->

<!--函数默认参数的不正确用法-->
<?php
function makeyogurt($type = "access",$flavour)
{
	return "Making a bowl of $type+++++++++++++++++++ $flavour.\n";
}
echo makeyogurt("dddddddddd"),"<BR>";
?>

<!--函数默认参数的正确用法-->
<?php
function makeyogurt1($flavour,$type = "access")
{
	return "Making a bowl of $type,,,,, $flavour.\n";
}
echo makeyogurt1("dddddddddd");
?>

<!--返回一个数组已得到多个返回值-->
<?php
function small_numbers()
{
    return array (0, 1, 2);
}
list ($zero, $one, $two) = small_numbers();
echo $zero, $one, $two
?>

<?php
function &returns_reference()
{
    return $someref;
}

$newref =& returns_reference();
echo $newref;
?> 


<!--用可变函数的语法来调用一个对象的方法-->
<?php
class Foo
{
    function Variable()
    {
        $name = 'Bar';
        $this->$name(); // This calls the Bar() method
    }

    function Bar()
    {
        echo "This is Bar,<br />";
    }
}

$foo = new Foo();
$funcname = "Variable";
$foo->$funcname();   // This calls $foo->Variable()
$foo->Variable();
?> 

<?php
function foo() {
    echo "In foo()<br />\n";
}

function bar($arg = '') {
    echo "In bar(); argument was '$arg'.<br />\n";
}

// 使用 echo 的包装函数
function echoit($string)
{
    echo $string;
	print("ddddddd,<br />");
	printf("hhhhhhhhhhhh,<br />");
}



$func = "foo";
$func();

$func = "bar";
$func("xudedong");


$func = "echoit";
$func("vcbnm");
?> 

<?php
class SimpleClass
{
    // property declaration
    public $var = 'a default value,<br />';

    // method declaration
    public function displayVar() {
        echo $this->var;
    }
}

$sim = new SimpleClass();
$sim->displayVar();

?> 









