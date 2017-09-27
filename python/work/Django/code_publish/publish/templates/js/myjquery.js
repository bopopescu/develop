/*
   no use
   @author: xudedong
   @date: 2017/07/12
   @description: use jquery
*/
$(document).ready(function(){
    $("#updatei").click(function(){
        //alert("你好,我是jQuery!");
        if(!$("#product").val()){
            alert("不能为空,请务必选择一项产品");
            return false;
        }
        //$("#update").attr({"disabled": "true"});
        $("#update").val("更新中...");
    })
})

