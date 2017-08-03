//ajax分别以POST和GET方式来传送数据

$.ajax({
	type: "POST",
	url: "/revert/" + id + "/",
	data: {"changelog": changelog},
	success: function(data){alert("success")},
	error: function(data){alert(data)},
	dataType: "html"
});


$.ajax({
	type: "GET",
	url: "/revert/" + id + "/",
	data: {"changelog": changelog},
	success: function(data){alert("success")},
	error: function(data){alert(data)},
	dataType: "html"
});