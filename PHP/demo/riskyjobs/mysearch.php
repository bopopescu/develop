<?php
	$split_array = explode("  gre ","kl      gre                  sdfs wt er");
	echo $split_array;
	var_dump($split_array);
	
	$join_array = array(1,2,3);
	var_dump($join_array);
	$test = implode(" or ", $join_array);
	
	echo $test,"<br />";
	
	$search_query = "select * from search";
	$where_clause = "";
	$user_search = "qwe rty uio";
	$search_words = explode(" ", $user_search);
	$new_where_list = array();
	foreach($search_words as $word){
		$where_list[] = "description LIKE '%$word%'";
		array_push($new_where_list,"description LIKE '%$word%'");
	}
	
	$where_clause = implode(" OR ", $new_where_list);
	echo $where_clause,"<br /><br />";
	
	echo $search_query .= " where $where_clause";
    
	echo "<hr />";
	
	$search_query = "select * from search";
	$user_search = "tight, walker, circus";
	echo str_replace(","," ",$user_search);
	//echo explode(" ",$user_search);
	$search_words = explode(" ", $user_search);
	var_dump($search_words);
	$where_list = array();
	foreach ($search_words as $word){
		//$where_list[] = "name like '%$word%'";
		if (!empty($word)){
			array_push($where_list,"name like '%$word%'");
		}
	}
	$where_clause = implode(" OR ", $where_list);
	echo $search_query .= " where $where_clause"."<br />";
	
	$test = array();
	foreach ($test as $record){
		echo $record,"<br />";
	}
	
	echo '<a href = "mysearch.php">'.substr("qwertyuiop",0,4)."...</a>";
?>