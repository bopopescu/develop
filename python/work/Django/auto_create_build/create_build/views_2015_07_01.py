#encoding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import *
from forms import *
from django.core.exceptions import ValidationError
import os
import logging
import subprocess
import time
import smtplib
from email.mime.text import MIMEText

log = logging.getLogger("django")


@csrf_exempt
def register(request):
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
def login(request):
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        passwd = request.POST.get("passwd","").strip()
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
    return render_to_response("login.html", locals())


def logout(request):
    if request.session.has_key("username"):
        del request.session["username"]
        return HttpResponseRedirect("/display_all_records/")


def send_mail(to_list,sub,content):
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
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()
        return True  
    except Exception, e:  
        print str(e)  
        return False


def get_passwd_page(request):
    return render_to_response("get_passwd.html",locals())

    
@csrf_exempt
def get_passwd(request):
    username = request.POST.get("username","").strip()
    email = request.POST.get("email","").strip()
    if username and email:
        try:
            register = Register.objects.get(username = username)
        except Exception,e:
            return HttpResponse("<body style = 'background-color:#77ac98'><a href = ''>用户名不存在,点击返回重新填写</a></body>")
        else:
            passwd = register.passwd
            content = "Hello,your password is: %s" % passwd
            title = "Find Password"
            send_mail([email],title,content)
        return HttpResponseRedirect("/get_passwd_page/")
    else:
        return render_to_response("get_passwd.html",locals())



def index(request):
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


def write_file(filename, content):
    try:
        fp = open(filename, "w")
        fp.write(content)
        fp.close()
    except Exception, e:
        log.info("write file error: " + str(e))


def read_file(filename):
    content = ""
    try:
        if os.path.exists(filename):
            log.info("%s exists!" % filename)
            fp = open(filename, "r")
            content = fp.read()
            fp.close()
        else:
            log.info("%s does not exist!" % filename)
    except Exception, e:
        log.info("read file error: " + str(e))
    return content


def read_file_lines(filename):
    all_lines = []
    try:
        if os.path.exists(filename):
            fp = open(filename, "r")
            all_lines = fp.readlines()
            fp.close()
    except Exception, e:
        log.info("read file lines error: " + str(e))
    return all_lines


def create_slave(masterip,slave_path,slaveip,slave_platform,slavename):
    try:
        create_slave_cmd = "buildslave create-slave " + slave_path + " " + masterip + ":9989 " + slavename + " 123456"
        salt_cmd = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + create_slave_cmd + '"'
        #os.system(create_slave_cmd)
        os.system(salt_cmd)
        log.info("create slave: %s successfully!" % slavename)
    except Exception, e:
        log.info(str(e))    


def create_start_slave_script(slave_platform, slave_source_path,slavename):
    if slave_platform == "Win":
        extend_name = ".bat"
    else:
        extend_name = ""
    script_file = os.path.join(slave_source_path, "start_slave_" + slavename + extend_name)
    ########how to use salt################
    write_file(script_file, "buildslave start ./" + slavename)
    return script_file


def start_slave_script(slaveip,slave_platform,script_file):
    try:
        salt_cmd = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + script_file + '"'
        os.system(salt_cmd)
        #os.system(script_file)
        log.info("start %s successfully!" % script_file)
    except Exception, e:
        log.info(str(e))


def create_new_master(master_template,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list,git_project_path_flag = False):
    content = read_file(master_template)
    new_content = content.replace("buildername", buildername).replace("Slave_Name", slavename).replace("git_url", git_project_path).replace("branches_list", str(branches_list))\
                  .replace("monitor_file_path", monitor_file_path).replace("start_hour",hour).replace("start_minute",minute).replace("send_mail_list",str(send_mail_list))
    if git_project_path_flag:
        new_content = new_content.replace("c['change_source'].append(cs_gitpoller)","#c['change_source'].append(cs_gitpoller)")
    ########how to use salt################
    write_file(new_master, new_content)
    log.info("create new master config file: %s successfully!" % new_master)



def import_new_master(old_master,buildername):
    new_list = []
    all_lines = read_file_lines(old_master)
    for each_line in all_lines:
        if each_line.startswith("c = BuildmasterConfig = {}"):
            each_line += "\nimport master_" + buildername
        new_list.append(each_line)
    new_list.append("c = master_" + buildername + ".update_params_dict(c)\n")
    ########################how to use salt ####################
    try:    
        fp = open(old_master, "w")
        for each_line in new_list:
            fp.write(each_line)
        fp.close()
        log.info("import new master config file: master_%s to main conf file successfully!" % buildername)
    except Exception,e:
        log.info("import new master error: " + str(e))

def create_new_factory(build_info_id,factory_template,new_factory):
    content = read_file(factory_template)
    new_content = content.replace("var_build_info_id", str(build_info_id))
    ########################how to use salt ####################
    write_file(new_factory, new_content)


def restart_master(masterip,slave_platform):
    if masterip == "10.10.2.201":
        restart_master_cmd = ""
        current_path = r"D:\buildbot_DVDFab\master"
    elif masterip == "10.10.2.170":
        restart_master_cmd = "buildbot sighup DVDFab9_developer"
        current_path = "/Buildbot_DVDFab/master"
    elif  masterip == "10.10.2.141":
        restart_master_cmd = "buildbot sighup VDMC_android"
        current_path = "/home/goland/buildbot"
    #############################################need to use salt to run cmd############################
    salt_cmd = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + restart_master_cmd + '"'
    subprocess.Popen(salt_cmd, cwd = current_path, shell = True)
    #subprocess.Popen(restart_master_cmd, cwd = current_path, shell = True)


def deal_with_data(input_data):
    data_list = []
    input_data = input_data.replace(",",";")
    for each_data in input_data.split(";"):
        if each_data.strip():
            data_list.append(each_data.strip().decode().encode())
    return data_list


def get_params(masterip,slave_platform,slavename,buildername):
    if masterip == "10.10.2.201":
        old_master = r"d:\buildbot_DVDFab\master\DVDFab_dev\master.cfg"
        master_template = r"d:\buildbot_DVDFab\master\DVDFab_dev\master_template.cfg"
        new_master = r"d:\buildbot_DVDFab\master\DVDFab_dev\master_" + buildername + ".py"
        factory_template = r"d:\buildbot_DVDFab\master\DVDFab_dev\factory_template.py"
        new_factory = r"d:\buildbot_DVDFab\master\DVDFab_dev\dvdfab_factory_" + buildername + ".py"
        if slave_platform.upper() == "WIN":
            src_scripts_path = "d:/Buildbot_DVDFab/tool"
            slave_source_path = "X:/"
        elif slave_platform.upper() == "MAC":
            src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
            slave_source_path = "/Volumes/X/"
        elif slave_platform.upper() == "UBUNTU":
            src_scripts_path = "/home/goland/buildbot/scripts"
            slave_source_path = "/home/goland/buildbot"
        scripts_path = os.path.join(src_scripts_path,slavename)
        builder_waterfall_address = "http://10.10.2.201:8010/waterfall?show=" + buildername
        
    elif masterip == "10.10.2.170":
        old_master = "/Buildbot_DVDFab/master/DVDFab9_Developer/master.cfg"
        master_template = "/Buildbot_DVDFab/master/DVDFab9_Developer/master_template.cfg"
        new_master = "/Buildbot_DVDFab/master/DVDFab9_Developer/master_" + buildername + ".py"
        factory_template = "/Buildbot_DVDFab/master/DVDFab9_Developer/factory_template.py"
        new_factory = "/Buildbot_DVDFab/master/DVDFab9_Developer/dvdfab_factory_" + buildername + ".py"
        if slave_platform.upper() == "WIN":
            src_scripts_path = "d:/Buildbot_DVDFab/tool"
            slave_source_path = "X:/"
        elif slave_platform.upper() == "MAC":
            src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
            slave_source_path = "/Volumes/X/"
        elif slave_platform.upper() == "UBUNTU":
            src_scripts_path = "/home/goland/buildbot/scripts"
            slave_source_path = "/home/goland/buildbot"
        scripts_path = os.path.join(src_scripts_path,slavename)
        builder_waterfall_address = "http://10.10.2.170:8010/waterfall?show=" + buildername
        
    elif masterip == "10.10.2.141":
        old_master = "/home/goland/buildbot/VDMC_android/master.cfg"
        master_template = "/home/goland/buildbot/VDMC_android/master_template.cfg"
        new_master = "/home/goland/buildbot/VDMC_android/master_" + buildername + ".py"
        factory_template = "/home/goland/buildbot/VDMC_android/factory_template.py"
        new_factory = "/home/goland/buildbot/VDMC_android/dvdfab_factory_" + buildername + ".py"
        if slave_platform.upper() == "WIN":
            src_scripts_path = "d:/Buildbot_DVDFab/tool"
            slave_source_path = "X:/"
        elif slave_platform.upper() == "MAC":
            src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
            slave_source_path = "/Volumes/X/"
        elif slave_platform.upper() == "UBUNTU":
            src_scripts_path = "/home/goland/buildbot/scripts"
            slave_source_path = "/home/goland/buildbot"
        scripts_path = os.path.join(src_scripts_path,slavename)
        builder_waterfall_address = "http://10.10.2.141:8010/waterfall?show=" + buildername
    return old_master,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,builder_waterfall_address


def git_first_commit(src_scripts_path,scripts_path,slavename,slaveip,slave_platform):
    git_add_cmd = "git add " + scripts_path    
    salt_cmd_git_add = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + git_add_cmd + '"'
    subprocess.call(salt_cmd_git_add, cwd = src_scripts_path, shell = True)
    
    git_commit_cmd = "git commit %s -m 'new add for %s'" % (scripts_path, slavename)
    salt_cmd_git_commit = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + git_commit_cmd + '"'
    subprocess.call(salt_cmd_git_commit, cwd = src_scripts_path, shell = True)
    
    git_push_origin = "git push origin master"
    salt_cmd_git_push_origin = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + git_push_origin + '"'
    subprocess.call(salt_cmd_git_push_origin, cwd = src_scripts_path, shell = True)
    log.info("first git push success!")


def git_commit(src_scripts_path, scripts_path, slavename,slaveip,slave_platform):
    git_commit_cmd = "git commit %s -m 'update for %s'" % (scripts_path, slavename)
    salt_cmd_git_commit = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + git_commit_cmd + '"'
    subprocess.call(salt_cmd_git_commit, cwd = src_scripts_path, shell = True)
    git_push_origin = "git push origin master"
    salt_cmd_git_push_origin = 'echo "123456"|sudo -S salt "' + slave_platform.lower() + "_" + slaveip + '" cmd.run "' + git_push_origin + '"'
    subprocess.call(salt_cmd_git_push_origin, cwd = src_scripts_path, shell = True)
    log.info("git push success!")

    
@csrf_exempt
def create_new_build(request):
    #cmd = 'echo "123456"|sudo -S salt "win_10.10.2.30" cmd.run "buildslave create-slave X:/TEST 10.10.2.170:9989 TEST 123456"'
    #cmd = 'echo "123456"|sudo -S salt "win_10.10.2.30" state.sls test'
    #p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    #out = p.stdout.read()
    #err = p.stderr.read()
    #fp = open("/home/goland/111.txt","w")
    #fp.write("out: " + out)
    #fp.write("err: " + err)
    #fp.close()

    masterip = request.POST.get("masterip", "").strip()
    slaveip = request.POST.get("slaveip", "").strip()
    slave_platform = request.POST.get("slave_platform", "").strip()
    slavename = request.POST.get("slavename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    start_method = request.POST.get("start_method", "").strip()
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

    if len(request.POST.values()) == 0:
        return render_to_response("error.html")
    for each_value in request.POST.values():
        if not each_value.strip():
            return render_to_response("error.html")
    log.info("\n")
    log.info("-----------------------------begin----------------------------------")
    log.info("master ip is:%s" % masterip)
    log.info("slave ip is:%s" % slaveip)
    log.info("slave platform is:%s" % slave_platform)
    log.info("slavename is:%s" % slavename)
    log.info("buildername is:%s" % buildername)
    slave_count = Build_Info.objects.filter(slavename = slavename).count()
    if slave_count >= 1:
        var_name = "slave"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)

    builder_count = Build_Info.objects.filter(buildername = buildername).count()
    if builder_count >= 1:
        var_name = "builder"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)

    git_project_path_count = Build_Info.objects.filter(git_project_path = git_project_path).count()
    if git_project_path_count >= 1:
        git_project_path_flag = True
    else:
        git_project_path_flag = False
    
    old_master,master_template,new_master,factory_template,new_factory,src_scripts_path,scripts_path,slave_source_path,builder_waterfall_address = get_params(masterip,slave_platform,slavename,buildername)
    build_info = Build_Info(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename, buildername = buildername,start_method = start_method,\
                            username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,monitor_file_path = monitor_file_path,\
                            send_mail = send_mail, flag = 1, new_master = new_master, new_factory = new_factory,scripts_path = scripts_path)
    build_info.save()
    obj = Build_Info.objects.all()[0]
    if obj:
        build_info_id = obj.id
    else:
        build_info_id = ""
    all_length = len(request.POST)
    if start_method == "radio_timing":
        other_length = 9
    elif start_method == "radio_trigger":
        other_length = 10
    else:
        other_length = 7
    table_length = all_length - other_length
    if table_length > 0:
        for each_num in xrange(1,(table_length/3)+1):
            if not os.path.exists(scripts_path):
                ###############################     the line below need to use saltstack     ###################################
                #salt "ip" cmd.run "mkdir"
                os.makedirs(scripts_path)
            if slave_platform == "Win":
                filename = "script" + str(each_num) + ".bat"    
            else:
                filename = "script" + str(each_num) + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/")            
            ###############################     the line below need to use saltstack     ###################################
            write_file(script_file, request.POST["script_content" + str(each_num)])
            build_steps = Build_Steps(build_info_id = build_info_id, script_content = script_file, \
                                  work_dir = request.POST["work_dir" + str(each_num)], description = request.POST["description" + str(each_num)])
            build_steps.save()
    #commit build step scripts to git
    ###############################     the line below need to use saltstack     ###################################
    git_first_commit(src_scripts_path,scripts_path,slavename,slaveip, slave_platform)
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    log.info(send_mail_list)
    slave_path = os.path.join(slave_source_path, slavename)
    ###############################     the line below need to use saltstack     ###################################
    create_slave(masterip,slave_path,slaveip,slave_platform,slavename)
    ###############################     the line below need to use saltstack     ###################################
    create_new_master(master_template,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list,git_project_path_flag)
    ###############################     the line below need to use saltstack     ###################################
    import_new_master(old_master,buildername)
    ###############################     the line below need to use saltstack     ###################################
    create_new_factory(build_info_id,factory_template,new_factory)
    #TODO: restart master
    ###############################     the line below need to use saltstack     ###################################
    restart_master(masterip,slave_platform)
    ###############################     the line below need to use saltstack     ###################################
    script_file = create_start_slave_script(slave_platform,slave_source_path,slavename)
    ###############################     the line below need to use saltstack     ###################################
    start_slave_script(slaveip,slave_platform,script_file)
    
    return render_to_response("success.html",{"builder_waterfall_address":builder_waterfall_address})



#fen ye xian shi
def display_all_records(request):
    per_page_count = 20
    nowpage = request.GET.get("nowpage","").strip()
    if nowpage == "":
        nowpage = 1
    else:
        nowpage = int(nowpage)
    count = Build_Info.objects.filter(flag = 1).count()
    if count % per_page_count == 0:
        pageall = count / per_page_count
    else:
        pageall = count / per_page_count + 1
    if nowpage <= 1:
        pageup = 1
    else:
        pageup = nowpage - 1
    if nowpage + 1 >= pageall:
        pagedn = pageall
    else:
        pagedn = nowpage + 1
    start = per_page_count * (nowpage - 1)        
    build_info = Build_Info.objects.filter(flag = 1)[start:(start + per_page_count)]
    return render_to_response("display_all_records.html", locals())


def display_details(request,params):
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


@csrf_exempt
def search_info(request):
    flag = 0
    search_name = request.POST.get("search_name", "").strip()
    record_name = request.POST.get("record_name", "").strip()
    if not record_name:
        flag = 1

    if search_name == "slavename" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["slavename like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        if not build_info:
            return HttpResponseRedirect("/empty/")
        
    elif search_name == "buildername" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["buildername like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        if not build_info:
            return HttpResponseRedirect("/empty/")
    elif search_name == "slave_platform" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["slave_platform like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        if not build_info:
            return HttpResponseRedirect("/empty/")
    elif search_name == "username" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["username like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        if not build_info:
            return HttpResponseRedirect("/empty/")
    else:
        return HttpResponseRedirect("/display_all_records/")
    return render_to_response("display_all_records.html",locals())



def update_info_page(request, params):
    if request.session.has_key("username"):
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

    git_project_path_master_conf = Build_Info.objects.filter(git_project_path = git_project_path)
    git_project_path_master_conf_list = []
    git_project_path_flag = False
    if len(git_project_path_master_conf) >= 1:
        for each_record in git_project_path_master_conf:
            git_project_path_master_conf_list.append(each_record.new_master)
            all_lines = read_file_lines(each_record.new_master)
            for each_line in all_lines:
                if each_line.strip().startswith("c['change_source'].append(cs_gitpoller)"):
                    git_project_path_flag = True
                    break

    build_info.update(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename,buildername = buildername,\
                      start_method = start_method,username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,\
                      monitor_file_path = monitor_file_path,send_mail = send_mail, flag = 1,new_master = new_master,new_factory = new_factory,scripts_path = scripts_path)

    all_count = build_steps.count()
    if all_count > 0:
        for each_num in xrange(1,all_count+1):
            if slave_platform == "Win":
                filename = "script" + str(each_num) + ".bat"    
            else:
                filename = "script" + str(each_num) + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/")
            ###############################     the line below need to use saltstack     ###################################
            write_file(script_file, request.POST["script_content" + str(each_num)])
            each_step = build_steps.filter(script_content = script_file)
            each_step.update(build_info_id = params, script_content = script_file, \
                            work_dir = request.POST["work_dir" + str(each_num)], description = request.POST["description" + str(each_num)])

    log.info("update success!!")
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    #update conf file
    if masterip == "10.10.2.201":
        factory_template = r"\\10.10.2.201\DVDFab_dev\factory_template.py"
        master_template = r"\\10.10.2.201\DVDFab_dev\master_template.cfg"
        builder_waterfall_address = "http://10.10.2.201:8010/waterfall?show=" + buildername
        #src_scripts_path = "d:/Buildbot_DVDFab/tool"

    elif masterip == "10.10.2.170":
        factory_template = r"\\10.10.2.170\DVDFab9_Developer\factory_template.py"
        master_template = r"\\10.10.2.170\DVDFab9_Developer\master_template.cfg"
        builder_waterfall_address = "http://10.10.2.170:8010/waterfall?show=" + buildername
        #src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
   
    elif masterip == "10.10.2.141":
        factory_template = r"\\10.10.2.141\VDMC_android\factory_template.py"
        master_template = r"\\10.10.2.141\VDMC_android\master_template.cfg"
        builder_waterfall_address = "http://10.10.2.141:8010/waterfall?show=" + buildername
        #src_scripts_path = "/home/goland/buildbot/scripts"
    #old_master,master_template,new_master,factory_template,new_factory,scripts_path,slave_source_path,builder_waterfall_address = get_params(masterip,slave_platform,slavename,buildername)
    ###############################     the line below need to use saltstack     ###################################
    create_new_master(master_template,buildername,slavename,git_project_path,branches_list,monitor_file_path,hour,minute,new_master,send_mail_list,git_project_path_flag)
    ###############################     the line below need to use saltstack     ###################################
    create_new_factory(params,factory_template,new_factory)
    #TODO: git push scripts
    #commit updated build step scripts to git
    ###############################     the line below need to use saltstack     ###################################
    #git_commit(src_scripts_path, scripts_path, slavename)
    git_commit(os.path.dirname(scripts_path), scripts_path, slavename,slaveip,slave_platform)
    ###############################     the line below need to use saltstack     ###################################
    restart_master(masterip,slave_platform)
    return render_to_response("update_success.html",{"builder_waterfall_address":builder_waterfall_address})

def delete_files(filename):
    if os.path.exists(filename):
        os.remove(filename)
        log.info("delete %s!" % filename)


def update_master(masterip,buildername):
    if masterip == "10.10.2.201":
        old_master = r"\\10.10.2.201\DVDFab_dev\master.cfg"        
    elif masterip == "10.10.2.170":
        old_master = r"\\10.10.2.170\DVDFab9_Developer\master.cfg"
    elif masterip == "10.10.2.141":
        old_master = r"\\10.10.2.141\VDMC_android\master.cfg"
    ###############################     the line below need to use saltstack     ###################################
    master_content_lines = read_file_lines(old_master)
    new_line_list = []
    flag = 0
    for each_line in master_content_lines:
        if each_line.startswith("import master_" + buildername):
            log.info("remove this line: %s" % each_line)
            flag = 1
        elif each_line.strip().startswith("c = master_" + buildername + ".update_params_dict(c)"):
            log.info("remove this line: %s" % each_line)
            flag = 1
        else:
            new_line_list.append(each_line)
    if flag:
        log.info("create new master conf file")
        ###############################     the line below need to use saltstack     ###################################
        fp = open(old_master, "w")
        for each_line in new_line_list:
            fp.write(each_line)
        fp.close()
        log.info("remove builderer %s conf from master conf file" % buildername)
        

def delete(request, params):
    if request.session.has_key("username"):
        build_info = Build_Info.objects.get(id=params)
        masterip = build_info.masterip
        build_steps = Build_Steps.objects.filter(build_info_id=params)
        #build_steps.delete()
        #build_info.delete()
        #delete_files(factory_path)
        #delete_files(master_path)
        build_info.flag = 2
        build_info.save()
        masterip = build_info.masterip
        buildername = build_info.buildername
        ###############################     the line below need to use saltstack     ###################################
        update_master(masterip,buildername)
        return HttpResponseRedirect("/display_all_records/")
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")










