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
from django.contrib import auth
from django.contrib.auth.models import User
import settings
#from DjangoVerifyCode import Code

log = logging.getLogger("django")


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
    #return HttpResponse(settings.XDD)
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
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        passwd = request.POST.get("passwd","").strip()
        user = auth.authenticate(username=username,password=passwd)
        if user is not None:
            auth.login(request,user)
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
    return HttpResponseRedirect("/display_all_records/")


def logout_old(request):
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
            send_mail([email],title,content)
        return render_to_response("get_passwd_success.html",locals())
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


def create_subordinate(mainip,subordinate_path,subordinateip,subordinate_platform,subordinatename):
    try:
        create_subordinate_cmd = "buildsubordinate create-subordinate " + subordinate_path + " " + mainip + ":9989 " + subordinatename + " 123456"
        salt_cmd = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + create_subordinate_cmd + '"'
        #os.system(create_subordinate_cmd)
        os.system(salt_cmd)
        log.info("create subordinate: %s successfully!" % subordinatename)
    except Exception, e:
        log.info(str(e))    


def create_start_subordinate_script(subordinate_platform,subordinate_source_path,subordinatename):
    if subordinate_platform == "Win":
        extend_name = ".bat"
    else:
        extend_name = ""
    script_file = os.path.join(subordinate_source_path, "start_subordinate_" + subordinatename + extend_name)
    ########how to use salt################
    write_file(script_file, "buildsubordinate start ./" + subordinatename)
    return script_file


def start_subordinate_script(subordinateip,subordinate_platform,subordinate_source_path,subordinatename):
    try:
        log.info("begin to start subordinate: %s!" % subordinatename)
        start_subordinate_cmd = "buildsubordinate start " + os.path.join(subordinate_source_path,subordinatename)
        salt_cmd = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + start_subordinate_cmd + '"'
        subprocess.Popen(salt_cmd, shell = True)
        log.info("start subordinate cmd is: " + salt_cmd)
        log.info("start subordinate: %s successfully!" % subordinatename)
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

def create_new_factory(build_info_id,subordinate_platform,factory_template,new_factory):
    content = read_file(factory_template)
    new_content = content.replace("var_build_info_id", str(build_info_id)).replace("var_subordinate_platform", subordinate_platform)
    write_file(new_factory, new_content)
    log.info("create or update factory!")

def restart_main():
    current_path = "/home/goland/buildbot"
    restart_main_cmd = "buildbot restart main"
    subprocess.Popen(restart_main_cmd, cwd = current_path, shell = True)
    log.info("I am here: restart main cmd is: %s" % restart_main_cmd)


def deal_with_data(input_data):
    data_list = []
    input_data = input_data.replace(",",";")
    for each_data in input_data.split(";"):
        if each_data.strip():
            data_list.append(each_data.strip().decode().encode())
    return data_list


def get_params(subordinate_platform,subordinatename,buildername):
    old_main = "/home/goland/buildbot/main/main.cfg"
    main_template = "/home/goland/buildbot/main/main_template.cfg"
    factory_template = "/home/goland/buildbot/main/factory_template.py"
    new_main = "/home/goland/buildbot/main/main_" + buildername + ".py"
    new_factory = "/home/goland/buildbot/main/dvdfab_factory_" + buildername + ".py"
    if subordinate_platform.upper() == "WIN":
        subordinate_source_path = "X:/"
        subordinate_scripts_path = "d:/Buildbot_DVDFab/tool/scripts"
    elif subordinate_platform.upper() == "MAC":
        subordinate_source_path = "/Volumes/X/"
        subordinate_scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool/scripts"
    elif subordinate_platform.upper() == "UBU":
        subordinate_source_path = "/home/goland/buildbot"
        subordinate_scripts_path = "/home/goland/buildbot/tool/scripts"
    src_scripts_path = "/home/goland/buildbot/scripts"
    scripts_path = os.path.join(src_scripts_path,subordinatename)
    builder_waterfall_address = "http://10.10.2.64:8010/waterfall?show=" + buildername
    return old_main,main_template,new_main,factory_template,new_factory,src_scripts_path,scripts_path,subordinate_source_path,subordinate_scripts_path,builder_waterfall_address


def make_dirs(subordinate_source_path,subordinate_scripts_path,subordinate_platform,subordinateip):
    create_dir1 = "mkdir " + subordinate_source_path
    create_dir2 = "mkdir " + subordinate_scripts_path
    salt_cmd_create_dir1 = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + create_dir1
    salt_cmd_create_dir2 = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + create_dir2
    #subprocess.Popen(salt_cmd_create_dir1, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    subprocess.Popen(salt_cmd_create_dir2, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)


def git_first_commit(src_scripts_path,scripts_path,subordinatename,subordinateip,subordinate_platform):
    git_add_cmd = "git add " + scripts_path    
    subprocess.call(git_add_cmd, cwd = src_scripts_path, shell = True)
    
    git_commit_cmd = "git commit %s -m 'new add for %s'" % (scripts_path, subordinatename)
    subprocess.call(git_commit_cmd, cwd = src_scripts_path, shell = True)
    
    git_push_origin = "git push origin main"
    subprocess.call(git_push_origin, cwd = src_scripts_path, shell = True)
    log.info("first git push success!")


def git_commit(src_scripts_path, scripts_path, subordinatename,subordinateip,subordinate_platform):
    git_commit_cmd = "git commit %s -m 'update for %s'" % (scripts_path, subordinatename)
    subprocess.call(git_commit_cmd, cwd = src_scripts_path, shell = True)
    git_push_origin = "git push origin main"
    subprocess.call(git_push_origin, cwd = src_scripts_path, shell = True)
    log.info("git push success!")


def git_clone(subordinate_scripts_path,subordinatename,subordinateip,subordinate_platform):
    git_url = "git@10.10.2.31:documents/buildsystem.git"
    git_clone_cmd = "git clone " + git_url + " " + subordinate_scripts_path
    salt_cmd_git_clone = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + git_clone_cmd + '"'
    log.info("git clone cmd is: " + git_clone_cmd)    

    p2 = subprocess.Popen(salt_cmd_git_clone, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out2 = p2.stdout.read()
    err2 = p2.stderr.read()
    log.info("out2 " + out2)
    log.info("err2 " + err2)
    log.info("salt cmd git clone: " + salt_cmd_git_clone)
    log.info("git clone successfully!")

def git_pull(subordinate_scripts_path, subordinateip, subordinate_platform):
    git_pull_cmd = "git pull "# + subordinate_scripts_path
    salt_cmd_git_pull = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + git_pull_cmd + '"'
    subprocess.Popen(salt_cmd_git_pull, cwd = subordinate_scripts_path, shell = True)
    

def get_submit_script_content_values(post_dict):
    script_content_list = []
    for each_key in post_dict.keys():
        if "script_content" in each_key:
            script_content_list.append(each_key)
    return script_content_list

@csrf_exempt
def create_new_build(request):
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
    if not start_method:
        return render_to_response("error.html")
    for each_value in request.POST.values():
        if not each_value.strip():
            return render_to_response("error.html")
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
    
    old_main,main_template,new_main,factory_template,new_factory,src_scripts_path,scripts_path,subordinate_source_path,subordinate_scripts_path,builder_waterfall_address = get_params(subordinate_platform,subordinatename,buildername)
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
    
    script_content_list = get_submit_script_content_values(request.POST)
    if table_length > 0:
        for each_key in script_content_list:
            each_num = each_key.replace("script_content","")
            if not os.path.exists(scripts_path):
                os.makedirs(scripts_path, mode = 0777)
            if subordinate_platform == "Win":
                filename = "script" + each_num + ".bat"    
            else:
                filename = "script" + each_num + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/") 
            subordinate_script_file = os.path.join(os.path.join(subordinate_scripts_path,subordinatename), filename).replace("\\","/")
            write_file(script_file, request.POST[each_key])
            build_steps = Build_Steps(build_info_id = build_info_id, script_content = script_file,subordinate_script_file = subordinate_script_file, \
                                  work_dir = request.POST["work_dir" + each_num], description = request.POST["description" + each_num])
            build_steps.save()
    log.info("-----------------------------begin----------------------------------\n")
    log.info("main ip is: %s" % mainip)
    log.info("subordinate ip is: %s" % subordinateip)
    log.info("subordinate platform is: %s" % subordinate_platform)
    log.info("subordinatename is: %s" % subordinatename)
    log.info("buildername is: %s" % buildername)
    #make_dirs(subordinate_source_path,subordinate_scripts_path,subordinate_platform,subordinateip)
    git_first_commit(src_scripts_path,scripts_path,subordinatename,subordinateip, subordinate_platform)
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    log.info(send_mail_list)
    subordinate_path = os.path.join(subordinate_source_path, subordinatename)
    create_subordinate(mainip,subordinate_path,subordinateip,subordinate_platform,subordinatename)
    create_new_main(main_template,buildername,subordinatename,git_project_path,branches_list,monitor_file_path,hour,minute,new_main,send_mail_list,git_project_path_flag)
    import_new_main(old_main,buildername)
    create_new_factory(build_info_id,subordinate_platform,factory_template,new_factory)
    restart_main()
    
    git_clone(subordinate_scripts_path,subordinatename,subordinateip,subordinate_platform)
    start_subordinate_script(subordinateip,subordinate_platform,subordinate_source_path,subordinatename)
    log.info("-----------------------------end----------------------------------\n")
    return render_to_response("success.html",{"builder_waterfall_address":builder_waterfall_address})

#fen ye xian shi
def display_all_records(request):
    per_page_count = 20
    nowpage = request.GET.get("nowpage","").strip()
    if nowpage == "":
        nowpage = 1
    else:
        nowpage = int(nowpage)
    count = Build_Info.objects.all().count()
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
    build_info = Build_Info.objects.all()[start:(start + per_page_count)]
    return render_to_response("display_all_records.html", locals())


#fen ye xian shi
def display_all_used_records(request):
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
    return render_to_response("display_all_used_records.html", locals())

#display each record details
def display_details(request,params):
    build_info = Build_Info.objects.get(id = params)
    build_steps = Build_Steps.objects.filter(build_info_id = params).order_by("subordinate_script_file")
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
        build_info = temp_build_info
        if not build_info:
            return HttpResponseRedirect("/empty/")
        
    elif search_name == "buildername" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["buildername like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        build_info = temp_build_info
        if not build_info:
            return HttpResponseRedirect("/empty/")
    elif search_name == "subordinate_platform" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["subordinate_platform like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        build_info = temp_build_info
        if not build_info:
            return HttpResponseRedirect("/empty/")
    elif search_name == "username" and record_name:
        temp_build_info = Build_Info.objects.extra(where = ["username like'%%" + str(record_name) + "%%'"])
        build_info = temp_build_info.filter(flag = 1)
        build_info = temp_build_info
        if not build_info:
            return HttpResponseRedirect("/empty/")
    else:
        return HttpResponseRedirect("/display_all_used_records/")
    return render_to_response("display_all_records.html",locals())
    return render_to_response("display_all_used_records.html",locals())



def update_info_page(request, params):
    if request.session.has_key("username"):
        hours = [i for i in xrange(24)]
        minutes = [i for i in xrange(60)]
        build_info= Build_Info.objects.get(id = params)
        build_steps = Build_Steps.objects.filter(build_info_id = params).order_by("subordinate_script_file")
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
    build_steps = Build_Steps.objects.filter(build_info_id=params).order_by("subordinate_script_file")
    mainip = request.POST.get("mainip", "").strip()
    subordinateip = request.POST.get("subordinateip", "").strip()
    subordinate_platform = request.POST.get("subordinate_platform", "").strip()
    subordinatename = request.POST.get("subordinatename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    start_method = request.POST.get("start_method", "").strip()
    username = request.POST.get("username", "").strip()
    username = request.session["username"]
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

    log.info("-----------------------------begin----------------------------------\n")
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
                      monitor_file_path = monitor_file_path,send_mail = send_mail, flag = 1)



    old_main,main_template,new_main,factory_template,new_factory,src_scripts_path,scripts_path,subordinate_source_path,subordinate_scripts_path,builder_waterfall_address = get_params(subordinate_platform,subordinatename,buildername)
    all_length = len(request.POST)
    all_count = build_steps.count()

    #delete old steps before save new steps
    for each_build_step in build_steps:
        each_step = Build_Steps.objects.get(id = each_build_step.id)
        each_step.delete()

    #save new steps    
    if all_count > 0:
        for each_num in xrange(1,all_count+1):
            if not os.path.exists(scripts_path):
                os.makedirs(scripts_path, mode = 0777)
            if subordinate_platform == "Win":
                filename = "script" + str(each_num) + ".bat"    
            else:
                filename = "script" + str(each_num) + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/") 
            subordinate_script_file = os.path.join(os.path.join(subordinate_scripts_path,subordinatename), filename).replace("\\","/")
            if request.POST.has_key("script_content" + str(each_num)): 
                write_file(script_file, request.POST["script_content" + str(each_num)])
                new_build_steps = Build_Steps(build_info_id = params, script_content = script_file,subordinate_script_file = subordinate_script_file, \
                                  work_dir = request.POST["work_dir" + str(each_num)], description = request.POST["description" + str(each_num)])
                new_build_steps.save()

    """
    all_count = build_steps.count()
    if all_count > 0:
        for each_num in xrange(1,all_count+1):
            if subordinate_platform == "Win":
                filename = "script" + str(each_num) + ".bat"    
            else:
                filename = "script" + str(each_num) + ".sh"
            script_file = os.path.join(scripts_path, filename).replace("\\","/")
            if request.POST.has_key("script_content" + str(each_num)):
                #return HttpResponse("script_content" + str(each_num))
                write_file(script_file, request.POST["script_content" + str(each_num)])
                each_step = build_steps.filter(script_content = script_file)
                each_step.update(build_info_id = params, script_content = script_file,\
                             work_dir = request.POST["work_dir" + str(each_num)], description = request.POST["description" + str(each_num)])

    """
    log.info("update success!!")
    branches_list = deal_with_data(branches)
    send_mail_list = deal_with_data(send_mail)
    create_new_main(main_template,buildername,subordinatename,git_project_path,branches_list,monitor_file_path,hour,minute,new_main,send_mail_list,git_project_path_flag)
    create_new_factory(params,subordinate_platform,factory_template,new_factory)
    git_commit(os.path.dirname(scripts_path), scripts_path, subordinatename,subordinateip,subordinate_platform)
    #git_pull(subordinate_scripts_path, subordinateip, subordinate_platform)
    restart_main()
    log.info("-----------------------------end----------------------------------\n")
    return render_to_response("update_success.html",{"builder_waterfall_address":builder_waterfall_address})


def delete_files(filename):
    if os.path.exists(filename):
        os.remove(filename)
        log.info("delete %s!" % filename)

def stop_subordinate(subordinateip,subordinate_platform,subordinate_source_path,subordinatename):
    try:
        log.info("begin to stop subordinate: %s!" % subordinatename)
        stop_subordinate_cmd = "buildsubordinate stop " + os.path.join(subordinate_source_path,subordinatename)
        salt_cmd = 'echo "123456"|sudo -S salt "' + subordinate_platform.lower() + "_" + subordinateip + '" cmd.run "' + stop_subordinate_cmd + '"'
        subprocess.Popen(salt_cmd, shell = True)
        log.info("stop subordinate cmd is: " + salt_cmd)
        log.info("stop subordinate: %s successfully!" % subordinatename)
    except Exception, e:
        log.info(str(e))

def update_main(mainip,buildername):
    old_main = r"/home/goland/buildbot/main/main.cfg"
    main_content_lines = read_file_lines(old_main)
    new_line_list = []
    flag = 0
    for each_line in main_content_lines:
        if each_line.strip().startswith("import main_" + buildername) and each_line.strip().endswith("import main_" + buildername):
            log.info("remove this line: %s" % each_line)
            flag = 1
        elif each_line.strip().startswith("c = main_" + buildername + ".update_params_dict(c)"):
            log.info("remove this line: %s" % each_line)
            flag = 1
        else:
            new_line_list.append(each_line)
    if flag:
        log.info("create new main conf file")
        fp = open(old_main, "w")
        for each_line in new_line_list:
            fp.write(each_line)
        fp.close()
        log.info("remove builder %s conf from main conf file" % buildername)
        

def delete(request, params):
    if request.session.has_key("username"):
        build_info = Build_Info.objects.get(id=params)
        mainip = build_info.mainip
        build_steps = Build_Steps.objects.filter(build_info_id=params)
        build_info.flag = 2
        build_info.save()
        mainip = build_info.mainip
        subordinateip = build_info.subordinateip
        subordinatename = build_info.subordinatename
        subordinate_platform = build_info.subordinate_platform
        buildername = build_info.buildername
        old_main,main_template,new_main,factory_template,new_factory,src_scripts_path,scripts_path,subordinate_source_path,subordinate_scripts_path,builder_waterfall_address = get_params(subordinate_platform,subordinatename,buildername)
        stop_subordinate(subordinateip,subordinate_platform,subordinate_source_path,subordinatename)
        update_main(mainip,buildername)
        restart_main()
        return HttpResponseRedirect("/display_all_used_records/")
    else:
        return HttpResponse("<body style = 'background-color:#77ac98'><a href = '/login/'>请先登录</a></body>")


