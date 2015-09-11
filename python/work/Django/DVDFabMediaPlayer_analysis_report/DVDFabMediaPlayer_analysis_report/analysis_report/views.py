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



def get_bug_name(filename):
    bug_name = ""
    if os.path.exists(filename):
        fp = open(filename, "r")
        all_lines = fp.readlines()
        fp.close()
        for each_line in all_lines:
            if each_line.strip().startswith("<font"):
                font_count = each_line.count("font")
                if font_count == 2:
                    bug_name = each_line.strip().split("</font")[0].split(">")[1]
                elif font_count == 4:
                    bug_function = each_line.strip().split("font")[1].split(">")[1].split("<")[0]
                    bug_module = each_line.strip().split("font")[3].split(">")[1].split("<")[0]
                    bug_name = bug_function + " " + bug_module
                break
    return bug_name
	
	
def display_each_day(request, param1): 
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
        
    each_day_path = os.path.join(Dump_Path, param1)

    for each_version in os.listdir(each_day_path):
        each_version_path = os.path.join(each_day_path, each_version)
        for record in os.listdir(each_version_path):
            record_path = os.path.join(each_version_path, record)
            if os.path.isdir(record_path):
                num += 1
            
    for each_version in os.listdir(each_day_path):
        id_number = 0
        bug_number = 0
        each_version_path = os.path.join(each_day_path, each_version)
        all_bug_list = []
        same_bug_list = []
        for record in os.listdir(each_version_path):
            record_path = os.path.join(each_version_path, record)
            if os.path.isdir(record_path):
                #num += 1
                #number += 1
                bug_name = get_bug_name(os.path.join(record_path,"index.htm"))
                if bug_name:
                    if bug_name in all_bug_list:
                        for each_record in each_record_list:
                            if bug_name in each_record:
                                each_record[-1].append(record)
                                each_record[-2] += 1
                    else:
                        all_bug_list.append(bug_name)
                        id_number += 1
                        count = 1
                        each_record_list.append([each_version, bug_name, id_number, "", count, [record]])
                bug_number += 1
        rate = int(round(float(bug_number)/float(num)*100))
        each_version_list.append((each_version, bug_number, rate))

        bug_rate_list = []
        for each_record in each_record_list:
            version = each_record[0]
            for each_list in each_version_list:
                if version in each_list:
                    bug_rate = int(round(float(each_record[4])/float(each_list[1])*100))
                    each_record[3] = bug_rate
        all_records_list.append(each_record_list)
    each_version_list = each_version_list[::-1]
    all_records_list = all_records_list[0]
    return render_to_response("display_each_day.html",locals())



def display_details(request, param1, param2):
    http_path = "http://10.10.2.72:9000/DVDFab_Dump/DVDFab_Media_Player"
    file_list = []
    num = request.GET.get("num","")
    cur_url = request.path
    file_path = os.path.join(Dump_Path, param1,param2,num)

    cur_url1 = cur_url[1:-1]
    if "/" in cur_url1:
        last_url = os.path.split(cur_url1)[1]
        other_url = os.path.split(cur_url1)[0]
    else:
        last_url = cur_url1
        other_url = ""
    jpg_file = ""
    for each_file in os.listdir(file_path):
        if os.path.splitext(each_file)[1].upper() == ".HTM":
            continue
        elif os.path.splitext(each_file)[1].upper() == ".JPG":
            full_jpg_file = os.path.join(file_path, each_file)
            jpg_file = each_file
        else:
            filename = os.path.join(file_path, each_file)
            file_list.append((each_file,filename))
    return render_to_response("display_details.html",locals())


