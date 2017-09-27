//对一些操作的确认提示
//没有用到这个脚本

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

function delete_product(id){
    var obj = document.getElementById(id);
    var flag = confirm(" 确定要删除吗？");
    if(flag){
        document.location.href = "/delete_product/" + id;
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

function publish(id){
    var obj = document.getElementById(id + "publish");
    var flag = confirm(" 确定要发布吗? ");
    if(flag){
        
        changelog = prompt("请输入changelog: ", "")
        if(!changelog){
            alert("请输入changelog")
            return false;
        }
           
        obj.value = "发布中";
        obj.disabled = true;
        //document.location.href = "/publish/" + id + "?changelog="+changelog;
        $.ajax({
            type: "POST",
            url: "/publish/" + id + "/",
            data: {"changelog": changelog},
            //success: function(data){alert("success")},
            //error: function(data){alert(data)},
            dataType: "html"
        });
    }
    else{
        return false;
    }
}

function revert(id){
    var revert_obj = document.getElementById(id + "revert");
    var obj = document.getElementById(id);
    //td_value = trimStr(obj.innerHTML)
    td_value = obj.innerHTML
    //reg_value = /^([\w\\\/]*\d{14})$/;
    //flag_value = td_value.search(reg_value)
    //if (td_value && flag_value){
        //alert(typeof (typeof 1) + "当前已是发布版本，不可回滚！");
        //return false;
    //}
    var flag = confirm(" 确定要回滚吗? ");
    if(flag){
        changelog = prompt("请输入changelog: ", "回滚")
        if(!changelog){
            return false;
        }
        revert_obj.value = "回滚中";
        revert_obj.disabled = true;
        //document.location.href = "/revert/" + id + "?changelog="+changelog;
        $.ajax({
            type: "POST",
            url: "/revert/" + id + "/",
            data: {"changelog": changelog},
            //success: function(data){alert("success")},
            //error: function(data){alert(data)},
            dataType: "html"
        });
    }
    else{
        return false;
    }
}
