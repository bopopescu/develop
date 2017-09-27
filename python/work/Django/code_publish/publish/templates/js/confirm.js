//对一些操作的确认提示


function confirm_operate(id, _prompt, url){
    var obj = document.getElementById(id);
    td_value = trimStr(obj.innerHTML)
    reg_value = /^([\w\\\/]*\d{14})$/;
    flag_value = td_value.search(reg_value)
    if (td_value && flag_value){
        //alert(typeof (typeof 1) + "当前已是发布版本，不可回滚！");
        return false;
    }

    var flag = confirm(_prompt);
    if(flag){
        document.location.href = "/" + url + "/" + id;
    }
    //else{
    //    return false;
    //}
}

//删除产品
function delete_product(id){
    var flag = confirm(" 确定要删除吗？");
    if(flag){
        document.location.href = "/delete_product/" + id;
    }
    else{
        return false;
    }
}

//删除产品对应关系
function delete_product_management(product, user){
    var flag = confirm(" 确定要删除 '" + product + "' 与 '" + user + "' 的对应关系吗？");
    if(flag){
        document.location.href = "/delete_product_management/?product=" + product + "&user=" + user;
    }
    else{
        return false;
    }
}

function delete_friend(id){
    var obj = document.getElementById(id);
    var flag = confirm(" 确定要删除该好友吗? 删除之后，您和好友将互相看不到对方的信息");
    if(flag){
        document.location.href = "/delete_friend/" + id;
    }
    else{
        return false;
    }
}


//发布和回滚的操作相同，所以共用同一函数
function publish_revert(id, msg){
    var flag = confirm(msg);
    if(flag){
        open_dialog(id);
    }
    else{
        return false;
    }
}

//弹出输入域   no use 
function open_log_dialog(id){
    var msk_obj = document.getElementById("log_mask");
    var pop_obj = document.getElementById("log_pop");
    var changelog_obj = document.getElementById("changelog");
    var hidden_changelog_obj = document.getElementById("hidden_changelog" + id);
    msk_obj.style.display = "block";
    pop_obj.style.display = "block";
    changelog_obj.innerHTML = '<p id ="changelog">' + hidden_changelog_obj.value + "</p>";
    //msk_obj.innerHTML = "<input type='text' id = 'input_id' hidden value=" + id + ">"
}

//弹出输入域
function close_log_dialog(){
    var msk_obj = document.getElementById("log_mask");
    var pop_obj = document.getElementById("log_pop");
    pop_obj.style.display = "none";
    msk_obj.style.display = "none";
}

//弹出输入域
function open_dialog(id){
    var msk_obj = document.getElementById("mask");
    var pop_obj = document.getElementById("pop");
    msk_obj.style.display = "block";
    pop_obj.style.display = "block";
    msk_obj.innerHTML = "<input type='text' id = 'input_id' hidden value=" + id + ">"
}

//弹出输入域
function close_dialog(){
    var msk_obj = document.getElementById("mask");
    var pop_obj = document.getElementById("pop");
    pop_obj.style.display = "none";
    msk_obj.style.display = "none";
}

//发布和回滚的操作相同，所以共用同一函数
function do_publish_revert(){
    var log_obj = document.getElementById("log");
    var input_obj = document.getElementById("input_id");
    id = input_obj.value;
    changelog = log_obj.value
    if(!changelog){
        alert("请输入changelog")
        return false;
    }
    var revert_obj = document.getElementById(id + "publish_revert");
    //document.location.href = "/publish_revert/" + id + "?changelog="+changelog;
    $.ajax({
        type: "POST",
        url: "/publish_revert/" + id + "/",
        data: {"changelog": changelog},
        //success: function(data){alert("success")},
        //error: function(data){alert(data)},
        //beforeSend: function(){alert("before send")},
        complete:function(){window.location.reload(); alert("动作开始执行")},
        dataType: "html",
    });
    revert_obj.value = "发布中";
    revert_obj.disabled = true;
    close_dialog();
}
