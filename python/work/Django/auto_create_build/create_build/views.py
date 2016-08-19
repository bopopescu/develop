#-*- encoding:utf-8 -*- 
"""
    created by
    @作者: dedong.xu
    @日期: 2015-05-20
    @目的: 提供一个工具，让相关负责人自己去创建build，不参与他们的业务逻辑
"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import available_attrs
from django.core.exceptions import ValidationError
from django.utils import simplejson
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

import sys
from models import *
from forms import *
import os
import logging
import subprocess
import time
import smtplib
from email.mime.text import MIMEText
import settings
#from DjangoVerifyCode import Code
reload(sys)
sys.setdefaultencoding("utf8")


log = logging.getLogger("django")
temp_file = os.path.dirname(__file__) + "/temp_file.txt"

SEARCH_LIST = ["slavename", "buildername", "slave_platform", "buildip", "username"]

def checkslavename(request):
    slavename = request.POST.get("slavename", "").strip() 
    try:
        build_info_obj = Build_Info.objects.get(slavename__exact = slavename)
    except Exception, e:
        build_info_obj = ""
    prompt_slavename = "already exists!" if build_info_obj else ""
    return HttpResponse(prompt_slavename, content_type = "application/json")


def checkbuildername(request):
    buildername = request.POST.get("buildername", "").strip() 
    try:
        build_info_obj = Build_Info.objects.get(buildername__exact = buildername)
    except Exception, e:
        build_info_obj = ""
    prompt_buildername = "already exists!" if build_info_obj else ""
    return HttpResponse(prompt_buildername, content_type = "application/json")


@csrf_exempt
def register_old(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get("username","").strip()
            request.session["username"] = username
            return HttpResponseRedirect("/display_all_records/")
    else:
        form=UserForm()
    return render_to_response("register.html",locals())

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            #form.save()
            username = request.POST.get("username","").strip()
            password = request.POST.get("passwd","").strip()
            email = request.POST.get("email","").strip()
            request.session["username"] = username
            user = User.objects.create_user(username,email,password)
            user.save()
            return HttpResponseRedirect("/display_all_records/")
    else:
        form=UserForm()
    return render_to_response("register.html",locals())



@csrf_exempt
def login(request):
    if request.session.has_key("username"):
        return HttpResponseRedirect("/display_all_records/")
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        passwd = request.POST.get("passwd","").strip()
        user = auth.authenticate(username=username,password=passwd)
        if user is not None:
            auth.login(request, user)
            request.session["username"] = username
            return HttpResponseRedirect("/display_all_records/")
        else:
            return HttpResponse("<body style = 'background-color:#77ac98'><a href = ''>密码不正确,点击返回重新登录</a></body>")
        """
        try:
            register = Register.objects.get(username = username)
        except Exception,e:
            return HttpResponse("<body style = 'background-color:#77ac98'><a href = ''>用户名不存在,点击返回重新登录</a></body>")
            #raise forms.ValidationError("用户名不存在")
        if register.passwd == passwd:
            request.session["username"] = username
            return HttpResponseRedirect("/display_all_records/")
        else:
            return HttpResponse("<body style = 'background-color:#77ac98'><a href = ''>密码不正确,点击返回重新登录</a></body>")
        """
    return render_to_response("login.html", locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/navmenu/")
    return HttpResponseRedirect("/display_all_records/")


def logout_old(request):
    if request.session.has_key("username"):
        del request.session["username"]
        return HttpResponseRedirect("/login/")
        return HttpResponseRedirect("/display_all_records/")


def send_mails(to_list,sub,content):
    mail_host="10.10.7.100"  #set mail server
    mail_user="buildbot"    #usename
    mail_pass="123456"   #password
    mail_postfix="goland.cn"  #
    
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.starttls()  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()
        log.info("send mail successfully!")
        return True  
    except Exception, e:  
        print str(e) 
        log.info("send mail failed: %s" % str(e)) 
        return False


def get_passwd_page(request):
    return render_to_response("get_passwd.html",locals())

    
@csrf_exempt
def get_passwd(request):
    username = request.POST.get("username","").strip()
    email = request.POST.get("email","").strip()
    if username and email:
        try:
            #register = Register.objects.get(username = username)
            register = User.objects.get(username = username)
        except Exception,e:
            return HttpResponse("<body style = 'background-color:#77ac98'><a href = ''>用户名不存在,点击返回重新填写</a></body>")
        else:
            #passwd = register.passwd
            passwd = register.password
            content = "Hello,your password is: %s" % passwd
            title = "Find Password"
            send_mails([email],title,content)
        return render_to_response("get_passwd_success.html",locals())
        return HttpResponseRedirect("/get_passwd_page/")
    else:
        return render_to_response("get_passwd.html",locals())


def navmenu(request):
    return render_to_response("navmenu.html")


def params_required_old(request, func = None, redirect_field_name = REDIRECT_FIELD_NAME, login_url = None):
    product = request.GET.get("product", "").strip()
    if product.lower() not in ["vidon", "dvdfab"]:
        return HttpResponseRedirect("/navmenu/")
    actual_decorator = user_passes_test(redirect_field_name = redirect_field_name)#, login_url = None)
    if func:
        return actual_decorator(func)
        #func_result = func(request, *args, **kwargs)
        #if func_result:
        #    return func_result
    return actual_decorator


def params_required(func = None):
    from functools import wraps
    @wraps(func, assigned=available_attrs(func))
    def wrapper(request, *args, **kwargs):
        product = request.GET.get("product", "").strip()
        #assert product.lower() in ("vidon", "dvdfab")
        if product.lower() not in ["vidon", "dvdfab"]:
            return HttpResponseRedirect("/navmenu/")
        func_result = func(request, *args, **kwargs)
        if func_result:
            return func_result
    return wrapper


@params_required
def index(request):
    product = request.GET.get("product", "").strip()
    if request.session.has_key("username"):
        hours = [i for i in xrange(24)]
        minutes = [i for i in xrange(60)]
        return render_to_response("index.html",locals())
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")

def increase_file(filename, content):
    try:
        fp = open(filename, "a+")
        fp.write(content + "\n")
        fp.close()
    except Exception, e:
        log.info("increase file error: " + str(e))


def write_file_lines(filename, content_list):
    fp = open(filename, "w+")
    for each_line in content_list:
        fp.write(each_line)
    fp.close()


def write_file(filename, content):
    try:
        fp = open(filename, "w")
        fp.write(content)
        fp.close()
    except Exception, e:
        log.info("write file error: " + str(e))


def read_file(filename):
    try:
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
    except Exception, e:
        content = ""
        log.info("read file error: " + str(e))
    return content


def read_file_lines(filename):
    try:
        fp = open(filename, "r")
        all_lines = fp.readlines()
        fp.close()
    except Exception, e:
        all_lines = []
        log.info("read file lines error: " + str(e))
    return all_lines

def get_salt_cmd(slave_platform, slaveip, cmd):
    """get salt cmd"""        
    salt_cmd = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + cmd + '"'
    return salt_cmd


def is_salt_ok(slaveip, slave_platform):
    """test salt is ok"""
    is_salt_working = False
    salt_cmd = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" test.ping'
    process = subprocess.Popen(salt_cmd, stdout = subprocess.PIPE, shell = True)
    result_content = process.stdout.read()
    if "True" in result_content:
        is_salt_working = True
        log.info("salt is OK!")
    else:
        log.info("salt does not response!")
    return is_salt_working


def create_slave(masterip,master_port, slave_path,slaveip,slave_platform,slavename):
    """"create slave"""
    try:
        if slaveip == "10.10.2.97":
            create_slave_cmd = "C:/Python27/Scripts/buildslave create-slave " + slave_path + " " + masterip + ":9989 " + slavename + " 123456"
        else:
            create_slave_cmd = "buildslave create-slave " + slave_path + " " + masterip + ":" + master_port + " " + slavename + " 123456"
        salt_cmd = get_salt_cmd(slave_platform, slaveip, create_slave_cmd)
        os.system(salt_cmd)
        log.info("create slave: %s successfully!" % slavename)
    except Exception, e:
        log.info(str(e))   


def create_start_slave_script(slaveip, slave_platform,slave_source_path,slavename):
    if slave_platform == "Win":
        extend_name = ".bat"
        start_all_slave_cmd = "start .\\start_slave_" + slavename + extend_name
    else:
        extend_name = ""
        start_all_slave_cmd = "./start_slave_" + slavename + extend_name
    script_file = os.path.join(slave_source_path, "start_slave_" + slavename + extend_name)
    all_script_file = os.path.join(slave_source_path, "start_all_slave" + extend_name)
    if slaveip == "10.10.2.97":
        start_slave_cmd = "C:/Python27/Scripts/buildslave start ./" + slavename
    else:
        start_slave_cmd = "buildslave start ./" + slavename
    create_script_cmd = "echo " + start_slave_cmd + " > " + script_file
    salt_cmd = get_salt_cmd(slave_platform, slaveip, create_script_cmd)
    subprocess.Popen(salt_cmd, shell = True)
    create_all_script_cmd = "echo " + start_all_slave_cmd + " >> " + all_script_file
    salt_cmd = get_salt_cmd(slave_platform, slaveip, create_all_script_cmd)
    subprocess.Popen(salt_cmd, shell = True)
    return script_file


def start_slave_script(slaveip,slave_platform,slave_source_path,slavename):
    try:
        log.info("begin to start slave: %s!" % slavename)
        if slaveip == "10.10.2.97":
            start_slave_cmd = "C:/Python27/Scripts/buildslave start " + os.path.join(slave_source_path,slavename)
        else:
            start_slave_cmd = "buildslave start " + os.path.join(slave_source_path,slavename)
        salt_cmd = get_salt_cmd(slave_platform, slaveip, start_slave_cmd)
        subprocess.Popen(salt_cmd, shell = True)
        log.info("start slave cmd is: " + salt_cmd)
        log.info("start slave: %s successfully!" % slavename)
    except Exception, e:
        log.info(str(e))


def create_new_master(master_template,slaveip,gitpoller_file,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list):
    content = read_file(master_template)
    new_content = content.replace("slave_ip",slaveip).replace("buildername", buildername).replace("Slave_Name", slavename).replace("git_url", git_project_path).replace("branches_list", str(branches_list))\
                  .replace("monitor_file_path", monitor_file_path).replace("start_hour",hour).replace("start_minute",minute).replace("send_mail_list",str(send_mail_list))
    get_gitpoller(gitpoller_file, buildername, git_project_path, branches_list)
    write_file(new_master, new_content)
    log.info("create new master config file: %s successfully!" % new_master)

def get_gitpoller(gitpoller_file, buildername, git_project_path, branches_list):
    if os.path.exists(gitpoller_file):
        all_lines = read_file_lines(gitpoller_file)
        flag, branches_flag, update_gitpoller_flag = True, True, True
        new_list = []
        for each_line in all_lines:
            if not branches_flag:
                log.info("pass this line, because last loop already appended this line to the list")
                branches_flag = True
                continue
            if each_line.find(git_project_path) != -1:
                flag = False
                if each_line.strip().startswith("cs_gitpoller_" + buildername):
                    update_gitpoller_flag = False
                    log.info("the build %s already monitors the git project!  break the loop!" % buildername)
                    break
                log.info("%s is already monitored!" % git_project_path)
                cur_index = all_lines.index(each_line)
                branches_line = all_lines[cur_index + 1]
                if branches_line.find("branches") != -1:
                    branches_flag = False
                    new_list.append(each_line)
                    log.info(branches_line)
                    t = ""
                    for i in branches_list:
                        t += "' , '" + i
                    try:
                        each_line = branches_line.split("]")[0] + t[1:] + "'],\n"
                        log.info("append new branch to the monitored list!")
                    except Exception, e:
                        each_line = branches_line
                        log.info("append new branch exception: %s" % str(e))
                    log.info("new each line is: %s" % each_line)
                    new_list.append(each_line)
                    continue
                else:
                    log.info("exception: could not monitor the branches!")
            new_list.append(each_line)
        if flag:
            log.info("monitor new git project")
            new_content = '\ncs_gitpoller_buildername = GitPoller(repourl="git_url",\nbranches = branches_list,\
                          \npollInterval = 60,\ngitbin = "/usr/bin/git")\n\ncs_gitpoller_list.append(cs_gitpoller_buildername)'
            new_content = new_content.replace("buildername", buildername).replace("git_url", git_project_path).replace("branches_list", str(branches_list))
            increase_file(gitpoller_file, new_content)
        else:
            if update_gitpoller_flag:
                write_file_lines(gitpoller_file, new_list)
    else:
        new_content = 'from buildbot.changes.gitpoller import GitPoller\ncs_gitpoller_list = []\n\
                      \ncs_gitpoller_buildername = GitPoller(repourl="git_url",\nbranches = branches_list,\
                      \npollInterval = 60,\ngitbin = "/usr/bin/git")\n\ncs_gitpoller_list.append(cs_gitpoller_buildername)'
        new_content = new_content.replace("buildername", buildername).replace("git_url", git_project_path).replace("branches_list", str(branches_list))
        write_file(gitpoller_file, new_content)


def get_lock(locks_file, slaveip):
    ip = slaveip.strip().split(".")[-1]
    if os.path.exists(locks_file):
        all_lines = read_file_lines(locks_file)
        flag = True
        for each_line in all_lines:
            db_lock = "db_lock_" + ip + "="
            if each_line.strip().startswith(db_lock) or db_lock in each_line:
                flag = False
                log.info(db_lock[:-1] + " already exists!")
                break
        if flag:
            new_content = ""
            db_lock = "db_lock_" + ip
            new_content += "\n" + db_lock + "=locks.MasterLock('database_" + ip +  "')"
            new_content += "\nbuild_lock_dict['" + db_lock + "'] = "+ db_lock
            increase_file(locks_file, new_content)
    else:
        new_content = "from buildbot import locks"
        db_lock = "db_lock_" + ip
        new_content += "\n" + db_lock + "=locks.MasterLock('database_" + ip +  "')"
        new_content += "\nbuild_lock_dict['" + db_lock + "'] = " + db_lock
        write_file(locks_file, new_content)


def import_new_master(old_master,slaveip,buildername):
    new_list = []
    all_lines = read_file_lines(old_master)
    for each_line in all_lines:
        if each_line.startswith("c = BuildmasterConfig = {}"):
            each_line += "\nimport master_" + buildername
        new_list.append(each_line)
        
    new_list.append("c = master_" + buildername + ".update_params_dict(c)\n")
    try:   
        write_file_lines(old_master, new_list) 
        log.info("import new master config file: master_%s to main conf file successfully!" % buildername)
    except Exception,e:
        log.info("import new master error: " + str(e))

def create_new_factory(build_info_id,slave_platform,factory_template,new_factory):
    content = read_file(factory_template)
    new_content = content.replace("var_build_info_id", str(build_info_id)).replace("var_slave_platform", slave_platform)
    write_file(new_factory, new_content)
    log.info("create or update factory!")

def restart_master(product):
    current_path = "/home/goland/buildbot"
    if product.lower() == "vidon":
        restart_master_cmd = "buildbot restart master"
    else:
        restart_master_cmd = "buildbot restart DVDFab_master"
    subprocess.Popen(restart_master_cmd, cwd = current_path, shell = True)
    log.info("I am here: restart master cmd is: %s" % restart_master_cmd)


def deal_with_data(input_data):
    data_list = []
    input_data = input_data.replace(",",";")
    for each_data in input_data.split(";"):
        if each_data.strip():
            data_list.append(each_data.strip().decode().encode())
    return data_list


def get_params(slave_platform,slavename,buildername,product = None):
    if product and product.lower() == "vidon":
        old_master = "/home/goland/buildbot/master/master.cfg"
        locks_file = "/home/goland/buildbot/master/locks.py"
        gitpoller_file = "/home/goland/buildbot/master/gitpoller.py"
        master_template = "/home/goland/buildbot/master/master_template.cfg"
        factory_template = "/home/goland/buildbot/master/factory_template.py"
        new_master = "/home/goland/buildbot/master/master_" + buildername + ".py"
        new_factory = "/home/goland/buildbot/master/dvdfab_factory_" + buildername + ".py"
        builder_waterfall_address = "http://10.10.2.64:8010/waterfall?show=" + buildername
    else:
        old_master = "/home/goland/buildbot/DVDFab_master/master.cfg"
        locks_file = "/home/goland/buildbot/DVDFab_master/locks.py"
        gitpoller_file = "/home/goland/buildbot/DVDFab_master/gitpoller.py"
        master_template = "/home/goland/buildbot/DVDFab_master/master_template.cfg"
        factory_template = "/home/goland/buildbot/DVDFab_master/factory_template.py"
        new_master = "/home/goland/buildbot/DVDFab_master/master_" + buildername + ".py"
        new_factory = "/home/goland/buildbot/DVDFab_master/dvdfab_factory_" + buildername + ".py"
        builder_waterfall_address = "http://10.10.2.64:8020/waterfall?show=" + buildername
        
    if slave_platform.upper() == "WIN":
        slave_source_path = "X:/"
        slave_scripts_path = "d:/Buildbot_DVDFab/tool/scripts"
    elif slave_platform.upper() == "MAC":
        slave_source_path = "/Volumes/DATA"
        slave_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool/scripts"
    elif slave_platform.upper() == "UBU":
        slave_source_path = "/home/goland/buildbot"
        slave_scripts_path = "/home/goland/buildbot/tool/scripts"
    src_scripts_path = "/home/goland/buildbot/scripts"
    scripts_path = os.path.join(src_scripts_path,slavename)
    return old_master,locks_file,gitpoller_file,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,slave_scripts_path,builder_waterfall_address


def git_commit(src_scripts_path, scripts_path, slavename, slaveip, slave_platform, message):
    git_pull_cmd = "git pull"    
    git_add_cmd = "git add " + scripts_path    
    git_commit_cmd = "git commit %s -m '%s %s'" % (scripts_path, message, slavename)
    git_push_cmd = "git push origin master"
    cmd_list = [git_pull_cmd, git_add_cmd, git_commit_cmd, git_push_cmd]
    for cmd in cmd_list:
        subprocess.call(cmd, cwd = src_scripts_path, shell = True)


def git_clone(slave_scripts_path,slavename,slaveip,slave_platform):
    git_url = "git@10.10.2.31:autobuild/auto_build.git"
    git_clone_cmd = "git clone " + git_url + " " + slave_scripts_path
    salt_cmd_git_clone = get_salt_cmd(slave_platform, slaveip, git_clone_cmd)
    log.info("git clone cmd is: " + git_clone_cmd)    

    p2 = subprocess.Popen(salt_cmd_git_clone, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out2 = p2.stdout.read()
    err2 = p2.stderr.read()
    log.info("out2 " + out2)
    log.info("err2 " + err2)
    log.info("salt cmd git clone: " + salt_cmd_git_clone)
    log.info("git clone successfully!")

def git_pull(slave_scripts_path, slaveip, slave_platform):
    git_pull_cmd = "git pull "# + slave_scripts_path
    salt_cmd = get_salt_cmd(slave_platform, slaveip, git_pull_cmd)
    subprocess.Popen(salt_cmd, cwd = slave_scripts_path, shell = True)
    

def get_submit_script_content_values(post_dict):
    flag_str = "script_content"
    temp_list = []
    script_content_list = []
    for each_key in post_dict.keys():
        if flag_str in each_key:
            temp_each_key = each_key.replace(flag_str,"")
            try:
                temp_list.append(int(temp_each_key))
            except Exception,e:
                temp_list.append(float(temp_each_key))
    for record in sorted(temp_list):
        script_content_list.append(flag_str + str(record))
    log.info("script content list is: " + str(script_content_list)) 
    
    #script_content_list = sorted([i.replace(".","__") for i in post_dict.keys() if "script_content" in i])
    return script_content_list

def get_submit_script_content_values_new(post_dict):
    script_content_list = sorted([i.replace(".","__") for i in post_dict.keys() if "script_content" in i])
    return script_content_list


def format_file(temp_file, script_file):
    all_lines = read_file_lines(temp_file)
    fp = open(script_file, "w")
    for each_line in all_lines:
        fp.write(each_line.strip("\r\n") + "\n")
        #fp.write(each_line.strip("\r\n"))
    fp.close()


def test_salt(request):
    platform_list = ["", "win", "mac", "ubu"]
    context = {}
    context["platform_list"] = platform_list
    if request.method == "POST":
        slaveip = request.POST.get("slaveip","").strip()
        slave_platform = request.POST.get("slave_platform","").strip()
        cmd = 'echo "123456"|sudo -S salt "' + slave_platform + '_' + slaveip + '" test.ping'
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True) 
        result_content = process.stdout.read()
        if "True" not in result_content:
            test_result = "Salt minion not response!"
        else:
            test_result = "Salt minion is OK!"
        context["slaveip"] = slaveip
        context["slave_platform"] = slave_platform
        context["test_result"] = test_result
    
    return render_to_response("test_salt.html", context)


def get_master_port(product):
    product_dict = {"vidon":"9989", "dvdfab":"9999"}
    if product.lower() in product_dict:
        master_port = product_dict[product.lower()]
    else:
        master_port = ""
    return master_port


@csrf_exempt
def create_new_slave(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        masterip = request.POST.get("masterip", "").strip()
        product = request.POST.get("product", "").strip()
        slaveip = request.POST.get("slaveip", "").strip()
        slave_platform = request.POST.get("slave_platform", "").strip()
        slavename = request.POST.get("slavename", "").strip()
        buildername = request.POST.get("buildername", "").strip()
        master_port = get_master_port(product)
        old_master,locks_file,gitpoller_file,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,slave_scripts_path,builder_waterfall_address = get_params(slave_platform,slavename,buildername,product)
        slave_path = os.path.join(slave_source_path, slavename)
        create_slave(masterip,master_port,slave_path,slaveip,slave_platform,slavename)
        git_clone(slave_scripts_path,slavename,slaveip,slave_platform)
        create_start_slave_script(slaveip, slave_platform,slave_source_path,slavename)
        start_slave_script(slaveip,slave_platform,slave_source_path,slavename)
        log.info("create slave %s successfully!" % slavename)
        content = "Hello, " + username + u"创建新的" + "build: " + buildername
        title = "创建" + "build".encode("utf-8")
        send_mails(["dedong.xu@goland.cn"],title,content)
        return render_to_response("success.html",{"builder_waterfall_address":builder_waterfall_address})
    return render_to_response("create_slave.html")

def get_other_length(start_method, start_method_dict):
    if start_method in start_method_dict:
        other_length = start_method_dict[start_method]
    else:
        other_length = start_method_dict["radio_manual"]
    return other_length


def get_last_id():
    obj = Build_Info.objects.latest("id")
    #obj = Build_Info.objects.all()[0]
    build_info_id = obj.id if obj else ""
    return build_info_id


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, mode = 0777)


@csrf_exempt
def create_new_build(request):
    product = request.POST.get("product", "").strip()
    masterip = request.POST.get("masterip", "").strip()
    slaveip = request.POST.get("slaveip", "").strip()
    slave_platform = request.POST.get("slave_platform", "").strip()
    slavename = request.POST.get("slavename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    start_method = request.POST.get("start_method", "").strip()
    new_path = request.POST.get("new_path", "").strip()
    old_path = request.POST.get("old_path", "").strip()
    username = request.session["username"]
    hour = request.POST.get("hour", "200").strip()
    minute = request.POST.get("minute", "200").strip()
    empty_path = "git_project_path_" + buildername
    git_project_path = request.POST.get("git_project_path", empty_path).strip()
    branches = request.POST.get("branches", "branches").strip()
    monitor_file_path = request.POST.get("monitor_file_path", "monitor_file_path").strip()
    send_mail = request.POST.get("send_mail", "").strip()
    script_content1 = request.POST.get("script_content1", "").strip()
    work_dir1 = request.POST.get("work_dir1", "").strip()
    description1 = request.POST.get("description1", "").strip()
    
    master_port = get_master_port(product)
    if len(request.POST.values()) == 0 or not start_method:
        return render_to_response("error.html")
    for each_key in request.POST.keys():
        if not request.POST[each_key].strip() and each_key != "old_path" and each_key != "new_path":
            return render_to_response("error.html")
    slave_count = Build_Info.objects.filter(product__iexact = product).filter(slavename = slavename).count()
    if slave_count >= 1:
        context = {"request" : request, "var_name" : "slave"}
        return render_to_response("duplicate.html",context)

    builder_count = Build_Info.objects.filter(product__iexact = product).filter(buildername = buildername).count()
    if builder_count >= 1:
        context = {"request" : request, "var_name" : "builder"}
        return render_to_response("duplicate.html",context)
    
    old_master,locks_file,gitpoller_file,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,slave_scripts_path,builder_waterfall_address = get_params(slave_platform,slavename,buildername, product)
    build_info = Build_Info(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename, buildername = buildername,start_method = start_method,\
                            username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,monitor_file_path = monitor_file_path,\
                            send_mail = send_mail, flag = 1, new_master = new_master, new_factory = new_factory,scripts_path = scripts_path, product = product)
    build_info.save()
    
    build_info_id = get_last_id()
    all_length = len(request.POST)
    start_method_dict = {"radio_timing":11, "radio_trigger":12, "radio_manual":9}
    other_length = get_other_length(start_method, start_method_dict)
    table_length = all_length - other_length

    script_content_list = get_submit_script_content_values(request.POST)
    if table_length > 0:
        num = 1
        for each_key in script_content_list:
            each_num = each_key.replace("script_content","")
            create_folder(scripts_path)
            filename = "script" + str(num) + ".bat" if slave_platform == "Win" else "script" + str(num) + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/") 
            slave_script_file = os.path.join(os.path.join(slave_scripts_path,slavename), filename).replace("\\","/")
            write_file(temp_file, request.POST[each_key].strip())
            format_file(temp_file, script_file)
            if new_path and old_path:
                workdir = request.POST["work_dir" + each_num].replace(old_path, new_path)
            else:
                workdir = request.POST["work_dir" + each_num]
            build_steps = Build_Steps(build_info_id = build_info_id, script_content = script_file,slave_script_file = slave_script_file, \
                                  work_dir = workdir, description = request.POST["description" + each_num])
            build_steps.save()
            num += 1
    log.info("-----------------------------begin----------------------------------\n")
    log.info("master ip is: %s" % masterip)
    log.info("build ip is: %s" % slaveip)
    log.info("build platform is: %s" % slave_platform)
    log.info("slavename is: %s" % slavename)
    log.info("buildername is: %s" % buildername)
    git_commit(src_scripts_path,scripts_path,slavename,slaveip, slave_platform, "new add for")
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    log.info(send_mail_list)
    create_new_master(master_template,slaveip,gitpoller_file,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list)
    import_new_master(old_master,slaveip,buildername)
    get_lock(locks_file, slaveip)
    create_new_factory(build_info_id,slave_platform,factory_template,new_factory)
    restart_master(product)
    slave_path = os.path.join(slave_source_path, slavename)
    is_salt_working = is_salt_ok(slaveip, slave_platform)
    if is_salt_working:
        create_slave(masterip,master_port,slave_path,slaveip,slave_platform,slavename)
        git_clone(slave_scripts_path,slavename,slaveip,slave_platform)
        create_start_slave_script(slaveip, slave_platform,slave_source_path,slavename)
        start_slave_script(slaveip,slave_platform,slave_source_path,slavename)
        log.info("-----------------------------end----------------------------------\n")
        content = "Hello, " + username + u" 创建新的" + "build: " + buildername
        title = "创建" + "build".encode("utf-8")
        send_mails(["dedong.xu@goland.cn"],title,content)
        return render_to_response("success.html",{"builder_waterfall_address":builder_waterfall_address})
    else:
        log.info("Sorry, do not create slave: %s" % slavename)
        title = "create slave: %s failed!" % slavename
        content = "<a href = 'http://www.baidu.com'>Hello</a>, perhaps because of salt minion does not response, the master created slave failed!\n\
		           先测试salt是否OK,地址:http://10.10.2.64:9000/test_salt/,\n\
				   OK的话，就去创建刚才的slave,地址:http://10.10.2.64:9000/create_new_slave/,\n\
				   记住slavename和buildername一定要和刚才的名字一致!"
        send_mails(["dedong.xu@goland.cn"],title,content)
        return HttpResponse("<span>不能创建slave!可能是salt minion无响应，请点击<a href = '/test_salt/'></span><span style = 'font-size:2.0em'>测试salt minion</a></span><span>，如果无响应，请联系徐德东！</span>")


def copy_build_info_page(request, params):
    if request.session.has_key("username"):
        product = request.GET.get("product", "").strip()
        hours = [i for i in xrange(24)]
        minutes = [i for i in xrange(60)]
        build_info= Build_Info.objects.get(id = params)
        build_steps = Build_Steps.objects.filter(build_info_id = params)
        all_list = []
        for each_record in build_steps:
            context = {}
            script_file = each_record.script_content
            content = read_file(script_file)
            context["script_content"] = content
            context["work_dir"] = each_record.work_dir
            context["description"] = each_record.description
            all_list.append(context)
        if build_info.hour:
            build_info_hour = int(build_info.hour)
            build_info_minute = int(build_info.minute)
        return render_to_response("copy_build_info.html", locals())
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")

@csrf_exempt
def copy_build(request, params):
    cur_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    product = request.GET.get("product", "").strip()
    masterip = request.POST.get("masterip", "").strip()
    slaveip = request.POST.get("slaveip", "").strip()
    slave_platform = request.POST.get("slave_platform", "").strip()
    slavename = request.POST.get("slavename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    start_method = request.POST.get("start_method", "").strip()
    #username = request.POST.get("username", "").strip()
    username = request.session["username"]
    hour = request.POST.get("hour", "200").strip()
    minute = request.POST.get("minute", "200").strip()
    empty_path = "git_project_path_" + buildername
    git_project_path = request.POST.get("git_project_path", empty_path).strip()
    branches = request.POST.get("branches", "branches").strip()
    monitor_file_path = request.POST.get("monitor_file_path", "monitor_file_path").strip()
    send_mail = request.POST.get("send_mail", "").strip()
   
    new_master = request.POST.get("new_master","").strip()
    new_factory = request.POST.get("new_factory","").strip()
    scripts_path = request.POST.get("scripts_path","").strip()
    
    master_port = get_master_port(product)
    if len(request.POST.values()) == 0 or not start_method:
        return render_to_response("error.html")
    for each_value in request.POST.values():
        if not each_value.strip():
            return render_to_response("error.html")
    slave_count = Build_Info.objects.filter(product__iexact = product).filter(slavename = slavename).count()
    if slave_count >= 1:
        var_name = "slave"
        context = {"request":request, "var_name":var_name}
        return render_to_response("duplicate.html",context)

    builder_count = Build_Info.objects.filter(product__iexact = product).filter(buildername = buildername).count()
    if builder_count >= 1:
        var_name = "builder"
        context = {"request":request, "var_name":var_name}
        return render_to_response("duplicate.html",context)
    
    old_master,locks_file,gitpoller_file,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,slave_scripts_path,builder_waterfall_address = get_params(slave_platform,slavename,buildername, product)
    build_info = Build_Info(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename, buildername = buildername,start_method = start_method,\
                            username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,monitor_file_path = monitor_file_path,\
                            send_mail = send_mail, flag = 1, new_master = new_master, new_factory = new_factory,scripts_path = scripts_path, product = product)
    build_info.save()
    
    build_info_id = get_last_id()
    all_length = len(request.POST)
    start_method_dict = {"radio_timing":9, "radio_trigger":10, "radio_manual":7}
    other_length = get_other_length(start_method, start_method_dict)
    table_length = all_length - other_length

    script_content_list = get_submit_script_content_values(request.POST)
    if table_length > 0:
        num = 1
        for each_key in script_content_list:
            each_num = each_key.replace("script_content","")
            create_folder(scripts_path)
            filename = "script" + str(num) + ".bat" if slave_platform == "Win" else "script" + str(num) + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/") 
            slave_script_file = os.path.join(os.path.join(slave_scripts_path,slavename), filename).replace("\\","/")
            write_file(temp_file, request.POST[each_key].strip())
            format_file(temp_file, script_file)
            build_steps = Build_Steps(build_info_id = build_info_id, script_content = script_file,slave_script_file = slave_script_file, \
                                  work_dir = request.POST["work_dir" + each_num], description = request.POST["description" + each_num])
            build_steps.save()
            num += 1
    log.info("-----------------------------begin----------------------------------\n")
    log.info("master ip is: %s" % masterip)
    log.info("build ip is: %s" % slaveip)
    log.info("build platform is: %s" % slave_platform)
    log.info("slavename is: %s" % slavename)
    log.info("buildername is: %s" % buildername)
    git_commit(src_scripts_path,scripts_path,slavename,slaveip, slave_platform, "new add for")
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    log.info(send_mail_list)
    create_new_master(master_template,slaveip,gitpoller_file,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list)
    import_new_master(old_master,slaveip,buildername)
    get_lock(locks_file, slaveip)
    create_new_factory(build_info_id,slave_platform,factory_template,new_factory)
    restart_master(product)
    slave_path = os.path.join(slave_source_path, slavename)
    is_salt_working = is_salt_ok(slaveip, slave_platform)
    if is_salt_working:
        create_slave(masterip,master_port,slave_path,slaveip,slave_platform,slavename)
        git_clone(slave_scripts_path,slavename,slaveip,slave_platform)
        create_start_slave_script(slaveip, slave_platform,slave_source_path,slavename)
        start_slave_script(slaveip,slave_platform,slave_source_path,slavename)
        log.info("-----------------------------end----------------------------------\n")
        content = "Hello, " + username + u" 复制新的" + "build: " + buildername
        title = "复制" + "build".encode("utf-8")
        send_mails(["dedong.xu@goland.cn"],title,content)
        return render_to_response("success.html",{"builder_waterfall_address":builder_waterfall_address})
    else:
        log.info("Sorry, do not create slave: %s" % slavename)
        title = "copy slave failed!"
        content = "Hello, perhaps because of salt minion does not response, the master created slave failed!"
        send_mails(["dedong.xu@goland.cn"],title,content)
        return HttpResponse("<span>不能创建slave!可能是salt minion无响应，请点击<a href = '/test_salt/'></span><span style = 'font-size:2.0em'>测试salt minion</a></span><span>，如果无响应，请联系徐德东！</span>")
        

def search_result(product, search_name, record_name, flag):
    build_info = Build_Info.objects.filter(product = product)
    record_list = ["slavename", "buildername", "slave_platform", "buildip", "username"]
    for record in record_list:
        if search_name == record:
            search_str = "%s like '%%%%%s%%%%'" % (search_name, str(record_name))
            temp_build_info = build_info.extra(where = [search_str])
            break
        else:
            temp_build_info = build_info
    build_info = temp_build_info.filter(flag = 1) if flag == 1 else temp_build_info

    return build_info     

def fenye(nowpage, build_info):
    per_page_count = 20
    nowpage = 1 if nowpage == "" else int(nowpage)
    count = build_info.count()
    if count % per_page_count == 0:
        pageall = count / per_page_count
    else:
        pageall = count / per_page_count + 1
    pageup = 1 if nowpage <= 1 else nowpage - 1
    if nowpage + 1 >= pageall:
        pagedn = pageall
    else:
        pagedn = nowpage + 1
    start = per_page_count * (nowpage - 1)        
    build_info = build_info[start: (start + per_page_count)]
    return build_info, nowpage, pageall, pageup, pagedn

@params_required
def display_all_records(request):
    search_list = SEARCH_LIST
    product = request.GET.get("product", "").strip()
    search_name = request.GET.get("search_name", "").strip()
    record_name = request.GET.get("record_name", "").strip()
    build_info = search_result(product, search_name, record_name, 2)
    nowpage = request.GET.get("nowpage","").strip()
    build_info, nowpage, pageall, pageup, pagedn = fenye(nowpage, build_info)
    return render_to_response("display_all_records.html", locals())


@params_required
def display_all_used_records(request):
    search_list = SEARCH_LIST
    product = request.GET.get("product", "").strip()
    search_name = request.GET.get("search_name", "").strip()
    record_name = request.GET.get("record_name", "").strip()
    build_info = search_result(product, search_name, record_name, 1) 
    all_length = len(build_info)
    nowpage = request.GET.get("nowpage","").strip()
    build_info, nowpage, pageall, pageup, pagedn = fenye(nowpage, build_info)
    return render_to_response("display_all_used_records.html", locals())

#display each record details
def display_details(request,params):
    product = request.GET.get("product", "").strip()
    build_info = Build_Info.objects.get(id = params)
    build_steps = Build_Steps.objects.filter(build_info_id = params)
    all_counts = build_steps.count()
    all_list = []
    for each_record in build_steps:
        context = {}
        script_file = each_record.script_content
        content = read_file(script_file)
        context["script_content"] = content
        context["work_dir"] = each_record.work_dir
        context["description"] = each_record.description
        all_list.append(context)
    return render_to_response("display_details.html", locals())


def empty(request):
    return render_to_response("empty.html")


def update_info_page(request, params):
    if request.session.has_key("username"):
        product = request.GET.get("product", "").strip()
        hours = [i for i in xrange(24)]
        minutes = [i for i in xrange(60)]
        build_info= Build_Info.objects.get(id = params)
        build_steps = Build_Steps.objects.filter(build_info_id = params)
        all_list = []
        for each_record in build_steps:
            context = {}
            script_file = each_record.script_content
            content = read_file(script_file)
            context["script_content"] = content
            context["work_dir"] = each_record.work_dir
            context["description"] = each_record.description
            all_list.append(context)
        if build_info.hour:
            build_info_hour = int(build_info.hour)
            build_info_minute = int(build_info.minute)
        return render_to_response("update_info.html", locals())
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")


@csrf_exempt
def update_info(request,params):
    product = request.GET.get("product", "").strip()
    build_info = Build_Info.objects.filter(id=params)
    build_steps = Build_Steps.objects.filter(build_info_id=params)
    masterip = request.POST.get("masterip", "").strip()
    slaveip = request.POST.get("slaveip", "").strip()
    slave_platform = request.POST.get("slave_platform", "").strip()
    slavename = request.POST.get("slavename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    start_method = request.POST.get("start_method", "").strip()
    username = request.POST.get("username", "").strip()
    #username = request.session["username"]
    hour = request.POST.get("hour", "200").strip()
    minute = request.POST.get("minute", "200").strip()
    empty_path = "git_project_path_" + buildername
    git_project_path = request.POST.get("git_project_path", empty_path).strip()
    branches = request.POST.get("branches", "branches").strip()
    monitor_file_path = request.POST.get("monitor_file_path", "monitor_file_path").strip()
    send_mail = request.POST.get("send_mail", "").strip()
   
    new_master = request.POST.get("new_master","").strip()
    new_factory = request.POST.get("new_factory","").strip()
    scripts_path = request.POST.get("scripts_path","").strip()
         
    for each_value in request.POST.values():
        if not each_value.strip():
            return render_to_response("update_error.html", locals())

    log.info("-----------------------------begin----------------------------------\n")
    build_info.update(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename,buildername = buildername,\
                      start_method = start_method,username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,\
                      monitor_file_path = monitor_file_path,send_mail = send_mail, flag = 1)

    old_master,locks_file,gitpoller_file,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,slave_scripts_path,builder_waterfall_address = get_params(slave_platform,slavename,buildername, product)
    all_length = len(request.POST)
    all_count = build_steps.count()

    #delete old steps before save new steps
    for each_build_step in build_steps:
        each_step = Build_Steps.objects.get(id = each_build_step.id)
        each_step.delete()

    script_content_list = get_submit_script_content_values(request.POST)
    num = 1
    for each_key in script_content_list:
        each_num = each_key.replace("script_content","")
        create_folder(scripts_path)
        filename = "script" + str(num) + ".bat" if slave_platform == "Win" else "script" + str(num) + ".sh"
        script_file = os.path.join(scripts_path, filename).replace("\\","/")
        slave_script_file = os.path.join(os.path.join(slave_scripts_path,slavename), filename).replace("\\","/")
        write_file(temp_file, request.POST[each_key].strip())
        format_file(temp_file, script_file)
        build_steps = Build_Steps(build_info_id = params, script_content = script_file,slave_script_file = slave_script_file,\
                                  work_dir = request.POST["work_dir" + each_num].strip(), description = request.POST["description" + each_num].strip())
        build_steps.save()
        num += 1

    log.info("update success!!")
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    create_new_master(master_template,slaveip,gitpoller_file,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list)
    create_new_factory(params,slave_platform,factory_template,new_factory)
    git_commit(os.path.dirname(scripts_path), scripts_path, slavename,slaveip,slave_platform, "update for")
    restart_master(product)
    log.info("-----------------------------end----------------------------------\n")
    #reload(sys)
    #sys.setdefaultencoding("utf8")
    content = "Hello, %s 修改build: %s" % (username, buildername)
    title = "修改build"
    send_mails(["dedong.xu@goland.cn"],title,content)
    return render_to_response("update_success.html",{"builder_waterfall_address":builder_waterfall_address})


def delete_files(filename):
    if os.path.exists(filename):
        os.remove(filename)
        log.info("delete %s!" % filename)

def stop_slave(slaveip,slave_platform,slave_source_path,slavename):
    try:
        log.info("begin to stop slave: %s!" % slavename)
        if slaveip == "10.10.2.97":
            stop_slave_cmd = "C:/Python27/Scripts/buildslave stop " + os.path.join(slave_source_path,slavename)
        else:
            stop_slave_cmd = "buildslave stop " + os.path.join(slave_source_path,slavename)
        salt_cmd = get_salt_cmd(slave_platform, slaveip, stop_slave_cmd)
        subprocess.Popen(salt_cmd, shell = True)
        log.info("stop slave cmd is: " + salt_cmd)
        log.info("stop slave: %s successfully!" % slavename)
    except Exception, e:
        log.info(str(e))

def update_master(product,buildername):
    if product.lower() == "vidon":
        old_master = "/home/goland/buildbot/master/master.cfg"
    else:
        old_master = "/home/goland/buildbot/DVDFab_master/master.cfg"
    master_content_lines = read_file_lines(old_master)
    new_line_list = []
    flag = 0
    for each_line in master_content_lines:
        if each_line.strip().startswith("import master_" + buildername) and each_line.strip().endswith("import master_" + buildername):
            log.info("remove this line: %s" % each_line)
            flag = 1
        elif each_line.strip().startswith("c = master_" + buildername + ".update_params_dict(c)"):
            log.info("remove this line: %s" % each_line)
            flag = 1
        elif each_line.strip().startswith("master_" + buildername + ".get_lock(build_lock_list)"):
            log.info("remove this line: %s" % each_line)
            flag = 1
        else:
            new_line_list.append(each_line)
    if flag:
        log.info("update master conf file")
        write_file_lines(old_master, new_line_list)
        log.info("remove builder %s conf from master conf file" % buildername)
        

def get_subprocess_content(cmd):
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.readlines()
    error = p.stdout.read()
    return out, error


def delete_slave_from_build_pc(slave_platform, slaveip, slavename, slave_source_path):
    if slave_platform.upper() == "WIN":
        log.info("your slave: %s is in Windows platform, ip is %s , do not have any good methods to delete it!" % (slavename, slaveip))
    else:
        cmd = "ps -ef | grep " + slavename
        salt_cmd = get_salt_cmd(slave_platform, slaveip, cmd)
        out, error = get_subprocess_content(salt_cmd)
        if error:
            log.info("delete slave error: " + error)
        if out:
            slavename_pid = ""
            for each_line in out:
                if "buildslave start" in each_line and slavename in each_line:
                    try:
                        slavename_pid = int([i for i in each_line.strip().split(" ") if i.strip()][1])
                    except:
                        slavename_pid = ""
                    break
            if isinstance(slavename_pid, int):
                kill_pid_cmd = "kill -9 " + str(slavename_pid)
                salt_cmd = get_salt_cmd(slave_platform, slaveip, kill_pid_cmd)
                out, error = get_subprocess_content(salt_cmd)
                if error:
                    log.info("kill pid error: " + error)
                if out:
                    log.info("kill pid out: " + out)
                    #delete slave folder
                    delete_slave_folder_cmd = "rm -fr " + os.path.join(slave_source_path, slavename)
                    salt_cmd = get_salt_cmd(slave_platform, slaveip, delete_slave_folder_cmd)
                    out, error = get_subprocess_content(salt_cmd)
                    if error:
                        log.info("delete slave error: " + error)
                    if out:
                        log.info("delete slave out: " + out)
                

def delete(request, params):
    if request.session.has_key("username"):
        product = request.GET.get("product", "").strip()
        build_info = Build_Info.objects.get(id=params)
        slavename = build_info.slavename
        if not slavename.endswith("_del"):
            build_steps = Build_Steps.objects.filter(build_info_id=params)
            masterip = build_info.masterip
            slaveip = build_info.slaveip
            slave_platform = build_info.slave_platform
            buildername = build_info.buildername
            old_master,locks_file,gitpoller_file, master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,slave_scripts_path,builder_waterfall_address = get_params(slave_platform,slavename,buildername, product)
            stop_slave(slaveip,slave_platform,slave_source_path,slavename)
            update_master(product,buildername)
            restart_master(product)
            build_info.slavename = build_info.slavename + "_del"
            build_info.buildername = build_info.buildername + "_del"
            build_info.flag = 2
            build_info.save()
            #kill slave pid and delete slave folder from build pc
            delete_slave_from_build_pc(slave_platform, slaveip, slavename, slave_source_path)
            username = request.session["username"]
            content = "Hello, " + username + u" 删除" + " build: " + buildername
            title = u"删除" + "build".encode("utf-8")
            send_mails(["dedong.xu@goland.cn"],title,content)
        else:
            log.info("%s is already deleted!\n" % slavename)
        return HttpResponseRedirect("/display_all_used_records/?product="+product)
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")


