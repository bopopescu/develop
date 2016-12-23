#-*- encoding:utf-8 -*-

#standard lib
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib import auth
#from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db import transaction

import random
import os
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import time
import re
import threading
import StringIO
import smtplib
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#3rd lib
import xlwt

#local lib
from models import Platform, PC_Info, Record, DepartMent, Staff_Info, IP
from auto_om.settings import BASE_DIR

LOG_FILE = "auto_om.log"
PING_COUNT = 2
ONLINE = "online"
OFFLINE = "offline"
STATUS = []
ADMIN_USER_EMAIL_LIST = ["dedong.xu@goland.cn"]#, "feng.yue@goland.cn"]


def log(info):
    """ record log """
    logging.basicConfig(filename = os.path.join(BASE_DIR, LOG_FILE), level = logging.NOTSET, filemode = "a", format = "%(asctime)s : %(message)s")
    logging.info(info)


def log_size(info, logfile = LOG_FILE, mode = "a", levelname = logging.NOTSET, maxBytes = 50*1024*1024, backupCount = 10):
    """ 可以设定log文件的大小，当超过设定的值时，就将当前文件重命名，然后创建一个新的同名日志文件 """
    Rthandler = RotatingFileHandler(logfile, mode = mode, maxBytes = maxBytes, backupCount = backupCount)
    log_format = "%(asctime)s : %(levelname)s : %(message)s"
    formatter = logging.Formatter(log_format)
    Rthandler.setFormatter(formatter)
    log = logging.getLogger()
    log.setLevel(levelname)
    log.addHandler(Rthandler)
    logging.info(info)
    log.removeHandler(Rthandler)


def multi_send_mail(mail_list, sub, content):
    """ 多线程发送邮件 """
    for mail_to_one in mail_list:
        t = threading.Thread(target = send_mail, args = (mail_to_one, sub, content))
        t.start()


def send_mail(to_one,sub,content):
    """ 发邮件 """
    mail_host="10.10.7.100"  #set mail server
    mail_user="buildbot"    #usename
    mail_pass="123456"   #password
    mail_postfix="goland.cn"  #
        
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = to_one  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.starttls()  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_one, msg.as_string())  
        server.close()
        #log.info("send mail successfully!")
        return True  
    except Exception, e:  
        #log.info("send mail failed: %s" % str(e)) 
        return False



@transaction.commit_on_success
def test(request):
    """ 
    装饰器这样的写法，只要views里加入异常保护，即便出错，之前保存的也不会回滚;所以不好。
    use Django transaction commit on success 
    """
    name = request.GET.get("name", "").strip()
    pc_info_list = PC_Info.objects.all()
    try:
        for i in xrange(len(pc_info_list)):
            if i == len(pc_info_list)-1:
                dsfsdfs
            pc_info_list[i].description = name
            pc_info_list[i].save()
    except:
        pass
    return HttpResponseRedirect("/")


def test1(request):
    name = request.GET.get("name", "").strip()
    pc_info_list = PC_Info.objects.all()
    try:    
        for i in xrange(len(pc_info_list)):
            if i == len(pc_info_list)-1:
                #try:
                    dsfsdfs
                #except:
                #    return  HttpResponseRedirect("/")
            pc_info_list[i].description = name
            pc_info_list[i].save()
    except:
        pass
    return HttpResponseRedirect("/")


@transaction.autocommit
def test2(request):
    """ use Django transaction auto commit """
    name = request.GET.get("name", "").strip()
    pc_info_list = PC_Info.objects.all()
    for i in xrange(len(pc_info_list)):
        if i == len(pc_info_list)-1:
            #try:
                dsfsdfs
            #except:
            #    return  HttpResponseRedirect("/")
        pc_info_list[i].description = name
        pc_info_list[i].save()
    return HttpResponseRedirect("/")


def test3(request):
    """ use Django transaction auto commit """
    name = request.GET.get("name", "").strip()
    pc_info_list = PC_Info.objects.all()
    try:
        with transaction.autocommit():
        #with transaction.atoimic():  no this method
        #with transaction.commiti_manually():
            for i in xrange(len(pc_info_list)):
                if i == len(pc_info_list)-1:
                    dsfsdfs
                pc_info_list[i].description = name
                pc_info_list[i].save()
    except Exception, e:
        pass
    return HttpResponseRedirect("/")


def test4(request):
    """ 
    建议使用这样的写法，使用with语句，即使加入了异常保护，views函数不会出错,但是有异常发生；最后一次的保存失败，之前的保存也会回滚的
    use Django transaction commit on success 
    """
    name = request.GET.get("name", "").strip()
    pc_info_list = PC_Info.objects.all()
    try:
        with transaction.commit_on_success():
            for i in xrange(len(pc_info_list)):
                if i == len(pc_info_list)-1:
                    dsfsdfs
                pc_info_list[i].description = name
                pc_info_list[i].save()
    except Exception, e:
        pass
    return HttpResponseRedirect("/")


@csrf_exempt
def login(request, template_name = "login.html"):
    """ login """
    if request.session.has_key("username"):
        return HttpResponseRedirect("/")
    redirect_url = request.GET.get("next", "").strip()
    if not redirect_url:
        redirect_url = "/"
    elif not redirect_url.startswith("/"):
        redirect_url = "/" + redirect_url
    #return HttpResponse(redirect_url)
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = auth.authenticate(username = username, password = password)
        if user is not None:# and user.has_perm("om.can_vote"):
            auth.login(request, user)
            request.session["username"] = username
            if not request.user.is_staff:
                return HttpResponseRedirect("/create_virtual/")
            return HttpResponseRedirect(redirect_url)
        else:
            failed_prompt = "username and password didn't match!"
    return render_to_response(template_name, locals())


def logout(request):
    """ logout """
    redirect_url = request.GET.get("next", "").strip()
    auth.logout(request)
    return HttpResponseRedirect(redirect_url)


def search_result(pc_info_list, search_list, search_name, record_name):
    """ search result by condition """
    for each_record in search_list:
        if each_record == search_name:
            if search_name.lower() == "platform":
                try:
                    #platform = Platform.objects.get(name__icontains = record_name)
                    #pc_info_list = platform.platform_set.all()
                    pc_info_list = pc_info_list.filter(platform__name__icontains = record_name)
                except Exception as e:
                    log("search result platform exception, %s" % str(e))
                    pc_info_list = []
            elif search_name.lower() == "department":
                try:
                    pc_info_list = pc_info_list.filter(department__name__icontains = record_name)
                except Exception as e:
                    log("search result description exception, %s" % str(e))
                    pc_info_list = []
            else:
                search_str = "%s like '%%%%%s%%%%'" % (search_name, record_name)
                pc_info_list = pc_info_list.extra(where = [search_str])
            break
    return pc_info_list

def staff_required(user, login_url = None):
    """ required current user is staff """
    if user.is_staff:
        return True
    return False

def superuser_required(user, login_url = None):
    """ required current user is superuser """
    if user.is_superuser:
        return True
    return False


def superuser_required1(user, login_url = None, raise_exception = False):
    def check_perms(user):
        if user.is_superuser:
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url = login_url)


def display_user_permission(request):
    redirect_url = request.GET.get("next", "").strip()
    return render_to_response("display_user_permission.html", locals())



#@user_passes_test(lambda u: u.has_perm("om.can_vote"), login_url = "/add_pc/")
#@permission_required("om.can_vote", login_url = "/add_pc/")#, raise_exception = 1)
@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
#@superuser_required
def index1(request):
    """ display all pc info """
    redirect_url = request.get_full_path()
    search_list = ["platform", "ip", "username", "is_virtual"]
    cur_time = time.time()
    pc_info_list = PC_Info.objects.all()
    search_name = request.GET.get("search_name", "").strip()
    record_name = request.GET.get("record_name", "").strip()
    pc_info_list = search_result(pc_info_list, search_name, record_name)
    ip_list = [pc_info.ip for pc_info in pc_info_list]
    multi_all_run(pc_info_list)
    locals().update({"ONLINE": ONLINE, "OFFLINE": OFFLINE})
    return render_to_response("index.html", locals())


def order_list(pc_info_list, record_list, ziduan, order):
    """ get the order """
    for record in record_list:
        if ziduan == record:
            if order == "1" or order == "":
                pc_info_list = pc_info_list.order_by(ziduan)
                order = 2
            elif order == "2":
                pc_info_list = pc_info_list.order_by("-"+ziduan)
                order = 1
            else:
                order = 1
                pc_info_list = pc_info_list
            break
    return pc_info_list, order

#@user_passes_test(lambda u: u.has_perm("om.can_vote"), login_url = "/add_pc/")
#@permission_required("om.can_vote", login_url = "/add_pc/")#, raise_exception = 1)
@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
#@superuser_required
def index(request, template, model, search_list, record_list, total_pc_flag):
    """ display all pc info """
    is_esxi = False
    li = [i for i in xrange(10)]
    redirect_url = request.get_full_path()
    cur_time = time.time()
    
    """ 
    下面这两句代码意思一样,都是去除ESXi系统的集合 
    pc_info_list = PC_Info.objects.exclude(platform__pk = 4)
    pc_info_list = PC_Info.objects.exclude(platform__name__iexact = "ESXi")
    """
    pc_info_list = model.objects.all()

    search_name = request.GET.get("search_name", "").strip()
    record_name = request.GET.get("record_name", "").strip()
    pc_info_list = search_result(pc_info_list, search_list, search_name, record_name)
    ziduan = request.GET.get("ziduan", "")
    order = request.GET.get("order", "1")
    pc_info_list, order = order_list(pc_info_list, record_list, ziduan, order)
    if total_pc_flag:
        total_memory, total_cpu, total_hard_disk = get_virtual_total_info(pc_info_list)    
    ip_list = [pc_info.ip for pc_info in pc_info_list]
    multi_all_run([pc_info for pc_info in pc_info_list if pc_info.ip])
    locals().update({"ONLINE": ONLINE, "OFFLINE": OFFLINE})
    total_pc = len(pc_info_list)
    total_running_pc = len([i for i in pc_info_list if i.status == ONLINE])
    return render_to_response(template, locals())


def get_virtual_total_info(pc_info_list):
    """ 获取所有的正在运行的虚拟机的内存，CPU以及硬盘的总和 """
    condition_dict = {"is_virtual": "yes", "status": "online"}
    #info_list = pc_info_list.filter(is_virtual = "yes", status = "online")
    info_list = pc_info_list.filter(**condition_dict)
    total_memory = total_cpu = total_hard_disk = 0
    for each_info in info_list:
        total_memory += get_digit_str(each_info.memory)[0]
        total_cpu += get_digit_str(each_info.cpu)[0]
        total_hard_disk += get_digit_str(each_info.hard_disk)[0]
    return total_memory, total_cpu, total_hard_disk

#下面的代码没用,但是暂作保留
@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
def display_esxi(request):
    """ display all esxi pc info """
    is_esxi = True
    redirect_url = request.get_full_path()
    search_list = ["ip", "username", "is_virtual"]
    cur_time = time.time()
    
    """ 下面这两句代码意思一样 """
    pc_info_list = PC_Info.objects.filter(platform__pk = 4)
    pc_info_list = PC_Info.objects.filter(platform__name__iexact = "ESXi")
    
    search_name = request.GET.get("search_name", "").strip()
    record_name = request.GET.get("record_name", "").strip()
    pc_info_list = search_result(pc_info_list, search_name, record_name)
    
    ziduan = request.GET.get("ziduan", "")
    order = request.GET.get("order", "")
    pc_info_list, order = order_list(pc_info_list, ziduan, order)
    
    ip_list = [pc_info.ip for pc_info in pc_info_list]
    multi_all_run(pc_info_list)
    locals().update({"ONLINE": ONLINE, "OFFLINE": OFFLINE})
    return render_to_response("index.html", locals())


def multi_all_run(pc_info_list):
    """ use multi process to run run_ping_analyze_update """
    for pc_info in pc_info_list:
        ip = pc_info.ip
        t = threading.Thread(target = run_ping_analyze_update, args = (pc_info, ip))
        t.setDaemon(False)
        t.start()
        #print ip, t.isAlive(), t.isDaemon(), t.getName()

def run_ping_analyze_update(pc_info, ip):
    """ ping pc; analyze ping result; then update pc status """
    status = analyze_ping_result(ping(ip))
    update_status(pc_info, status)


def update_status(pc_info, status):
    """ update pc status  """
    pc_info.status = status
    pc_info.save()


"""
def new_multi_all_run(pc_info_list):
    for pc_info in pc_info_list:
        ip = pc_info.ip
        t = threading.Thread(target = get_ping_result, args = (pc_info, ip))
        t.setDaemon(False)
        t.start()
    
def get_ping_result(pc_info, ip):
    for i in xrange(PING_COUNT):
        t = threading.Thread(target = new_ping, args = (ip,))
        t.start()
    if STATUS:
        update_status(pc_info, ONLINE)
        clear_list(STATUS)
    else:
        update_status(pc_info, OFFLINE)

       
def clear_list(the_list):
    while the_list:
        the_list.pop()


def get_status():
    for i in xrange(PING_COUNT):
        t = threading.Thread(target = new_ping, args = (ip,))
        t.start()
    if STATUS:
        status = ONLINE
        clear_list(STATUS)
    else:
        status = OFFLINE

def new_ping(ip):
    ping_cmd = "ping %s -c 1" % (ip)
    p = subprocess.Popen(ping_cmd, stdout = subprocess.PIPE, shell = True)
    all_lines = p.stdout.readlines()
    analyze_line = ""
    for line in all_lines:
        if line.find("packet") != -1 and line.find("loss") != -1 and line.find("%") != -1:
            analyze_line = line
            break
    pattern = r"(\d+)(\%)"
    search_result = re.search(pattern, analyze_line)
    if search_result:
        get_result = int(search_result.group(1))
    else:
        get_result = 100
    if get_result == 0:
        STATUS.append(ONLINE)
    print "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", ip#, STATUS
"""


def ping(ip):
    """ ping ip """
    ping_file = os.path.join(BASE_DIR, "ping", ip)
    ping_cmd = "ping %s -c %d > %s" % (ip, PING_COUNT, ping_file)
    try:
        os.system(ping_cmd)
    except Exception as e:
        log("ping exception: current ip is: %s, exception :%s" % (ip, str(e)))
    return ping_file


def analyze_ping_result(ping_file):
    """ analyze ping result """
    all_lines = read_file_lines(ping_file)
    analyze_line = ""
    for line in all_lines:
        if line.find("packet") != -1 and line.find("loss") != -1 and line.find("%") != -1:
            analyze_line = line
            break
    pattern = r"(\d+)(\%)"
    search_result = re.search(pattern, analyze_line)
    if search_result:
        loss_result = int(search_result.group(1))
    else:
        loss_result = 100
    if loss_result < 100:
        status = ONLINE
    else:
        status = OFFLINE
    return status


def write_file(filename, c):
    """ write file """
    with open(filename, "w") as fp:
        fp.write(c)


def read_file(filename):
    """ read file """
    with open(filename, "r") as fp:
        return fp.read()


def read_file_lines(filename):
    """ read file by lines """
    with open(filename, "r") as fp:
        return fp.readlines()

def save_record(operation_str):
    """ save each operation record """
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S")
    content = "%s at %s" % (operation_str, cur_time)
    record = Record(content = content)
    record.save()


@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
@csrf_exempt
def add_pc(request):
    """ add new pc """
    redirect_url = request.get_full_path()
    platform = Platform.objects.all()
    platform_list = [""] + [i.name for i in platform]
    if request.method == "POST":
        platform = request.POST.get("platform", "").strip()
        ip = request.POST.get("ip", "").strip()
        memory = request.POST.get("memory", "").strip()
        cpu = request.POST.get("cpu", "").strip()
        hard_disk = request.POST.get("hard_disk", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        is_virtual = request.POST.get("is_virtual", "").strip()
        description = request.POST.get("description", "").strip()
        modify_date = join_date = time.strftime("%Y-%m-%d %H:%M:%S")
        platform_obj = Platform.objects.get(name = platform)
        try:
            PC_Info.objects.get(ip = ip)
            exist_prompt = "ip: %s already exists!" % ip
        except Exception:
            if all([ip]):
            #if all([platform, ip, memory, cpu, hard_disk, username, password, is_virtual, description, join_date, modify_date]):
                #ip_pattern = r"^[\d\.]+$" 
                #ip_pattern = r"\d{2}\.\d{2}\.\d{1}\.\d{1,3}" 
                #if not re.search(ip_pattern, ip):
                #    return HttpResponse("ip格式不正确，请重新填写！格式为xx.xx.x.x(x)(x)；括号里表示非必须")
                #hard_disk_pattern = r"^(\d+)([MmGg])$"
                #if not re.search(hard_disk_pattern, hard_disk):
                #    return HttpResponse("hard disk 那一项输入不正确,格式应类似：100G。数字在前，单位为G或M，不区分大小写！")
                if hard_disk and hard_disk[-1].isdigit():
                    hard_disk += "G"
                #status = analyze_ping_result(ping(ip))
                status = "offline"
                try:
                    with transaction.commit_on_success():
                        pc_info = PC_Info(platform = platform_obj, ip = ip, memory = memory, memory_left = memory, cpu = cpu, cpu_left = cpu,\
                        hard_disk = hard_disk, hard_disk_left = hard_disk, username = username, password = password,is_virtual = is_virtual,\
                        join_date = join_date, modify_date = modify_date, status = status,description = description)
                        pc_info.save()
                        save_record("%s add new pc: %s" % (request.user, ip))
                        sub = "Add New PC"
                        content = "Hello, %s add new pc: %s, platform is: %s" % (request.user, ip, platform)
                        mail_list = ADMIN_USER_EMAIL_LIST + [get_cur_user_email(request.session["username"], "@goland.cn")]
                        multi_send_mail(mail_list, sub, content)
                except Exception, e:
                    log("add pc exception, %s" % str(e))
                return HttpResponseRedirect("/")
    return render_to_response("add_pc.html", locals())


@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
@csrf_exempt
def update(request, params = None):
    """ update pc info """
    redirect_url = request.get_full_path()
    if params is None and request.method == "GET":
        params = request.GET.get("id", "").strip()
    if not params.isdigit():
        raise Http404
    
    platform_list = Platform.objects.all()
    pc_info = PC_Info.objects.select_related().get(id = params)
    cur_platform = pc_info.platform.name
    if request.method == "POST":
        platform = request.POST.get("platform", "").strip()
        ip = request.POST.get("ip", "").strip()
        memory = request.POST.get("memory", "").strip()
        memory_left = request.POST.get("memory_left", "").strip()
        cpu = request.POST.get("cpu", "").strip()
        cpu_left = request.POST.get("cpu_left", "").strip()
        hard_disk = request.POST.get("hard_disk", "").strip()
        hard_disk_left = request.POST.get("hard_disk_left", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        is_virtual = request.POST.get("is_virtual", "").strip()
        description = request.POST.get("description", "").strip()
        modify_date = time.strftime("%Y-%m-%d %H:%M:%S")
        platform_obj = Platform.objects.get(name = platform)
        pc_count = PC_Info.objects.filter(ip = ip).exclude(id = params).count()
        if pc_count >= 1:
            exist_prompt = "ip: %s already exists!" % ip
        elif all([ip]):
        #elif all([platform, ip, memory, cpu, hard_disk, username, password, is_virtual, description, modify_date]):
            #ip_pattern = r"\d{2}\.\d{2}\.\d{1}\.\d{1,3}" 
            #if not re.search(ip_pattern, ip):
            #    return HttpResponse("ip格式不正确，请重新填写！格式为xx.xx.x.x(x)(x)；括号里表示非必须")
            #hard_disk_pattern = r"^(\d+)([MmGg])$"
            #if not re.search(hard_disk_pattern, hard_disk):
            #    return HttpResponse("hard disk 那一项输入不正确,格式应类似：100G。数字在前，单位为G或M，不区分大小写！")
            #status = analyze_ping_result(ping(ip))
            status = "offline"
            pc_info.platform = platform_obj
            pc_info.ip = ip
            pc_info.memory = memory
            pc_info.cpu = cpu
            pc_info.hard_disk = hard_disk
            pc_info.username = username
            pc_info.password = password
            pc_info.is_virtual = is_virtual
            pc_info.description = description
            pc_info.modify_date = modify_date
            pc_info.status = status
            if platform.upper() == "ESXI":
                pc_info.memory_left = memory_left
                pc_info.cpu_left = cpu_left
                pc_info.hard_disk_left = hard_disk_left
            try:
                with transaction.commit_on_success():
                    pc_info.save()
                    save_record("%s update pc: %s" % (request.user, ip))
                    sub = "Update PC"
                    content = "Hello, %s update pc: %s, platform is: %s" % (request.user, ip, platform)
                    mail_list = ADMIN_USER_EMAIL_LIST + [get_cur_user_email(request.session["username"], "@goland.cn")]
                    multi_send_mail(mail_list, sub, content)
            except Exception, e:
                log("update pc exception, %s" % str(e))
            return HttpResponseRedirect("/")
    return render_to_response("update.html", locals())


@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
@csrf_exempt
def delete(request, model, url, params = None):
    """ delete pc info """
    if params is None and request.method == "GET":
        params = request.GET.get("id", "").strip()
    if not params.isdigit():
        raise Http404
   
    try:
        with transaction.commit_on_success():
            model_info = model.objects.get(id = int(params))
            model_info.delete()
            save_record("%s delete pc: %s" % (request.user, model_info.ip))
            sub = "Delete PC"
            content = "Hello, %s delete pc: %s, platform is: %s" % (request.user, model_info.ip, model_info.platform.name)
            mail_list = ADMIN_USER_EMAIL_LIST + [get_cur_user_email(request.session["username"], "@goland.cn")]
            multi_send_mail(mail_list, sub, content)
    except Exception, e:
        pass
        #log("delete exception, %s" % str(e))
    return HttpResponseRedirect(url)

#@user_passes_test(lambda u: u.has_perm("om.can_vote"), login_url = "/add_pc/")
#@permission_required("om.can_vote", login_url = "/add_pc/")#, raise_exception = 1)
@login_required
@user_passes_test(staff_required, login_url = "/display_user_permission/")
#@superuser_required
def display_staff_info(request, template, model, search_list, record_list, total_pc_flag):
    """ display all pc info """
    is_esxi = False
    li = [i for i in xrange(10)]
    redirect_url = request.get_full_path()
    cur_time = time.time()
    
    """ 
    下面这两句代码意思一样,都是去除ESXi系统的集合 
    pc_info_list = PC_Info.objects.exclude(platform__pk = 4)
    pc_info_list = PC_Info.objects.exclude(platform__name__iexact = "ESXi")
    """
    pc_info_list = model.objects.all()

    search_name = request.GET.get("search_name", "").strip()
    record_name = request.GET.get("record_name", "").strip()
    pc_info_list = search_result(pc_info_list, search_list, search_name, record_name)
    #pc_info_list =     
    ziduan = request.GET.get("ziduan", "")
    order = request.GET.get("order", "1")
    pc_info_list, order = order_list(pc_info_list, record_list, ziduan, order)
    if total_pc_flag:
        total_memory, total_cpu, total_hard_disk = get_virtual_total_info(pc_info_list)    
    ip_list = [pc_info.ip for pc_info in pc_info_list]
    #multi_all_run(pc_info_list)
    multi_all_run([pc_info for pc_info in pc_info_list if pc_info.ip])
    locals().update({"ONLINE": ONLINE, "OFFLINE": OFFLINE})
    total_pc = len(pc_info_list)
    page, paginator, page_range, pc_info_list = fenye(request, pc_info_list)
    record_list = pc_info_list
    return render_to_response(template, locals())


def add_str(mystr, substr):
    """ 如果字符串最后一位是数字的话，加上它给定的字符串 """
    if mystr and mystr[-1].isdigit():
        mystr += substr
    return mystr


@login_required
@user_passes_test(staff_required, login_url = "/display_user_permission/")
@csrf_exempt
def add_staff_info(request):
    """ add staff info """
    redirect_url = request.get_full_path()
    platform = Platform.objects.all()
    department = DepartMent.objects.all()
    platform_list = [""] + [i.name for i in platform][:-2]
    department_list = [""] + [i.name for i in department]
    if request.method == "POST":
        platform = request.POST.get("platform", "").strip()
        department = request.POST.get("department", "").strip()
        staff_name = request.POST.get("staff_name", "").strip()
        ip = request.POST.get("ip", "").strip()
        mac_address = request.POST.get("mac_address", "").strip()
        asset_name = request.POST.get("asset_name", "").strip()
        serial_num = request.POST.get("serial_num", "").strip()
        asset_address = request.POST.get("asset_address", "").strip()
        memory = request.POST.get("memory", "").strip()
        cpu = request.POST.get("cpu", "").strip()
        hard_disk = request.POST.get("hard_disk", "").strip()
        description = request.POST.get("description", "").strip()
        modify_date = join_date = time.strftime("%Y-%m-%d %H:%M:%S")
        platform_obj = Platform.objects.get(name = platform)
        department_obj = DepartMent.objects.get(name = department)
        try:
            PC_Info.objects.get(ip = ip)
            exist_prompt = "ip: %s already exists!" % ip
        except Exception:
            if all([platform, department]):
                memory = add_str(memory, "G")
                hard_disk = add_str(hard_disk, "G")
                #status = analyze_ping_result(ping(ip))
                status = "offline"
                #try:
                with transaction.commit_on_success():
                        staff_info = Staff_Info(platform = platform_obj, department = department_obj, staff_name = staff_name, \
                        asset_name = asset_name, serial_num = serial_num, asset_address = asset_address, ip = ip, mac_address = mac_address,\
                        memory = memory, cpu = cpu, hard_disk = hard_disk,join_date = join_date, modify_date = modify_date, status = status,\
                        description = description)
                        staff_info.save()
                        save_record("%s add new pc: %s" % (request.user, ip))
                #except Exception, e:
                #    log("add staff into exception, %s" % str(e))
                return HttpResponseRedirect("/display_staff_info")
    return render_to_response("add_staff_info.html", locals())


@login_required
@user_passes_test(staff_required, login_url = "/display_user_permission/")
@csrf_exempt
def update_staff_info(request, params = None):
    """ update staff info """
    redirect_url = request.get_full_path()
    if params is None and request.method == "GET":
        params = request.GET.get("id", "").strip()
    if not params.isdigit():
        raise Http404
    
    platform_list = Platform.objects.all()
    platform_list = platform_list[0: len(platform_list)-2]
    department_list = DepartMent.objects.all()
    staff_info = Staff_Info.objects.select_related().get(id = params)
    cur_platform = staff_info.platform.name
    cur_department = staff_info.department.name
    if request.method == "POST":
        platform = request.POST.get("platform", "").strip()
        department = request.POST.get("department", "").strip()
        staff_name = request.POST.get("staff_name", "").strip()
        ip = request.POST.get("ip", "").strip()
        mac_address = request.POST.get("mac_address", "").strip()
        asset_name = request.POST.get("asset_name", "").strip()
        serial_num = request.POST.get("serial_num", "").strip()
        asset_address = request.POST.get("asset_address", "").strip()
        memory = request.POST.get("memory", "").strip()
        cpu = request.POST.get("cpu", "").strip()
        hard_disk = request.POST.get("hard_disk", "").strip()
        description = request.POST.get("description", "").strip()
        modify_date = time.strftime("%Y-%m-%d %H:%M:%S")
        platform_obj = Platform.objects.get(name = platform)
        department_obj = DepartMent.objects.get(name = department)
        pc_count = PC_Info.objects.filter(ip = ip).exclude(id = params).count()
        if pc_count >= 1:
            exist_prompt = "ip: %s already exists!" % ip
        elif all([platform, department]):
            memory = add_str(memory, "G")
            hard_disk = add_str(hard_disk, "G")
            status = "offline"
            staff_info.platform = platform_obj
            staff_info.department = department_obj
            staff_info.staff_name = staff_name
            staff_info.ip = ip
            staff_info.mac_address = mac_address
            staff_info.asset_name = asset_name
            staff_info.serial_num = serial_num
            staff_info.asset_address = asset_address
            staff_info.memory = memory
            staff_info.cpu = cpu
            staff_info.hard_disk = hard_disk
            staff_info.description = description
            staff_info.modify_date = modify_date
            staff_info.status = status
            try:
                with transaction.commit_on_success():
                    staff_info.save()
                    save_record("%s update pc: %s" % (request.user, ip))
            except Exception, e:
                log("delete exception, %s" % str(e))
            return HttpResponseRedirect("/display_staff_info")
    return render_to_response("update_staff_info.html", locals())


@login_required
@user_passes_test(staff_required, login_url = "/display_user_permission/")
@csrf_exempt
def delete_staff_info(request, model, url, params = None):
    """ delete pc info """
    if params is None and request.method == "GET":
        params = request.GET.get("id", "").strip()
    if not params.isdigit():
        raise Http404
   
    try:
    #with transaction.commit_on_success():
        model_info = model.objects.get(id = int(params))
        model_info.delete()
        save_record("%s delete pc: %s" % (request.user, model_info.ip))
    except Exception, e:
        log("delete staff info exception, %s" % str(e))
    return HttpResponseRedirect(url)


def get_salt_cmd(platform, ip, cmd, local_passwd = "123456"):
    """ get salt cmd """
    salt_cmd = 'echo "%s" | sudo -S salt "%s_%s" cmd.run "%s"' % (local_passwd, platform.lower(), ip, cmd)
    return salt_cmd


def run_subprocess_popen(cmd):
    """ use subprocess module to run cmd, and get the stdout and stderr """
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.read()
    err = p.stderr.read()
    return out, err


def shutdown_pc(platform, ip, password):
    """ shutdown pc """
    if platform.upper() == "WIN":
        shutdown_cmd = "shutdown -s -t 0"
        #shutdown_cmd = "shutdown -r -t 0"
    elif platform.upper() == "MAC":
        shutdown_cmd = 'echo "%s" | sudo -S shutdown -h now' % password
        #shutdown_cmd = 'echo "%s" | sudo -S reboot' % password
    elif platform.upper() == "UBU":
        shutdown_cmd = 'echo "%s" | sudo -S shutdown -h now' % password
        #shutdown_cmd = 'echo "%s" | sudo -S reboot' % password
    salt_cmd = get_salt_cmd(platform, ip, shutdown_cmd)
    out, err = run_subprocess_popen(salt_cmd)
    #log("out: %s" % out)
    #log("err: %s" % err)


@csrf_exempt
def shutdown_all(request):
    """ shutdown all pc """
    checkbox_list = request.POST.getlist("checkbox")    
    for each_id in checkbox_list:
        pc_info = PC_Info.objects.get(id = each_id)
        platform = pc_info.platform.name
        ip = pc_info.ip
        password = pc_info.password
        if ip == "10.10.2.64":
            continue
        elif ip and password:
            t = threading.Thread(target = shutdown_pc, args = (platform, ip, password))
            t.start()
    return HttpResponseRedirect("/")


@login_required
def display_operation_record(request):
    """ display operation record """
    context = {}
    redirect_url = request.get_full_path()
    record_list1 = Record.objects.all()
    page, paginator, page_range, record_list = fenye(request, record_list1)
    context["request"] = request
    context["redirect_url"] = redirect_url
    context["page"] = page
    context["paginator"] = paginator
    context["page_range"] = page_range
    context["record_list"] = record_list
    return render_to_response("display_operation_record.html", context) 


def fenye(request, record_list):
    """ 分页 """
    after_range_num = 5
    befor_range_num = 4
    each_page_num = 50
    try:
        page = int(request.GET.get("page", "1").strip())
    except ValueError:
        page = 1
    paginator = Paginator(record_list, each_page_num)
    try:
        record_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        page = paginator.num_pages
        record_list = paginator.page(page)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num: page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return page, paginator, page_range, record_list


def get_cpu(platform):
    """ 获取CPU内核数，程序里直接写死, 不允许在页面上输入 """
    cpu_dict = {"win": "2", "mac": "2", "ubu": "1"}
    return cpu_dict[platform.lower()]


def get_memory(platform):
    """ 获取内存大小，程序里直接写死，不允许在页面上输入 """
    memory_dict = {"win": "4G", "mac": "8G", "ubu": "2G"}
    return memory_dict[platform.lower()]


def get_hard_disk(platform):
    """ 获取hard disk，程序里直接写死, 不允许在页面上输入 """
    hard_disk_dict = {"win": "15", "mac": "15", "ubu": "15"}
    return hard_disk_dict[platform.lower()]
    

def get_ip():
    ip_list = IP.objects.filter(flag = 0)
    if ip_list:
        return ip_list[0].name
    else:
        return ""


def run_create_virtual_cmd(esxi_ip):
    """ 执行创建虚拟机的命令 """
    pass


def get_digit_str(s):
    """ 分别获取字符串中的数字与字符串 """
    p = r"(\d+)(\D*)"
    reg = re.match(p, s)
    if reg:
        return int(reg.group(1)), reg.group(2)
    return 0, ""


def get_left_memory_cpu_hard_disk(esxi, memory, cpu, hard_disk):
    """ 减去新创建的虚拟机占用的部分，返回剩下的资源 """
    memory_left, memory_left_str = get_digit_str(esxi.memory_left)
    cpu_left, cpu_left_str = get_digit_str(esxi.cpu_left)
    hard_disk_left, hard_disk_left_str = get_digit_str(esxi.hard_disk_left)
    memory, memory_str = get_digit_str(memory)
    cpu, cpu_str = get_digit_str(cpu)
    hard_disk, hard_disk_str = get_digit_str(hard_disk)

    new_memory_left = str(memory_left - memory) + memory_left_str
    new_cpu_left = str(cpu_left - cpu) + cpu_left_str
    new_hard_disk_left = str(hard_disk_left - hard_disk) + hard_disk_left_str
    return new_memory_left, new_cpu_left, new_hard_disk_left


def get_esxi(memory, cpu, hard_disk):
    """ 获取可用的ESXi服务器来当作即将要创建的虚拟机的载体 """
    list1 = PC_Info.objects.filter(platform__name__icontains = "ESXi")
    list2 = [esxi for esxi in list1 if get_digit_str(esxi.hard_disk_left)[0] > get_digit_str(hard_disk)[0]]
    list3 = [esxi for esxi in list2 if get_digit_str(esxi.memory_left)[0] > get_digit_str(memory)[0]]
    esxi_list = [esxi for esxi in list3 if get_digit_str(esxi.cpu_left)[0] > get_digit_str(cpu)[0]]
    #esxi_list = esxi_list.filter(hard_disk_left__gt = hard_disk).filter(memory_left__gt = memory)#.filter(cpu_left__gt = cpu)
    if not esxi_list:
        return ""
    current_esxi = random.choice(esxi_list)
    return current_esxi


def get_cur_user_email(username, mail_postfix):
    """ 如果不以给定的字符串结尾，则在尾部添加上该字符串 """
    if not username.endswith(mail_postfix):
        username += mail_postfix
    return username


@login_required
@csrf_exempt
def create_virtual(request):
    """ create virtual """
    redirect_url = request.get_full_path()
    platform_list = Platform.objects.all()
    platform_list = [""] + [i.name for i in platform_list][:-2]
    memory_list = ["2", "4", "6", "8"]
    cpu_list = [2, 4, 6, 8]
    if request.method == "POST":
        platform = request.POST.get("platform", "").strip()
        ip = get_ip()
        if not ip:
            not_available_ip = "Sorry, but there is no available ip!"
        else:
            #ip = request.POST.get("ip", "").strip()
            #memory = request.POST.get("memory", "").strip()
            memory = get_memory(platform)
            #cpu = request.POST.get("cpu", "").strip()
            cpu = get_cpu(platform)
            hard_disk = get_hard_disk(platform)
            username = "vidon"
            password = "1"
            #hard_disk = request.POST.get("hard_disk", "").strip()
            #username = request.POST.get("username", "").strip()
            #password = request.POST.get("password", "").strip()
            description = request.POST.get("description", "").strip()
            modify_date = join_date = time.strftime("%Y-%m-%d %H:%M:%S")
            platform_obj = Platform.objects.get(name = platform)
            is_virtual = "yes"
            try:
                PC_Info.objects.get(ip = ip)
                exist_prompt = "ip: %s already exists!" % ip
            except Exception:
                if all([platform, ip, memory, cpu, hard_disk, username, password, description, join_date, modify_date]):
                    ip_pattern = r"\d{2}\.\d{2}\.\d{1}\.\d{1,3}" 
                    if not re.search(ip_pattern, ip):
                        return HttpResponse("ip格式不正确，请重新填写！格式为xx.xx.x.x(x)(x)；括号里表示非必须")
                    hard_disk_pattern = r"^(\d+)([MmGg]?)$"
                    if not re.search(hard_disk_pattern, hard_disk):
                        return HttpResponse("hard disk 那一项输入格式不正确,可以只填写数字，不写单位的话默认为G，不区分大小写！")
                        #return HttpResponse("hard disk 那一项输入不正确,格式应类似：100G。数字在前，单位为G或M，不区分大小写！")
                    if hard_disk and hard_disk[-1].isdigit():
                        hard_disk += "G"
                    esxi = get_esxi(memory, cpu, hard_disk)
                    if not esxi:
                        no_suitable_esxi_prompt = "没有符合要求的机器，请联系管理员!"
                        return render_to_response("create_virtual.html", locals())
                    esxi_ip = esxi.ip
                    #run_create_virtual_cmd(esxi_ip)
                    new_memory_left, new_cpu_left, new_hard_disk_left = get_left_memory_cpu_hard_disk(esxi, memory, cpu, hard_disk)
                    try:
                        with transaction.commit_on_success():
                            pc_info = PC_Info(platform = platform_obj, ip = ip, memory = memory, memory_left = memory, cpu = cpu, cpu_left = cpu,\
                            hard_disk = hard_disk, hard_disk_left = hard_disk, username = username, password = password, is_virtual = is_virtual,\
                            join_date = join_date, modify_date = modify_date, description = description)
                            pc_info.save()
                            esxi.memory_left = new_memory_left
                            esxi.cpu_left = new_cpu_left
                            esxi.hard_disk_left = new_hard_disk_left
                            esxi.save()
                            save_record("%s create virtual: %s" % (request.user, ip))
                            sub = "Create Virtual"
                            content = "Hello, %s create virtual pc: %s, platform is: %s" % (request.user, ip, platform)
                            mail_list = ADMIN_USER_EMAIL_LIST + [get_cur_user_email(request.session["username"], "@goland.cn")]
                            multi_send_mail(mail_list, sub, content)
                    except Exception, e:
                        log("create virtual exception, %s" % str(e))
                    return HttpResponseRedirect("/")
    return render_to_response("create_virtual.html", locals())


@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
@csrf_exempt
def add_ip(request):
    """ 将IP添加到ip表里 """
    redirect_url = request.get_full_path()
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        try:
            IP.objects.get(name = name)
            exist_prompt = "ip: %s already exists!" % name
        except Exception as e:
            ip_obj = IP(name = name, flag = 0)
            ip_obj.save()
            return HttpResponseRedirect("/display_ip_list/")
    return render_to_response("add_ip.html", locals())


@login_required
@user_passes_test(superuser_required, login_url = "/display_user_permission/")
def display_ip_list(request):
    """ 展示ip列表 """
    redirect_url = request.get_full_path()
    ip_list = IP.objects.all()
    total_ip = len(ip_list)
    return render_to_response("display_ip_list.html", locals())


@login_required
@user_passes_test(staff_required, login_url = "/display_user_permission/")
@csrf_exempt
def update_ip(request, params = None):
    """ update ip """
    redirect_url = request.get_full_path()
    if params is None and request.method == "GET":
        params = request.GET.get("id", "").strip()
    if not params.isdigit():
        raise Http404
    
    ip_obj = IP.objects.get(id = params)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        ip_count = IP.objects.filter(name = name).exclude(id = params).count()
        if ip_count >= 1:
            exist_prompt = "ip: %s already exists!" % name
        elif all([name]):
            ip_obj.name = name
            try:
                with transaction.commit_on_success():
                    ip_obj.save()
                    save_record("%s update ip: %s" % (request.user, name))
            except Exception, e:
                log("update ip exception, %s" % str(e))
            return HttpResponseRedirect("/display_ip_list")
    return render_to_response("update_ip.html", locals())

@login_required
@user_passes_test(staff_required, login_url = "/display_user_permission/")
@csrf_exempt
def delete_ip(request, model, url, params = None):
    """ delete ip """
    if params is None and request.method == "GET":
        params = request.GET.get("id", "").strip()
    if not params.isdigit():
        raise Http404
   
    try:
    #with transaction.commit_on_success():
        model_info = model.objects.get(id = int(params))
        model_info.delete()
        save_record("%s delete ip: %s" % (request.user, model_info.name))
    except Exception, e:
        log("delete ip exception, %s" % str(e))
    return HttpResponseRedirect(url)


class Set_Excel_Style(object):
    """  设置excel的格式 """
    
    def __init__(self, height, name, bold = True, underline = True, italic = True):
        """ 初始化变量 """
        self.fnt = xlwt.Font()
        self.fnt.height = height
        self.fnt.name = name
        self.fnt.bold = bold
        self.fnt.underline = underline
        self.fnt.italic = italic
        self.style = xlwt.XFStyle()
        self.style.font = self.fnt

    def set_height(self, height):
        """ 设置高度 """
        self.fnt.height = height

    def set_bold(self, bold):
        """ 设置bold """
        self.fnt.bold = bold

    def set_name(self, name):
        """ 设置字体名字 """
        self.fnt.name = name


def set_style(height, name, bold = True, underline = True, italic = True):
    """ 设置excel的格式 """
    fnt = xlwt.Font()
    fnt.height = height
    fnt.name = name
    fnt.bold = bold
    fnt.underline = underline
    fnt.italic = italic
    style = xlwt.XFStyle()
    style.font = fnt
    return style 


def export_server_info_to_excel(request):
    """ 将数据导出到excel表格 """
    excel_file = "服务器信息.xls"
    cell_width = 5555         #单元格的宽度
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename = %s' % excel_file
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'Sheet1')
    title_list = ["操作系统", "IP", "虚拟机", "用户名", "密码", "内存", "CPU", "硬盘", "描述"]
    pc_info_list = PC_Info.objects.all()
    set_style = Set_Excel_Style(300, u"华文楷体")
    sheet.row(0).set_style(set_style.style)
    """写入标题行"""
    for title_index in xrange(len(title_list)):
        sheet.col(title_index).width = cell_width
        sheet.write(0,title_index, title_list[title_index])
    
    row = 1
    """写入每一行内容"""
    for s in pc_info_list:
        value_list = [s.platform.name, s.ip, s.is_virtual, s.username, s.password, s.memory, s.cpu, s.hard_disk, s.description]
        for index in xrange(len(value_list)):
            sheet.col(index).width = cell_width
            sheet.write(row, index, value_list[index])
        sheet.row(row).set_style(set_style.style)
        row=row + 1

    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    #response["Content-Length"] = os.path.getsize(excel_file)
    return response


def export_excel(request):
    """ 将数据导出到excel表格 """
    excel_file = "资产信息.xls"
    cell_width = 5555         #单元格的宽度
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename = %s' % excel_file
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'Sheet1')
    title_list = ["资产名称","资产编号","资产地址", "操作系统", "IP", "部门", "员工姓名", "内存", "CPU", "硬盘", "描述"]
    staff_info_list = Staff_Info.objects.all()
    #style = set_style(300, "Times New Roman") 
    set_style = Set_Excel_Style(300, u"华文楷体")
    sheet.row(0).set_style(set_style.style)
    """写入标题行"""
    for title_index in xrange(len(title_list)):
        sheet.col(title_index).width = cell_width
        sheet.write(0,title_index, title_list[title_index])
    
    row = 1
    """写入每一行内容"""
    for s in staff_info_list:
        value_list = [s.asset_name, s.serial_num, s.asset_address, s.platform.name, s.ip, s.department.name, s.staff_name, s.memory, s.cpu, s.hard_disk, s.description]
        for index in xrange(len(value_list)):
            sheet.col(index).width = cell_width
            sheet.write(row, index, value_list[index])
        sheet.row(row).set_style(set_style.style)
        row=row + 1

    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    #response["Content-Length"] = os.path.getsize(excel_file)
    return response



