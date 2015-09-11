from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import sqlite3
import shutil
import os
import subprocess

#NAS_DB_PATH = "/Volumes/nas/other/users/xudedong/backup_dvdfab.db"
DB_PATH = "/Volumes/MacintoshHD/test/backup_dvdfab.db"
TB_NAME = "vdmserver_information"
#AAA ="" 

def display_vdmserver_information(request):
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
    return render_to_response("display_vdmserver_information.html", locals())


def main(request):
    return render_to_response("main.html", locals())

def display_all_vdmserver_information(request, param):
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
    return render_to_response("display_all_vdmserver_information.html", locals())


def display_all_vdmserver_record(request):
    #platform_name = request.GET.get("platform_name","").strip()
    #if not platform_name:
    #    platform_name = "Win"
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
    return render_to_response("display_vdmserver_information.html", locals())


def display_all_vdmserver(request):
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
    return render_to_response("display_all_vdmserver.html", locals())

@csrf_exempt
def backup_vdmserver(request):
    url_path = request.get_full_path()
    checkbox = request.POST.getlist('checkbox')
    #platform_name = request.POST.get("platform_name", "")
    num_list = request.POST.getlist("num")
    if len(checkbox) < 1:
        return render_to_response("select_vdmserver_one.html", locals())
    if len(checkbox) > 1:
        return render_to_response("select_vdmserver_error.html", locals())
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
        version_list = ["bootingserver_version=" + res[2],"relayserver_version=" +res[3],"server_version=" + res[4],"transcode_version=" + res[5],"vidonbase_version=" + res[6], "vidonfs_version=" + res[7],"vidonpeer_version=" + res[8], "bootingserver_branch=" + res[9], "relayserver_branch=" + res[10], "server_branch=" + res[11], "transcode_branch=" + res[12], "vidonbase_branch=" + res[13], "vidonfs_branch=" + res[14], "vidonpeer_branch=" + res[15], "source_code_backup_path=" + res[17], "package_folder_backup_path=" + res[18]]  
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
        
        backup_txt = "/Volumes/MacintoshHD/VDMServer2_auto_package/Backup_VDMServer2.txt"
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
    return render_to_response("backup_vdmserver.html", locals())


def backup_result(request):
    return render_to_response("backup_result.html",locals())    
