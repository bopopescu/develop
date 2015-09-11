<?php
    //�������ⲽ��
	//1���Ȼ���û�������ַ������ж��Ƿ�Ϊ��
	//2���ǿյĻ�����������������ַ���ת��Ϊ�ո�
	//3��Ȼ��ͨ��explode�����õ������飬ȥ���յ�Ԫ��
	//4��Ȼ��ʹ��implode����ƴ�ӳ��ַ�������Ϊ��ѯ������
	require_once("connectvars.php");
	//$test = implode(" or ", array(1));
	//echo $test;
	
	//�ú���������Ϊ�˽�����ѯ������
	function build_query($user_search, $sort){
		$search_query = "select * from job_risky";
		$where_clause = "";
		
		//replace the user search chars
		$clean_search = str_replace(","," ",$user_search);
		//explode������һ�����ֽ�Ϊһ������
		$clean_words = explode(" ", $clean_search);
		
		//remove the empty chars
		foreach ($clean_words as $word){
			if (!empty($word)){
				$where_list[] = "description LIKE '%$word%'";
			}
		}
		if (count($where_list) > 0){
			//implode����������ƴ�ӳ�һ���ַ���
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
	
	//��Ϊ�ǲ�ͬ�����ӣ�����Ҫ�в�ͬ�ĺ���������
	function generate_page_links($user_search,$sort,$cur_page,$num_pages){
		$page_links = "";
		//if this page is not the first page, generate the privious link
		$page_links .= $cur_page == 1 ? '<- ' : '<a href = "'.$_SERVER["PHP_SELF"].'?usersearch='.$user_search.'&sort='.$sort.'&cur_page='.($cur_page-1).'"><-</a> ';
		
		//loop through the pages generating the page number links
		for($i; $i <= $num_pages; $i++){
			$page_links .= $cur_page == $i ? " ".$i : '<a href = "'.$_SERVER["PHP_SELF"].'?usersearch='.$user_search.'&sort='.$sort.'&cur_page='.$i.'"> '.$i.' </a> ';
		}
		
		//if this page is not the last page,generate the "next" link
		$page_links .= $cur_page == $num_pages ? ' ->' : '<a href = "'.$_SERVER["PHP_SELF"].'?usersearch='.$user_search.'&sort='.$sort.'&cur_page='.($cur_page+1).'">-></a> ';
		return $page_links;
		
	}	
	
	
	//$total = 18;
	//$results_per_page = 3;
	//$num_pages = $total % $results_per_page ?ceil($total / $results_per_page):ceil(($total / $results_per_page));
	//$num_pages = ceil($total / $results_per_page);
	//echo $num_pages;
	//echo 18%3;
	
	//�ú�����Ϊ�����ɴ������ӵı���
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
		$dbc = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die("connect mysql error");
		$user_search = mysqli_real_escape_string($dbc, trim($_GET["usersearch"]));
		if (!empty($user_search)){	
			//get sort from the url
			$sort = $_GET["sort"];	
			
			//calculate pagination information
			$cur_page = isset($_GET["cur_page"]) ? $_GET["cur_page"]:1;
			$results_per_page = 5;
			$skip = ($cur_page - 1) * $results_per_page;

		    //deal with the chars from user entering
			$sort_links = generate_sort_links($user_search, $sort);
			$search_query = build_query($user_search, $sort);
			$result = mysqli_query($dbc, $search_query);
			$total = mysqli_num_rows($result);
			$num_pages = ceil($total / $results_per_page);
			$page_links = generate_page_links($user_search,$sort,$cur_page,$num_pages);

			$result = mysqli_query($dbc, $search_query) or die("query mysql error");
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
			echo $page_links;
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
	
?>