<?php
	//define ("YOUTUBE_URL","http://gdata.youtube.com/feeds/api/videos/-/alien/abduction/head/first");
	define ("YOUTUBE_URL","http://www.iqiyi.com");
	define ("NUM_VIDEOS",5);
	
	//read the xml data into an object
	$xml = simplexml_load_file(YOUTUBE_URL);
	
	$num_videos_found = count($xml->entry);
	if ($num_videos_found > 0){
		echo "<table><tr>";
		for($i = 0; $i < min($num_videos_found,NUM_VIDEOS); $i++){
			//get the title
			$entry = $xml->entry[$i];
			$media = $entry.children("http://search.yahoo.com/mrss/");
			$title = $medis -> group -> title;
			
			//get the duration in minutes and seconds, and then format it
			$yt = $media ->children();
			$attr = $yt -> duration -> attributes();
			$length_min = floor($attr["seconds"]/60);
			$length_sec = $attr["seconds"]%60;
			$length_formatted = $length_min . (($length_min != 1)?' minutes,':' minute,').$length_sec.(($length_sec != 1)?' seconds':' second');
			
			//get the video url
			$sttr = $media -> group -> player -> attributes();
			$video_url = $attr["url"];
			
			//get the thumbnail image url
			$attr = $media -> group -> thumbnail[0] -> attributes();
			$thumbnail_url = $attr["url"];
			
			//display the results for this entry
			echo '<td style = "vertical-align:bottom,text-align:center" width = "' .(100/NUM_VIDEOS).
			     '%"><a href = "' .$video_url .'">' .$title.'<br /><span style = "font-size:smaller">'.
				 $length_formatted . '</span><br /><img src="'.$thumbnail_url.'"/></a></td>';
		}
		echo "</tr></table>";
	}
	else{
		echo "<p>Sorry, no videos were found!</p>";
	}
?>
