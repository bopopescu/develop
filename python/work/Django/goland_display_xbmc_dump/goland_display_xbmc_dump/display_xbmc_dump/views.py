from django.shortcuts import HttpResponse,HttpResponseRedirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from models import Dump_Info, Web_params
import ConfigParser
import os
import time
import datetime

import access_server

temp_path = os.path.expanduser("~")
PRODUCT_LIST = ["","Android Blu-ray Box AV100","Android Blu-ray Box AV200","VDMLauncher","XBMC13","XBMC14","VidonCloudTV"]

def read_ini(filename, field, key):
    cf = ConfigParser.ConfigParser()
    cf.read(filename)
    value = cf.get(field, key)
    return value


#def index(request):
#    return render_to_response("index.html",locals())


@csrf_exempt
def download_dump(request):
    product_list = PRODUCT_LIST
    web_params = Web_params.objects.all()	
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
		
    if request.method == "POST":
        result = access_server.access_server()
        product = request.POST.get("product", "").strip()
        username = request.POST.get("username", "").strip()
        useremail = request.POST.get("useremail", "").strip()
        chipid = request.POST.get("chipid", "").strip()
        #from_day = request.POST.get("from_day", "").strip()
        #to_day = request.POST.get("to_day", "").strip()
        
        from_list_time = from_day.split("-")
        #return HttpResponse(from_day)   
        if len(from_list_time[1]) == 1:
            month = "0" + from_list_time[1]
        else:
            month = from_list_time[1]
        if len(from_list_time[2]) == 1:
            day = "0" + from_list_time[2]
        else:
            day = from_list_time[2]
			
        from_day = from_list_time[0] + "-" + month + "-" + day
		
        to_list_time = to_day.split("-")
        if len(to_list_time[1]) == 1:
            month = "0" + to_list_time[1]
        else:
            month = to_list_time[1]
        if len(to_list_time[2]) == 1:
            day = "0" + to_list_time[2]
        else:
            day = to_list_time[2]
        to_day = to_list_time[0] + "-" + month + "-" + day
        if cmp(from_day, to_day) == 1:
            return render_to_response("input_date_error.html")
	  
        to_day_list = to_day.split("-")
        #return HttpResponse(to_day_list)
        t2 = datetime.datetime(int(to_day_list[0]),int(to_day_list[1]),int(to_day_list[2]))
        t3 = t2 + datetime.timedelta(days = 1)
        to_day_1 = str(t3)[:-9]
        
        if not username and not useremail and not chipid and not from_day and not to_day:
            return render_to_response("fill_in_one.html",locals())
        if from_day:
            web = Web_params(All_Record = from_day,To_Day = to_day,product = product, username = username, useremail = useremail, chipid = chipid)	
            web.save()

        if from_day:
            qs0 = Dump_Info.objects.filter(upload_time__gte = from_day)
            #qs4 = qs3.extra(where = ["upload_time like'%%" + date_time + "%%'"])
        else:
            qs0 = Dump_Info.objects.all()
        if product:
            qs = qs0.filter(software_title = product)
        else:
            qs = qs0
        if username:
            qs1 = qs.filter(username = username)
        else:
            qs1 = qs
        if useremail:
            qs2 = qs1.filter(useremail = useremail)
        else:
            qs2 = qs1
        if chipid:
            qs3 = qs2.filter(subject = chipid)
        else:
            qs3 = qs2	
        if to_day_1:
            qs4 = qs3.filter(upload_time__lte = to_day_1)
        else:
            qs4 = qs3
        count = qs4.count()
        session = qs4.order_by("-id")
  
        return render_to_response("index.html", locals())
		
    elif request.method == "GET":
        flag = 0
        param = request.GET.get("param","")
        to_day_list = to_day.split("-")
        t2 = datetime.datetime(int(to_day_list[0]),int(to_day_list[1]),int(to_day_list[2]))
        t3 = t2 + datetime.timedelta(days = 1)
        to_day_1 = str(t3)[:-9]
		#qs = Dump_Info.objects.extra(where = ["upload_time like'%%" + date_time + "%%'"])
        if from_day:
            qs0 = Dump_Info.objects.filter(upload_time__gte = from_day)
        else:
		    qs0 = Dump_Info.objects.all()
        if to_day_1:
            qs = qs0.filter(upload_time__lte = to_day_1)
        else:
            qs = qs0
			
        if product:
            qs1 = qs.filter(software_title = product)
        else:
            qs1 = qs
        if username:
            qs2 = qs1.filter(username = username)
        else:
            qs2 = qs1
        if useremail:
            qs3 = qs2.filter(useremail = useremail)
        else:
            qs3 = qs2
        if chipid:
            qs4 = qs3.filter(subject = chipid)
        else:
            qs4 = qs3
			
        count = 0
        final_count = qs4.count()
        if param == "id":
            count = final_count
            session = qs4.order_by("id")
        elif param == "version":
            count = final_count
            session = qs4.order_by("version")
        elif param == "software_title":
            count = final_count
            session = qs4.order_by("software_title")
        elif param == "filepath":
            count = final_count
            session = qs4.order_by("filepath")
        elif param == "record_type":
            count = final_count
            session = qs4.order_by("record_type")
        elif param == "username":
            count = final_count
            session = qs4.order_by("username")
        elif param == "useremail":
            count = final_count
            session = qs4.order_by("useremail")
            
        elif param == "subject":
            count = final_count
            session = qs4.order_by("subject")
        elif param == "logname1":
            count = final_count
            session = qs4.order_by("logname1")
        elif param == "logname2":
            count = final_count
            session = qs4.order_by("logname2")
        elif param == "logname3":
            count = final_count
            session = qs4.order_by("logname3")
        elif param == "logname4":
            count = final_count
            session = qs4.order_by("logname4")
        elif param == "stack_file":
            count = final_count
            session = qs4.order_by("stack_file")
        elif param == "stack_file1":
            count = final_count
            session = qs4.order_by("stack_file1")

        elif param == "filename":
            count = final_count
            session = qs4.order_by("filename")
        elif param == "status":
            count = final_count
            session = qs4.order_by("status")
        elif param == "upload_time":
            count = final_count
            session = qs4.order_by("upload_time")
        return render_to_response("index.html", locals())
    #return HttpResponseRedirect("/index/")
	
	
def write_file(filename, content):	
    fp = open(filename, "w")
    fp.write(content)
    fp.close()
	
	
def display_log_content(request,param):	
    logname = request.GET.get("logname","").strip()
    dump_info = Dump_Info.objects.get(id = param)
    filepath = dump_info.filepath
    filename = dump_info.filename
    #if filepath.endswith(".zip"):
    #    logfilename = os.path.join(os.path.splitext(filepath)[0],logname)
    #else:
    #    logfilename = os.path.join(os.path.join(filepath, os.path.splitext(filename)[0]),logname)
		
    if filepath.endswith(".zip"):
        logfilename_path = os.path.splitext(filepath)[0]
    else:
        logfilename_path = os.path.join(filepath, os.path.splitext(filename)[0])
    for roots, dirs, files in os.walk(logfilename_path):
        for onefile in files:
            if onefile == logname:
                logfilename = os.path.join(roots, onefile)
    content = []
    if os.path.exists(logfilename):
        fp = open(logfilename, "r")
        content_list = fp.readlines()
        fp.close()
        for record in content_list:
            content.append(record + "\r\n")
        length = len(content)
    return render_to_response("display_log_content.html", locals())
	
	
@csrf_exempt	
def index(request):
    product_list = PRODUCT_LIST
    cur_time = time.strftime("%Y-%m-%d")
    web_params = Web_params.objects.all()	
	
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
    param = request.GET.get("param","")
    perpage_number = request.POST.get("perpage_number", "").strip()
    if request.method == "POST":
        flag = 1
        #result = access_server.access_server()
        product = request.POST.get("product", "").strip()
        username = request.POST.get("username", "").strip()
        useremail = request.POST.get("useremail", "").strip()
        chipid = request.POST.get("chipid", "").strip()
        from_day = request.POST.get("from_day", "").strip()
        to_day = request.POST.get("to_day", "").strip()
        from_list_time = from_day.split("-")
        
        if len(from_list_time[1]) == 1:
            month = "0" + from_list_time[1]
        else:
            month = from_list_time[1]
        if len(from_list_time[2]) == 1:
            day = "0" + from_list_time[2]
        else:
            day = from_list_time[2]
			
        from_day = from_list_time[0] + "-" + month + "-" + day
		
        to_list_time = to_day.split("-")
        if len(to_list_time[1]) == 1:
            month = "0" + to_list_time[1]
        else:
            month = to_list_time[1]
        if len(to_list_time[2]) == 1:
            day = "0" + to_list_time[2]
        else:
            day = to_list_time[2]
        to_day = to_list_time[0] + "-" + month + "-" + day
        if cmp(from_day, to_day) == 1:
            return render_to_response("input_date_error.html")
		   
        to_day_list = to_day.split("-")
        #return HttpResponse(to_day_list)
        t2 = datetime.datetime(int(to_day_list[0]),int(to_day_list[1]),int(to_day_list[2]))
        t3 = t2 + datetime.timedelta(days = 1)
        to_day_1 = str(t3)[:-9]
        
        if not username and not useremail and not chipid and not from_day and not to_day:
            return render_to_response("fill_in_one.html",locals())
        if from_day:
            web = Web_params(All_Record = from_day,To_Day = to_day,product = product, username = username, useremail = useremail, chipid = chipid)	
            web.save()
        """
        if perpage_number:
            perpage_number = int(perpage_number)
            web = Web_params(All_Record = perpage_number)
            web.save()
        web_params = Web_params.objects.all()
        if web_params:
            perpage_number = int(web_params[0].All_Record)
        else:
            perpage_number = 100
        """

        if from_day:
            qs0 = Dump_Info.objects.filter(upload_time__gte = from_day)
            #qs4 = qs3.extra(where = ["upload_time like'%%" + date_time + "%%'"])
        else:
            qs0 = Dump_Info.objects.all()
        if product:
            qs = qs0.filter(software_title = product)
        else:
            qs = qs0
        if username:
            qs1 = qs.filter(username = username)
        else:
            qs1 = qs
        if useremail:
            qs2 = qs1.filter(useremail = useremail)
        else:
            qs2 = qs1
        if chipid:
            qs3 = qs2.filter(subject = chipid)
        else:
            qs3 = qs2	
        if to_day_1:
            #return HttpResponse(to_day_1)
            qs4 = qs3.filter(upload_time__lte = to_day_1)
            #qs4 = qs3.extra(where = ["upload_time like'%%" + date_time + "%%'"])
        else:
            qs4 = qs3
        count = qs4.count()

        """
        nowpage = request.GET.get("nowpage","")
        if nowpage == "":
            nowpage = 1
        else:
            nowpage = int(nowpage)
        count = qs4.count()
        #perpage_number = 10
        if count % perpage_number == 0:
            pageall = count/perpage_number
        else:
            pageall = count/perpage_number + 1
        if nowpage - 1 < 1:
            pageup = 1
        else:
            pageup = nowpage - 1
        if nowpage + 1 >= pageall:
            pagedn = pageall
        else:
            pagedn = nowpage + 1
        start = perpage_number*(nowpage - 1)
        session = qs4.order_by("-id")[start:(start + perpage_number)]
        """
        session = qs4.order_by("-id")
       
        #return render_to_response("index.html", locals())
        #if "product" in request.COOKIES:
        #    product_cookie = request.COOKIES["product"]
        #    if product == product_cookie:
        #        product = product_cookie
        #    else:
        #        product = product
        #else:
        #    product = product
        #response = render_to_response("index.html", locals())
        #response.set_cookie("product", product,360000)
        #product = request.COOKIES.get("product","")
        return render_to_response("index.html", locals())
		
    elif request.method == "GET":
        flag = 0
        to_day_list = to_day.split("-")
        t2 = datetime.datetime(int(to_day_list[0]),int(to_day_list[1]),int(to_day_list[2]))
        t3 = t2 + datetime.timedelta(days = 1)
        to_day_1 = str(t3)[:-9]
		#qs = Dump_Info.objects.extra(where = ["upload_time like'%%" + date_time + "%%'"])
        if from_day:
            qs0 = Dump_Info.objects.filter(upload_time__gte = from_day)
        else:
		    qs0 = Dump_Info.objects.all()
        if to_day_1:
            qs = qs0.filter(upload_time__lte = to_day_1)
        else:
            qs = qs0
        if product:
            qs1 = qs.filter(software_title = product)
        else:
            qs1 = qs
        if username:
            qs2 = qs1.filter(username = username)
        else:
            qs2 = qs1
        if useremail:
            qs3 = qs2.filter(useremail = useremail)
        else:
            qs3 = qs2
        if chipid:
            qs4 = qs3.filter(subject = chipid)
        else:
            qs4 = qs3
			
        count = 0
        final_count = qs4.count()
        if param == "id":
            count = final_count
            session = qs4.order_by("id")
        elif param == "version":
            count = final_count
            session = qs4.order_by("version")
        elif param == "software_title":
            count = final_count
            session = qs4.order_by("software_title")
        elif param == "filepath":
            count = final_count
            session = qs4.order_by("filepath")
        elif param == "record_type":
            count = final_count
            session = qs4.order_by("record_type")
        elif param == "username":
            count = final_count
            session = qs4.order_by("username")
        elif param == "useremail":
            count = final_count
            session = qs4.order_by("useremail")
            
        elif param == "subject":
            count = final_count
            session = qs4.order_by("subject")
        elif param == "logname1":
            count = final_count
            session = qs4.order_by("logname1")
        elif param == "logname2":
            count = final_count
            session = qs4.order_by("logname2")
        elif param == "logname3":
            count = final_count
            session = qs4.order_by("logname3")
        elif param == "logname4":
            count = final_count
            session = qs4.order_by("logname4")
        elif param == "stack_file":
            count = final_count
            session = qs4.order_by("stack_file")
        elif param == "stack_file1":
            count = final_count
            session = qs4.order_by("stack_file1")

        #elif param == "content":
        #    count = final_count
        #    session = qs.order_by("content")
        #elif param == "windows_version":
        #    count = final_count
        #    session = qs.order_by("windows_version")
        #elif param == "dvd_title":
        #    count = final_count
        #    session = qs.order_by("dvd_title")
        #elif param == "region_code":
        #    count = final_count
        #    session = qs.order_by("region_code")
        #elif param == "country":
        #    count = final_count
        #    session = qs.order_by("country")   
        #elif param == "buy_link":
        #    count = final_count
        #    session = qs.order_by("buy_link")

        elif param == "filename":
            count = final_count
            session = qs4.order_by("filename")
        elif param == "status":
            count = final_count
            session = qs4.order_by("status")
        elif param == "upload_time":
            count = final_count
            session = qs4.order_by("upload_time")
        return render_to_response("index.html", locals())
		
    else:
        return render_to_response("index.html", locals())
                        
def one_record(request, param):
    dump_info = Dump_Info.objects.get(id = param)
    return render_to_response("one_record.html", locals())				
