from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import sqlite3
import shutil
import os
import subprocess

DB_PATH = "/Volumes/MacintoshHD/test/backup_dvdfab.db"
TB_NAME = "tdmore_information"
#AAA ="" 
def display_tdmore_information(request):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s where (flag = 0 or flag = 2) order by id desc" % TB_NAME
        cur.execute(select_sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    return render_to_response("display_tdmore_information.html", locals())


def main(request):
    return render_to_response("main.html", locals())

def display_all_tdmore_information(request, param):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s where id = '%s'" % (TB_NAME, param)
        cur.execute(select_sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    return render_to_response("display_all_tdmore_information.html", locals())


def display_all_tdmore_record(request):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s order by id desc" % TB_NAME
        cur.execute(select_sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    return render_to_response("display_tdmore_information.html", locals())

def display_all_tdmore(request):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s order by id desc" % TB_NAME
        cur.execute(select_sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    return render_to_response("display_all_tdmore.html", locals())

@csrf_exempt
def backup_tdmore(request):
    url_path = request.get_full_path()
    checkbox = request.POST.getlist('checkbox')
    num_list = request.POST.getlist("num")
    if len(checkbox) < 1:
        return render_to_response("select_tdmore_one.html", locals())
    if len(checkbox) > 1:
        return render_to_response("select_tdmore_error.html", locals())
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s where id = '%s'" % (TB_NAME, checkbox[0])
        cur.execute(select_sql)
        res = cur.fetchone()
        version_list = ["include=" + res[3],"bluray=" +res[4],"common=" + res[5],"DVDFabQxLibs=" + res[6],"mobile2=" + res[7], "backup_path=" + res[8],"package_folder_backup_path=" + res[12], "include_branch=" + res[13], "bluray_branch=" + res[14], "common_branch=" + res[15], "DVDFabQxLibs_branch=" + res[16], "mobile2_branch=" + res[17]]  
        #if res[9] == 2:
        #    return render_to_response("already_backup.html")
        #update flag to 2 which is saved
        try:
            update_sql = "update %s set description = '%s'" % (TB_NAME, "")
            cur.execute(update_sql)
            update_sql = "update %s set flag = '%s' , description = '%s' where id = '%s'" % (TB_NAME, 2, "this is the current backup", checkbox[0])
            cur.execute(update_sql)
        except Exception ,e:
            return HttpResponse("update Exception " + str(e))
            
        #update flag to 1 which is deleted
        try:
            update_del_sql = "update %s set flag = '%s' where flag = '%s'" % (TB_NAME, 1, 0)
            cur.execute(update_del_sql)
        except Exception ,e:
            return HttpResponse("update del Exception " + str(e))
        svnpath = "/opt/local/bin/svn ci"
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update from 170!"'
        backup_txt = "/Volumes/MacintoshHD/auto_package/Backup_TDMore.txt"
        fp = open(backup_txt, "w")
        for record in version_list:
            fp.write(record + "\n\r")
        fp.close()
        try:
            cmdlist = [svnpath, backup_txt, svn_param]
            cmd = " ".join(cmdlist)
            subprocess.Popen(cmd, shell=True)
        except Exception ,e:
            return HttpResponse("svn ci exception: " + str(e))
    return render_to_response("backup_tdmore.html", locals())


def backup_result(request):
    return render_to_response("backup_result.html",locals())    
