<script>
 function createTable(){ 
     var div = document.getElementById("dd"); 
     var table = document.createElement("table");//创建table 
	 table.width = "100%";
	 
	 var row = table.insertRow();//创建一行 
	 var cell = row.insertCell();//创建一个单元 
	 cell.innerHTML="&nbsp;";
	 
	 var row1 = table.insertRow();//创建一行 
     var cell1 = row1.insertCell();//创建一个单元 
     cell1.width = "20%";//更改cell的各种属性 
	 cell1.innerHTML="<span style='color:red'>*</span>script_contents";
     cell1 = row1.insertCell();//创建一个单元 
     cell1.width = "80%";//更改cell的各种属性 
	 cell1.innerHTML='<textarea rows = 8% class = "class_size" name = "script_contents1"></textarea>'; 
     
	 
     var row2 = table.insertRow();//创建一行 
     var cell2 = row2.insertCell();//创建一个单元 
     cell2.width = "20%";//更改cell的各种属性 
	 cell2.innerHTML="<span style='color:red'>*</span>work_dir";
     cell2 = row2.insertCell();//创建一个单元 
     cell2.width = "80%";//更改cell的各种属性 
	 cell2.innerHTML="<input type = 'text' class = 'class_size'/>"; 
	 
	 var row3 = table.insertRow();//创建一行 
     var cell3 = row3.insertCell();//创建一个单元 
     cell3.width = "20%";//更改cell的各种属性 
	 cell3.innerHTML="<span style='color:red'>*</span>description";
     cell3 = row3.insertCell();//创建一个单元 
     cell3.width = "80%";//更改cell的各种属性 
	 cell3.innerHTML="<input type = 'text' class = 'class_size'/>";
	 
     div.appendChild(table);
 } 
 
function CreateInput(){
    document.getElementById("content").appendChild("<span>work_dir</span>");

    var input1 = document.createElement("input");
	input1.type = "text";
	input1.name = "test";
	document.getElementById("showText").appendChild(input1);
	
	var input2 = document.createElement("input");
	input2.type = "text";
	input2.name = "test";
	document.getElementById("showText").appendChild(input2);
	
	var textarea = document.createElement("textarea");
	document.getElementById("showText").appendChild(textarea);
}

  function add()                                   
  {       
          content1 = "script_content";
		  content2 = "work_dir";
		  content3 = "description";
          str1= '<input type="text" class = "class_size"  name=proportion>';
          str2= '<input type="text"  class = "class_size" name=proportion>';
		  textarea= '<textarea rows = 8% class = "class_size" name = "script_contents3"></textarea>';
		  window.content.innerHTML += content1 + "<br />" + content2 + "<br />" + content3
          window.ShowText.innerHTML += "<span style = 'color:red'>*</span>script_contents3" + 
		  textarea + "<br /><span style = 'color:red'>*</span>work_dir" + str1 + 
		  "<br \><span style = 'color:red'>*</span>description" + str2 + "<br />";
  }                                   
</script>