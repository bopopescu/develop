from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import sqlite3
import shutil
import os
import subprocess

DB_PATH = "/Volumes/MacintoshHD/test/backup_dvdfab.db"
TB_NAME = "safedvdcopy_information"

def display_safedvdcopy_information(request):
    platform_name = request.GET.get("platform_name","").strip()
    if not platform_name:
        platform_name = "Win"
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s where (flag = 0 or flag = 2) and platform = '%s' order by id desc" % (TB_NAME, platform_name)
        #select_sql = "select * from %s" % TB_NAME
        cur.execute(select_sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    return render_to_response("display_safedvdcopy_information.html", locals())


def main(request):
    return render_to_response("main.html", locals())

def display_all_safedvdcopy_information(request, param):
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
    return render_to_response("display_all_safedvdcopy_information.html", locals())


def display_all_safedvdcopy_record(request):
    platform_name = request.GET.get("platform_name","").strip()
    if not platform_name:
        platform_name = "Win"
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.isolation_level = None
        cur = conn.cursor()    
    except Exception, e:
        return HttpResponse("Exception " + str(e))
    else:
        select_sql = "select * from %s where platform = '%s' order by id desc" % (TB_NAME, platform_name)
        cur.execute(select_sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    return render_to_response("display_safedvdcopy_information.html", locals())

def display_all_safedvdcopy(request):
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
    return render_to_response("display_all_safedvdcopy.html", locals())

@csrf_exempt
def backup_safedvdcopy(request):
    url_path = request.get_full_path()
    checkbox = request.POST.getlist('checkbox')
    platform_name = request.POST.get("platform_name", "")
    num_list = request.POST.getlist("num")
    if len(checkbox) < 1:
        return render_to_response("select_safedvdcopy_one.html", locals())
    if len(checkbox) > 1:
        return render_to_response("select_safedvdcopy_error.html", locals())
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
            update_sql = "update %s set description = '%s' where platform= '%s'" % (TB_NAME, "", res[11])
            cur.execute(update_sql)
            update_sql = "update %s set flag = '%s' , description = '%s' where id = '%s' and platform = '%s'" % (TB_NAME, 2, "this is the current backup", checkbox[0], res[11])
            cur.execute(update_sql)
        except Exception ,e:
            return HttpResponse("update Exception " + str(e))
            
        #update flag to 1 which is deleted
        try:
            update_del_sql = "update %s set flag = '%s' where flag = '%s' and platform = '%s'" % (TB_NAME, 1, 0, res[11])
            cur.execute(update_del_sql)
        except Exception ,e:
            return HttpResponse("update del Exception " + str(e))
        svnpath = "/opt/local/bin/svn ci"
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update from 170!"'
        if res[11].upper() == "WIN":
            backup_txt = "/Volumes/MacintoshHD/auto_package/Backup_Win_SafeDVDCopy.txt"
            fp = open(backup_txt, "w")
            for record in version_list:
                fp.write(record + "\n\r")
            fp.close()
        elif res[11].upper() == "MAC":
            backup_txt = "/Volumes/MacintoshHD/auto_package/Backup_Mac_SafeDVDCopy.txt"
            fp = open(backup_txt, "w")
            for record in version_list:
                fp.write(record + "\n\r")
            #fp.write(res[8])
            fp.close()
        try:
            cmdlist = [svnpath, backup_txt, svn_param]
            cmd = " ".join(cmdlist)
            subprocess.Popen(cmd, shell=True)
        except Exception ,e:
            return HttpResponse("svn ci exception: " + str(e))
    return render_to_response("backup_safedvdcopy.html", locals())


def backup_result(request):
    return render_to_response("backup_result.html",locals())    
