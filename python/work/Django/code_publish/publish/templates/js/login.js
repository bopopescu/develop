function getColor(color){
    var obj = document.getElementById("first_div");
    obj.setAttribute("style", "background-color:"+color);
    //obj.style = "background-color:"+color;
}

function login(){
    var username_obj = document.getElementById("username");
    var password_obj = document.getElementById("password");
    if (!username_obj.value){
        alert("请输入用户名");
        return false;
    }
    if (!password_obj.value){
        alert("请输入密码");
        return false;
    }
  
    var login_obj = document.getElementById("login");
    login_obj.innerHTML = 'Loading<img src = "/static/image/loading.gif">'
}

