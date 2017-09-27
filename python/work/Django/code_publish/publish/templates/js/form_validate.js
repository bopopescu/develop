//表单验证

function MustSelectOne(){
    var obj = document.getElementById("product");
    if(!obj.value){
        alert("请选择产品");
        return false;
    }
    var up_obj = document.getElementById("update");
    up_obj.disabled = true;
    up_obj.value = "更新中...";
    up_obj.style.cursor = "not-allowed";
}

function MustSelectAll(){
    var user_obj = document.getElementById("user");
    var product_obj = document.getElementById("product");
    if(!(user_obj.value && product_obj.value)){
        alert("请选择选项");
        return false;
    }
    /*
    $.ajax({
            //type: "POST",
            //url: "/add_product_management/",
            //data: {"user": $("#user").val(), "product": $("#product").val()},
            //success: function(data){alert("success")},
            //error: function(data){alert(data)},
            //beforeSend: function(){alert("before send")},
            //complete:function(){window.location.reload(); alert("complete success");},
            //dataType: "html",
           });
    */
}

function NotEmpty(id){
    var obj = document.getElementById(id);
    if(!obj.value){
        alert("不能为空");
        return false;
    }
}

