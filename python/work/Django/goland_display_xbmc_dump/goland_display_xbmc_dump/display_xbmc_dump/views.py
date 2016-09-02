#-*- encoding:utf-8 -*-

from django.shortcuts import HttpResponse,HttpResponseRedirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from models import Dump_Info, Web_params
import ConfigParser
import os
import time
import datetime
import codecs
import re

import access_server

temp_path = os.path.expanduser("~")
PRODUCT_LIST = ["","Android Blu-ray Box AV100","Android Blu-ray Box AV200","VDMLauncher","XBMC13","XBMC14","VidonCloudTV","VidonWinCloudTV","VidonIOSCloud","VidonAndroidCloud","VidOn Server"]

def read_ini(filename, field, key):
    cf = ConfigParser.ConfigParser()
    cf.read(filename)
    value = cf.get(field, key)
    return value
	
	
def format_date_time(src_date):
    p = r"(\d+)-(\d+)-(\d+)"
    reg_com = re.compile(p)
    res = reg_com.search(src_date)
    if res:
        year, mon, day = res.group(1), res.group(2), res.group(3)
    else:
        year, mon, day = "","",""
    mon = "0%s" % mon if len(mon) == 1 else mon
    day = "0%s" % day if len(day) == 1 else day
    format_date = "%s-%s-%s" % (year, mon, day)
    return format_date

@csrf_exempt
def download_dump(request):
    product_list = PRODUCT_LIST
    web_params = Web_params.objects.all()	
    count = 0
    falg = 0
    if web_params:
        from_day = web_params[0].All_Record
        to_day = web_params[0].To_Day
        product = web_params[0].product
        username = web_params[0].username
        useremail = web_params[0].useremail
        chipid = web_params[0].chipid
    else:
        from_day = cur_time
        to_day = cur_time
    result = access_server.access_server()
    if not product and not username and not useremail and not chipid and not from_day and not to_day:
        return render_to_response("index.html",locals())
    if product and from_day and to_day:
        flag = 1
        from_day = format_date_time(from_day)
        to_day = format_date_time(to_day)
        #if cmp(from_day, to_day) == 1:
        #    return render_to_response("input_date_error.html")
        to_day_list = to_day.split("-")
        t2 = datetime.datetime(int(to_day_list[0]),int(to_day_list[1]),int(to_day_list[2]))
        t3 = t2 + datetime.timedelta(days = 1)
        to_day_1 = str(t3)[:-9]
        if from_day:
            web = Web_params(All_Record = from_day,To_Day = to_day,product = product, username = username, useremail = useremail, chipid = chipid)	
            web.save()
        qs0 = Dump_Info.objects.filter(upload_time__gte = from_day) if from_day else Dump_Info.objects.all()
        qs = qs0.filter(software_title = product) if product else qs0
        qs1 = qs.filter(username = username) if username else qs
        qs2 = qs1.filter(useremail = useremail) if useremail else qs1
        qs3 = qs2.filter(subject = chipid) if chipid else qs2
        qs4 = qs3.filter(upload_time__lte = to_day_1) if to_day_1 else qs3
        count = qs4.count()
        session = qs4.order_by("-id")
        page, paginator, page_range, session = fenye(request, session)
        empty_prompt = "Sorry, but there are no any results for your search!"
    return render_to_response("index.html", locals())
	
	
def write_file(filename, content):	
    fp = open(filename, "w")
    fp.write(content)
    fp.close()
	
	
def read_file_lines(filename):	
    fp = open(filename, "r")
    all_lines = fp.readlines()
    fp.close()
    return all_lines
	
	
def get_filename(file_path):
    logfilename = ""
    for roots, dirs, files in os.walk(file_path):
        for onefile in files:
            if onefile == logname:
                logfilename = os.path.join(roots, onefile)
                break
    return logfilename
	
	
def display_log_content(request,param):	
    logname = request.GET.get("logname","").strip()
    dump_info = Dump_Info.objects.get(id = param)
    filepath, filename = dump_info.filepath, dump_info.filename
    #filename = dump_info.filename
    if filepath.endswith(".zip"):
        logfilename_path = os.path.splitext(filepath)[0]
    else:
        logfilename_path = os.path.join(filepath, os.path.splitext(filename)[0])
    logfilename = get_filename(logfilename_path)    
    if os.path.exists(logfilename):
        #fp = codecs.open(logfilename, "r", "utf-8")
        all_lines = read_file_lines(logfilename)
        length = len(all_lines)
    return render_to_response("display_log_content.html", locals())
	
	
@csrf_exempt	
def index(request):
    product_list = PRODUCT_LIST
    param = request.GET.get("param","")
    flag = 0
    count = 0
    if request.method == "GET":
        product = request.GET.get("product", "").strip()
        username = request.GET.get("username", "").strip()
        useremail = request.GET.get("useremail", "").strip()
        chipid = request.GET.get("chipid", "").strip()
        from_day = request.GET.get("from_day", "").strip()
        to_day = request.GET.get("to_day", "").strip()
        if not product and not username and not useremail and not chipid and not from_day and not to_day:
            return render_to_response("index.html",locals())
        if product and from_day and to_day:
            flag = 1
            from_day = format_date_time(from_day)
            to_day = format_date_time(to_day)
            if cmp(from_day, to_day) == 1:
                return render_to_response("input_date_error.html")
		   
            to_day_list = to_day.split("-")
            t2 = datetime.datetime(int(to_day_list[0]),int(to_day_list[1]),int(to_day_list[2]))
            t3 = t2 + datetime.timedelta(days = 1)
            to_day_1 = str(t3)[:-9]
            if from_day:
                web = Web_params(All_Record = from_day,To_Day = to_day,product = product, username = username, useremail = useremail, chipid = chipid)	
                web.save()
            qs0 = Dump_Info.objects.filter(upload_time__gte = from_day) if from_day else Dump_Info.objects.all()
            qs = qs0.filter(software_title = product) if product else qs0
            qs1 = qs.filter(username = username) if username else qs
            qs2 = qs1.filter(useremail = useremail) if useremail else qs1
            qs3 = qs2.filter(subject = chipid) if chipid else qs2
            qs4 = qs3.filter(upload_time__lte = to_day_1) if to_day_1 else qs3
            count = qs4.count()
            session = qs4.order_by("-id")
            page, paginator, page_range, session = fenye(request, session)
            empty_prompt = "Sorry, but there are no any results for your search!"
    return render_to_response("index.html", locals())

	
def fenye(request, result_record):
    #使用分页类显示分页
    after_range_num = 5
    before_range_num = 4
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    paginator = Paginator(result_record, 100)
	
	#跳转至请求页面，如果该页面不存在或者超过则跳转至尾页
    try:
        each_page_record = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAninteger):
        page = paginator.num_pages
        each_page_record = paginator.page(page)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num: page + before_range_num]
    else:
        page_range = paginator.page_range[0: page + before_range_num]
    return page, paginator, page_range, each_page_record
		
def one_record(request, param):
    dump_info = Dump_Info.objects.get(id = param)
    return render_to_response("one_record.html", locals())				
