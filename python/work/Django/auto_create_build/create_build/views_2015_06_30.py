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


def create_subordinate(subordinate_path,subordinateip,subordinatename):
    try:
        create_subordinate_cmd = "buildsubordinate create-subordinate " + subordinate_path + " " + subordinateip + ":9989 " + subordinatename + " 123456"
        os.system(create_subordinate_cmd)
        log.info("create subordinate: %s successfully!" % subordinatename)
    except Exception, e:
        log.info(str(e))    


def create_start_subordinate_script(subordinate_platform, subordinate_source_path,subordinatename):
    if subordinate_platform == "Win":
        extend_name = ".bat"
    else:
        extend_name = ""
    script_file = os.path.join(subordinate_source_path, "start_subordinate_" + subordinatename + extend_name)
    write_file(script_file, "buildsubordinate start ./" + subordinatename)
    return script_file


def start_subordinate_script(script_file):
    try:
        os.system(script_file)
        log.info("start %s successfully!" % script_file)
    except Exception, e:
        log.info(str(e))


def create_new_main(main_template,buildername,subordinatename,git_project_path,branches_list,monitor_file_path,hour,minute,new_main,send_mail_list,git_project_path_flag = False):
    content = read_file(main_template)
    new_content = content.replace("buildername", buildername).replace("Subordinate_Name", subordinatename).replace("git_url", git_project_path).replace("branches_list", str(branches_list))\
                  .replace("monitor_file_path", monitor_file_path).replace("start_hour",hour).replace("start_minute",minute).replace("send_mail_list",str(send_mail_list))
    if git_project_path_flag:
        new_content = new_content.replace("c['change_source'].append(cs_gitpoller)","#c['change_source'].append(cs_gitpoller)")
    write_file(new_main, new_content)
    log.info("create new main config file: %s successfully!" % new_main)



def import_new_main(old_main,buildername):
    new_list = []
    all_lines = read_file_lines(old_main)
    for each_line in all_lines:
        if each_line.startswith("c = BuildmainConfig = {}"):
            each_line += "\nimport main_" + buildername
        new_list.append(each_line)
    new_list.append("c = main_" + buildername + ".update_params_dict(c)\n")
    try:    
        fp = open(old_main, "w")
        for each_line in new_list:
            fp.write(each_line)
        fp.close()
        log.info("import new main config file: main_%s to main conf file successfully!" % buildername)
    except Exception,e:
        log.info("import new main error: " + str(e))

def create_new_factory(build_info_id,factory_template,new_factory):
    content = read_file(factory_template)
    new_content = content.replace("var_build_info_id", str(build_info_id))
    write_file(new_factory, new_content)


def restart_main(mainip):
    if mainip == "10.10.2.201":
        restart_main_cmd = ""
        current_path = r"D:\buildbot_DVDFab\main"
    elif mainip == "10.10.2.170":
        restart_main_cmd = "buildbot sighup DVDFab9_developer"
        current_path = "/Buildbot_DVDFab/main"
    elif  mainip == "10.10.2.141":
        restart_main_cmd = "buildbot sighup VDMC_android"
        current_path = "/home/goland/buildbot"
    subprocess.Popen(restart_main_cmd, cwd = current_path, shell = True)


def deal_with_data(input_data):
    data_list = []
    input_data = input_data.replace(",",";")
    for each_data in input_data.split(";"):
        if each_data.strip():
            data_list.append(each_data.strip().decode().encode())
    return data_list


def get_params(mainip,subordinate_platform,subordinatename,buildername):
    if mainip == "10.10.2.201":
        old_main = r"\\10.10.2.201\DVDFab_dev\main.cfg"
        main_template = r"\\10.10.2.201\DVDFab_dev\main_template.cfg"
        new_main = r"\\10.10.2.201\DVDFab_dev\main_" + buildername + ".py"
        factory_template = r"\\10.10.2.201\DVDFab_dev\factory_template.py"
        new_factory = r"\\10.10.2.201\DVDFab_dev\dvdfab_factory_" + buildername + ".py"
        if subordinate_platform.upper() == "WIN":
            src_scripts_path = "d:/Buildbot_DVDFab/tool"
            subordinate_source_path = "X:/"
        elif subordinate_platform.upper() == "MAC":
            src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
            subordinate_source_path = "/Volumes/X/"
        elif subordinate_platform.upper() == "UBUNTU":
            src_scripts_path = "/home/goland/buildbot/scripts"
            subordinate_source_path = "/home/goland/buildbot"
        scripts_path = os.path.join(src_scripts_path,subordinatename)
        builder_waterfall_address = "http://10.10.2.201:8010/waterfall?show=" + buildername
        
    elif mainip == "10.10.2.170":
        old_main = r"\\10.10.2.170\DVDFab9_Developer\main.cfg"
        main_template = r"\\10.10.2.170\DVDFab9_Developer\main_template.cfg"
        new_main = r"\\10.10.2.170\DVDFab9_Developer\main_" + buildername + ".py"
        factory_template = r"\\10.10.2.170\DVDFab9_Developer\factory_template.py"
        new_factory = r"\\10.10.2.170\DVDFab9_Developer\dvdfab_factory_" + buildername + ".py"
        if subordinate_platform.upper() == "WIN":
            src_scripts_path = "d:/Buildbot_DVDFab/tool"
            subordinate_source_path = "X:/"
        elif subordinate_platform.upper() == "MAC":
            src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
            subordinate_source_path = "/Volumes/X/"
        elif subordinate_platform.upper() == "UBUNTU":
            src_scripts_path = "/home/goland/buildbot/scripts"
            subordinate_source_path = "/home/goland/buildbot"
        scripts_path = os.path.join(src_scripts_path,subordinatename)
        builder_waterfall_address = "http://10.10.2.170:8010/waterfall?show=" + buildername
        
    elif mainip == "10.10.2.141":
        old_main = r"\\10.10.2.141\VDMC_android\main.cfg"
        main_template = r"\\10.10.2.141\VDMC_android\main_template.cfg"
        new_main = r"\\10.10.2.141\VDMC_android\main_" + buildername + ".py"
        factory_template = r"\\10.10.2.141\VDMC_android\factory_template.py"
        new_factory = r"\\10.10.2.141\VDMC_android\dvdfab_factory_" + buildername + ".py"
        if subordinate_platform.upper() == "WIN":
            src_scripts_path = "d:/Buildbot_DVDFab/tool"
            subordinate_source_path = "X:/"
        elif subordinate_platform.upper() == "MAC":
            src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
            subordinate_source_path = "/Volumes/X/"
        elif subordinate_platform.upper() == "UBUNTU":
            src_scripts_path = "/home/goland/buildbot/scripts"
            subordinate_source_path = "/home/goland/buildbot"
        scripts_path = os.path.join(src_scripts_path,subordinatename)
        builder_waterfall_address = "http://10.10.2.141:8010/waterfall?show=" + buildername
    return old_main,main_template,new_main,factory_template,new_factory,src_scripts_path,scripts_path,subordinate_source_path,builder_waterfall_address


def git_first_commit(src_scripts_path,scripts_path,subordinatename):
    git_add_cmd = "git add " + scripts_path    
    subprocess.call(git_add_cmd, cwd = src_scripts_path, shell = True)
    git_commit_cmd = "git commit %s -m 'new add for %s'" % (scripts_path, subordinatename)
    subprocess.call(git_commit_cmd, cwd = src_scripts_path, shell = True)
    git_push_origin = "git push origin main"
    subprocess.call(git_push_origin, cwd = src_scripts_path, shell = True)
    log.info("git push success!")


def git_commit(src_scripts_path, scripts_path, subordinatename):
    git_commit_cmd = "git commit %s -m 'update for %s'" % (scripts_path, subordinatename)
    subprocess.call(git_commit_cmd, cwd = src_scripts_path, shell = True)
    git_push_origin = "git push origin main"
    subprocess.call(git_push_origin, cwd = src_scripts_path, shell = True)

    
@csrf_exempt
def create_new_build(request):
    cmd = 'echo "123456"|sudo -S salt "win_10.10.2.30" cmd.run "buildsubordinate create-subordinate X:/TEST 10.10.2.170:9989 TEST 123456"'
    #cmd = 'echo "123456"|sudo -S salt "win_10.10.2.30" state.sls test'
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    #out = p.stdout.read()
    #err = p.stderr.read()
    #fp = open("/home/goland/111.txt","w")
    #fp.write("out: " + out)
    #fp.write("err: " + err)
    #fp.close()

    mainip = request.POST.get("mainip", "").strip()
    subordinateip = request.POST.get("subordinateip", "").strip()
    subordinate_platform = request.POST.get("subordinate_platform", "").strip()
    subordinatename = request.POST.get("subordinatename", "").strip()
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
    log.info("main ip is:%s" % mainip)
    log.info("subordinate ip is:%s" % subordinateip)
    log.info("subordinate platform is:%s" % subordinate_platform)
    log.info("subordinatename is:%s" % subordinatename)
    log.info("buildername is:%s" % buildername)
    subordinate_count = Build_Info.objects.filter(subordinatename = subordinatename).count()
    if subordinate_count >= 1:
        var_name = "subordinate"
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
    
    old_main,main_template,new_main,factory_template,new_factory,src_scripts_path,scripts_path,subordinate_source_path,builder_waterfall_address = get_params(mainip,subordinate_platform,subordinatename,buildername)
    build_info = Build_Info(mainip = mainip, subordinateip = subordinateip, subordinate_platform = subordinate_platform, subordinatename = subordinatename, buildername = buildername,start_method = start_method,\
                            username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,monitor_file_path = monitor_file_path,\
                            send_mail = send_mail, flag = 1, new_main = new_main, new_factory = new_factory,scripts_path = scripts_path)
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
            if subordinate_platform == "Win":
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
    git_first_commit(src_scripts_path,scripts_path,subordinatename)
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    log.info(send_mail_list)
    subordinate_path = os.path.join(subordinate_source_path, subordinatename)
    ###############################     the line below need to use saltstack     ###################################
    create_subordinate(subordinate_path,subordinateip,subordinatename)
    ###############################     the line below need to use saltstack     ###################################
    create_new_main(main_template,buildername,subordinatename,git_project_path,branches_list,monitor_file_path,hour,minute,new_main,send_mail_list,git_project_path_flag)
    ###############################     the line below need to use saltstack     ###################################
    import_new_main(old_main,buildername)
    ###############################     the line below need to use saltstack     ###################################
    create_new_factory(build_info_id,factory_template,new_factory)
    #TODO: restart main
    ###############################     the line below need to use saltstack     ###################################
    restart_main(mainip)
    ###############################     the line below need to use saltstack     ###################################
    script_file = create_start_subordinate_script(subordinate_platform,subordinate_source_path,subordinatename)
    ###############################     the line below need to use saltstack     ###################################
    start_subordinate_script(script_file)
    
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

    if search_name == "subordinatename" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["subordinatename like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        if not build_info:
            return HttpResponseRedirect("/empty/")
        
    elif search_name == "buildername" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["buildername like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        if not build_info:
            return HttpResponseRedirect("/empty/")
    elif search_name == "subordinate_platform" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["subordinate_platform like'%%" + str(record_name) + "%%'"])
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
    mainip = request.POST.get("mainip", "").strip()
    subordinateip = request.POST.get("subordinateip", "").strip()
    subordinate_platform = request.POST.get("subordinate_platform", "").strip()
    subordinatename = request.POST.get("subordinatename", "").strip()
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
   
    new_main = request.POST.get("new_main","").strip()
    new_factory = request.POST.get("new_factory","").strip()
    scripts_path = request.POST.get("scripts_path","").strip()
    for each_value in request.POST.values():
        if not each_value.strip():
            return render_to_response("update_error.html", locals())

    git_project_path_main_conf = Build_Info.objects.filter(git_project_path = git_project_path)
    git_project_path_main_conf_list = []
    git_project_path_flag = False
    if len(git_project_path_main_conf) >= 1:
        for each_record in git_project_path_main_conf:
            git_project_path_main_conf_list.append(each_record.new_main)
            all_lines = read_file_lines(each_record.new_main)
            for each_line in all_lines:
                if each_line.strip().startswith("c['change_source'].append(cs_gitpoller)"):
                    git_project_path_flag = True
                    break

    build_info.update(mainip = mainip, subordinateip = subordinateip, subordinate_platform = subordinate_platform, subordinatename = subordinatename,buildername = buildername,\
                      start_method = start_method,username = username, hour = hour,minute = minute,git_project_path = git_project_path,branches = branches,\
                      monitor_file_path = monitor_file_path,send_mail = send_mail, flag = 1,new_main = new_main,new_factory = new_factory,scripts_path = scripts_path)

    all_count = build_steps.count()
    if all_count > 0:
        for each_num in xrange(1,all_count+1):
            if subordinate_platform == "Win":
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
    if mainip == "10.10.2.201":
        factory_template = r"\\10.10.2.201\DVDFab_dev\factory_template.py"
        main_template = r"\\10.10.2.201\DVDFab_dev\main_template.cfg"
        builder_waterfall_address = "http://10.10.2.201:8010/waterfall?show=" + buildername
        #src_scripts_path = "d:/Buildbot_DVDFab/tool"

    elif mainip == "10.10.2.170":
        factory_template = r"\\10.10.2.170\DVDFab9_Developer\factory_template.py"
        main_template = r"\\10.10.2.170\DVDFab9_Developer\main_template.cfg"
        builder_waterfall_address = "http://10.10.2.170:8010/waterfall?show=" + buildername
        #src_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool"
   
    elif mainip == "10.10.2.141":
        factory_template = r"\\10.10.2.141\VDMC_android\factory_template.py"
        main_template = r"\\10.10.2.141\VDMC_android\main_template.cfg"
        builder_waterfall_address = "http://10.10.2.141:8010/waterfall?show=" + buildername
        #src_scripts_path = "/home/goland/buildbot/scripts"
    #old_main,main_template,new_main,factory_template,new_factory,scripts_path,subordinate_source_path,builder_waterfall_address = get_params(mainip,subordinate_platform,subordinatename,buildername)
    ###############################     the line below need to use saltstack     ###################################
    create_new_main(main_template,buildername,subordinatename,git_project_path,branches_list,monitor_file_path,hour,minute,new_main,send_mail_list,git_project_path_flag)
    ###############################     the line below need to use saltstack     ###################################
    create_new_factory(params,factory_template,new_factory)
    #TODO: git push scripts
    #commit updated build step scripts to git
    ###############################     the line below need to use saltstack     ###################################
    #git_commit(src_scripts_path, scripts_path, subordinatename)
    git_commit(os.path.dirname(scripts_path), scripts_path, subordinatename)
    ###############################     the line below need to use saltstack     ###################################
    restart_main(mainip)
    return render_to_response("update_success.html",{"builder_waterfall_address":builder_waterfall_address})

def delete_files(filename):
    if os.path.exists(filename):
        os.remove(filename)
        log.info("delete %s!" % filename)


def update_main(mainip,buildername):
    if mainip == "10.10.2.201":
        old_main = r"\\10.10.2.201\DVDFab_dev\main.cfg"        
    elif mainip == "10.10.2.170":
        old_main = r"\\10.10.2.170\DVDFab9_Developer\main.cfg"
    elif mainip == "10.10.2.141":
        old_main = r"\\10.10.2.141\VDMC_android\main.cfg"
    ###############################     the line below need to use saltstack     ###################################
    main_content_lines = read_file_lines(old_main)
    new_line_list = []
    flag = 0
    for each_line in main_content_lines:
        if each_line.startswith("import main_" + buildername):
            log.info("remove this line: %s" % each_line)
            flag = 1
        elif each_line.strip().startswith("c = main_" + buildername + ".update_params_dict(c)"):
            log.info("remove this line: %s" % each_line)
            flag = 1
        else:
            new_line_list.append(each_line)
    if flag:
        log.info("create new main conf file")
        ###############################     the line below need to use saltstack     ###################################
        fp = open(old_main, "w")
        for each_line in new_line_list:
            fp.write(each_line)
        fp.close()
        log.info("remove builderer %s conf from main conf file" % buildername)
        

def delete(request, params):
    if request.session.has_key("username"):
        build_info = Build_Info.objects.get(id=params)
        mainip = build_info.mainip
        build_steps = Build_Steps.objects.filter(build_info_id=params)
        #build_steps.delete()
        #build_info.delete()
        #delete_files(factory_path)
        #delete_files(main_path)
        build_info.flag = 2
        build_info.save()
        mainip = build_info.mainip
        buildername = build_info.buildername
        ###############################     the line below need to use saltstack     ###################################
        update_main(mainip,buildername)
        return HttpResponseRedirect("/display_all_records/")
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")










