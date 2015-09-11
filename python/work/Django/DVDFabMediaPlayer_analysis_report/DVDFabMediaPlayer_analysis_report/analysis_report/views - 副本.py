from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import os

Dump_Path = r"F:\DVDFab_Dump\DVDFab_Media_Player"


def index(request):
    cur_url = request.path
    cur_url1 = cur_url
    each_dir_list = []
    for each_dir in os.listdir(Dump_Path):
        each_dir_path = os.path.join(Dump_Path, each_dir)
        num = 0
        zipfile_list = []
        for roots, dirs, files in os.walk(each_dir_path):
            for each_file in files:
                if os.path.splitext(each_file)[1].upper() == ".ZIP":
                    zipfile_list.append(each_file)
                    num += 1
        each_dir_list.append((each_dir, num))
    each_dir_list = each_dir_list[::-1]
    return render_to_response("index.html", locals())
	
	
def display_each_day(request, param1):
    number = 0
    num = 0
    each_version_list = []
    each_record_list = []
    all_records_list = []
    cur_url = request.path
    cur_url1 = cur_url[1:-1]
    if "/" in cur_url1:
        last_url = os.path.split(cur_url1)[1]
        other_url = os.path.split(cur_url1)[0]
    else:
        last_url = cur_url1
        other_url = ""

    for roots, dirs, files in os.walk(os.path.join(Dump_Path, param1)):
        for each_file in files:
            if os.path.splitext(each_file)[1].upper() == ".ZIP":
                num += 1
                
    each_day_path = os.path.join(Dump_Path, cur_url1)
    version_list = os.listdir(each_day_path)
    for each_version in os.listdir(each_day_path):
        each_version_path = os.path.join(each_day_path, each_version)
        number = 0
        for roots, dirs, files in os.walk(each_version_path):
            for each_file in files:
                if os.path.splitext(each_file)[1].upper() == ".ZIP":
                    number += 1
                    each_record_list.append((each_version,each_file, number,1,os.path.splitext(each_file)[0]))
        if num == "":
            rate = 0
        else:
            rate = int(round(float(number)/float(num)*100))
        each_version_list.append((each_version, number, rate))
        all_records_list.append(each_record_list)
    each_version_list = each_version_list[::-1]
    a = len(all_records_list)
    all_records_list = all_records_list[0]
    return render_to_response("display_each_day.html",locals())


def display_details(request, param1,param2):
    cur_url = request.path
    cur_url1 = cur_url[1:-1]
    if "/" in cur_url1:
        last_url = os.path.split(cur_url1)[1]
        other_url = os.path.split(cur_url1)[0]
    else:
        last_url = cur_url1
        other_url = ""
    return render_to_response("display_details.html",locals())


