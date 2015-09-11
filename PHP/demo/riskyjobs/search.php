<?php
    //搜索问题步骤
	//1：先获得用户输入的字符串，判断是否为空
	//2：非空的话，将串里面的特殊字符都转换为空格
	//3：然后通过explode处理后得到的数组，去除空的元素
	//4：然后使用implode函数拼接成字符串，作为查询的条件
	require_once("connectvars.php");
	//$test = implode(" or ", array(1));
	//echo $test;
	//该脚本共三个函数：1：建立查询条件；2：生成标题链接；3：生成分页导航连接
	
	//该函数功能是为了建立查询的条件
	function build_query($user_search, $sort){
		$search_query = "select * from job_risky";
		$where_clause = "";
		
		//replace the user search chars
		$clean_search = str_replace(","," ",$user_search);
		//explode函数将一个串分解为一个数组
		$clean_words = explode(" ", $clean_search);
		
		//remove the empty chars
		foreach ($clean_words as $word){
			if (!empty($word)){
				$where_list[] = "description LIKE '%$word%'";
			}
		}
		if (count($where_list) > 0){
			//implode函数将数组拼接成一个字符串
			$where_clause = implode(" OR ",$where_list);
			$search_query .= " WHERE $where_clause";
		}
		
		//sort the search query using the sort setting
		switch ($sort){
			case 1:
				$search_query .= " order by titile";
				break;
			case 2:
				$search_query .= " order by titile desc";
				break;
			case 3:
				$search_query .= " order by state";
				break;
			case 4:
				$search_query .= " order by state desc";
				break;
			case 5:
				$search_query .= " order by date_posted";
				break;
			case 6:
				$search_query .= " order by date_posted desc";
				break;
			default:
				//$search_query .= "";
		
		}
		return $search_query;
	}
	
	//生成分页导航连接； 因为是不同的链接，所以要有不同的函数来生成
	function generate_page_links($user_search,$sort,$cur_page,$num_pages){
		$page_links = "";
		//if this page is not the first page, generate the privious link
		if ($cur_page > 1){
			$page_links .= '<a href = "'.$_SERVER["PHP_SELF"].'?usersearch='.$user_search.'&sort='.$sort.'&cur_page='.($cur_page-1).'"><-</a> ';
		}
		else{
			$page_links .= '<- ';
		}
		
		//loop through the pages generating the page number links
		for($i; $i <= $num_pages; $i++){
			if ($cur_page == $i){
				$page_links .= " ".$i." ";
			}
			else{
				$page_links .= ' <a href = "'.$_SERVER["PHP_SELF"].'?usersearch='.$user_search.'&sort='.$sort.'&cur_page='.$i.'">'.$i.'</a> ';
			}
		}
		
		//if this page is not the last page,generate the "next" link
		if ($cur_page < $num_pages){
			$page_links .= ' <a href = "'.$_SERVER["PHP_SELF"].'?usersearch='.$user_search.'&sort='.$sort.'&cur_page='.($cur_page+1).'">-></a> ';
		}
		else{
			$page_links .= ' ->';
		}
		
		
		return $page_links;
	}	
	
	//该函数是为了生成带有链接的标题
	function generate_sort_links($user_search, $sort){
		$sort_links = "";
		switch ($sort){
			case 1:
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=2">Job Title</a></td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=3">Job State</a></td><td>Job Description</td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=5">Job Date Posted</a></td>';
				break;
			case 3:
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=1">Job Title</a></td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=4">Job State</a></td><td>Job Description</td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=5">Job Date Posted</a></td>';
				break;
			case 5:
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=1">Job Title</a></td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=3">Job State</a></td><td>Job Description</td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=6">Job Date Posted</a></td>';
				break;
			default:
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=1">Job Title</a></td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=3">Job State</a></td><td>Job Description</td>';
				$sort_links .= '<td><a href = "' . $_SERVER["PHP_SELF"] . '?usersearch=' . $user_search . '&sort=5&cur_page=' . $cur_page . '">Job Date Posted</a></td>';
				//break;
		}
		return $sort_links;
	}
	
	
	if (isset($_GET["usersearch"])){
		$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die(mysqli_error());
		$user_search = mysqli_real_escape_string($dbc, trim($_GET["usersearch"]));
		if (!empty($user_search)){	
			//get sort from the url
			$sort = $_GET["sort"];	
			
			//calculate pagination information
			$cur_page = isset($_GET["cur_page"]) ? $_GET["cur_page"]:1;
			$results_per_page = 5;
			$skip = (($cur_page - 1) * $results_per_page);

		    //deal with the chars from user entering
			$sort_links = generate_sort_links($user_search, $sort);
			$search_query = build_query($user_search, $sort);
			$result = mysqli_query($dbc, $search_query);
			$total = mysqli_num_rows($result);
			$num_pages = ceil($total / $results_per_page);
			//query again to get just the subset of results
			$query = $search_query ." Limit $skip, $results_per_page";
			//echo $query;
			$result = mysqli_query($dbc, $query) or die(mysqli_error());
			//echo $search_query;
			echo "<h1 align = 'center'>Search Results</h1><hr />";
			echo "<table width = '100%'>";
			
			echo "<tr>";
			echo $sort_links;
			echo "</tr>";
			/*echo $_SERVER["PHP_SELF"]."?usersearch=".$user_search . "&sort='state'";
			echo "<tr><td><a href = '".$_SERVER["PHP_SELF"]."?usersearch=".$user_search . "&sort=state" . "'<strong>Job ID</strong></a></td>".
			"<td><strong>Job Title</strong></td>".
			"<td><strong>Job City</strong></td>".
			"<td><strong>Job State</strong></td>".
			"<td><strong>Job Description</strong></td>".
			"<td><strong>Job Date Posted</strong></td></tr>";*/
			
			while ($row = mysqli_fetch_array($result)){
				//echo "<tr><td>".$row["job_id"]."</td>";
				echo "<tr><td>".$row["titile"]."</td>";
				//echo "<td>".$row["city"]."</td>";
				echo "<td>".$row["state"]."</td>";
				echo "<td>".substr($row["description"],0,10)."...</td>";
				echo "<td>".substr($row["date_posted"],0,10)."</td></tr>";
			}
			echo "</table>";
			//generate navigational page links if we have more than one page
			if ($num_pages > 1){
				$page_links = generate_page_links($user_search,$sort,$cur_page,$num_pages);
				echo $page_links;
			}
			
			echo "<hr />";
		mysqli_close($dbc);
		}
		else{
			echo "empty,<a href = 'search.html'>backup</a>!";
		}
		
	}
?>

<?php
	function replace_commas($str){
		$new_str = str_replace(","," ",$str);
		$new_str = str_replace("+"," ",$new_str);
		return $new_str;
	}
	$clean_str = replace_commas(array("ad,,,qqa","as"));
	print_r ($clean_str);
	
	$benefit_code = 1;
	switch($benefit_code){
		case 1:
			$benefits = "qqqqqqqqq";
			break;
		case 2:
			$benefits = "wwwwwwwwwww";
			break;
		case 3:
		case 4:
			$benefits = "eeeeeeeeeee";
			break;
		default:
			$benefits = "None";
	}
	echo $benefits,"<br />";
	
	$test1 = "Hello";
	echo $test1,"<br />";
	$test1 .= " World";
	echo $test1,"<br />";
	echo "**************************<br />";
	function checkbalance($balance){
		if ($balance < 1000){
			echo 1111111111,"<br />";
			throw new Exception("bbbbbbbb");
			throw new Exception("aaaaaaaaaaaa");
			throw new Exception("Balance is less than 1000");
		}
		else{
			echo 2222222;
		}
	}
	try{
		checkbalance(999);
	}

	catch(Exception $e){
		echo  $e->getMessage();
	}
	finally{
		echo  "<br />",66666,"<br />";
	}
	
	
?>