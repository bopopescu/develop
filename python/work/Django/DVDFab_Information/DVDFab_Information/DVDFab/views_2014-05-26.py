from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import time
import os
import sys
import shutil
import logging
import subprocess

filename = '/Users/DVDFab/name.txt'
#filename = "C:\\Apache2.2\\name.txt"
LOGPATH = "/Users/DVDFab/log"
LOGNAME = "log.txt"

default_encoding = 'utf-8'
if sys.getdefaultencoding()!=default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    

def log(info):
    logging.basicConfig(filename = LOGPATH + '/' + LOGNAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 

def svn_up(filename):
    svnup_cmdline = "/opt/local/bin/svn up --accept theirs-full "
    #svnup_cmdline = "svn up --accept theirs-full "
    svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
    svnup_cmdlist = [svnup_cmdline, filename,svnup_params]
    cmdline = " ".join(svnup_cmdlist)
    #log("cmdline is:  "+ cmdline)
    try:
        for i in xrange(20):
        #while 1:
            process = subprocess.Popen(cmdline, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            if process.poll() is None:
                time.sleep(0.5)
                log("does not finish")
                pass
            else:
                break
        #time.sleep(5)
        log("No Exception")
    except Exception,e:
        log("Exception " + str(e))
    content = process.stdout.read().decode("utf-8").encode("gb2312")
    error_content = process.stderr.read().decode("utf-8").encode("gb2312")
    log("stdout  " + str(content))
    log("stderr  " + str(error_content))
    
    #subprocess.call("mkdir /Users/DVDFab/log/123", shell=True)
    #subprocess.call('echo "user"|sudo -S chown _www: ' + filename, shell=True)
    #returncode = subprocess.call("chmod 777 " + filename, shell=True)
    #log("1111111111111111111" +filename)
    #log("returncode is :" + str(returncode))

@csrf_exempt    
def index(request):
    flag = ""
    all_name_list = []
    name_list = []
    if os.path.exists(filename):
        fp = open(filename, 'r')
        content = fp.read()
        fp.close()
        for onename in content.split(','):
            all_name_list.append(onename.strip())
        #name_list = [i for i in set(name_list)]
        for record in all_name_list:
            if record and record not in name_list:
                name_list.append(record)
    current_date=time.strftime('%d/%m/%Y')
    name = request.POST.get('name', '').strip()
    date = request.POST.get('date', '').strip()
    version = request.POST.get('version', '').strip()
    type_name = request.POST.get('type_name', '').strip()
    changelog = request.POST.get('changelog', '').strip()
    
    #DVDFab 8 version
    readme_file = "D:\\Develop\\trunk\\official\\DVDFab_alpha\\V8_Qt\\Readme.txt"
    if os.path.exists(readme_file):
        fp = open(readme_file, "r")
        content_lines = fp.readlines()
        fp.close()
        DVDFab_8_version = content_lines[1].strip().split(" ")[1].replace(".", "")
    else:
        DVDFabb_8_version = ""

    #BluFab 9  Official version
    product_blufab_txt= "/Volumes/X/Develop/Runtime_mobile2/product_blufab.txt"
    if os.path.exists(product_blufab_txt):
        fp = open(product_blufab_txt, "r")
        content = fp.read()
        fp.close()
        BluFab_9_Official_version = content.split("|")[0]
    else:
        BluFab_9Official_version = ""

    #BluFab 9 Beta version
    #product_blufab_txt= "/Volumes/X/Develop/Runtime_mobile2/product_blufab.txt"
    product_blufab_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab.txt"
    if os.path.exists(product_blufab_txt):
        fp = open(product_blufab_txt, "r")
        content = fp.read()
        fp.close()
        BluFab_9_Beta_version = content.split("|")[0]
    else:
        BluFab_9_Beta_version = ""

    #DVDFab 9  Official version
    product_dvdfab_txt= "/Volumes/X/Develop/Runtime_mobile2/product_dvdfab.txt"
    if os.path.exists(product_dvdfab_txt):
        fp = open(product_dvdfab_txt, "r")
        content = fp.read()
        fp.close()
        DVDFab_9_Official_version = content.split("|")[0]
    else:
        DVDFab_9_Official_version = ""

    #DVDFab 9 Beta version
    product_dvdfab_txt= "/Volumes/X/Develop/Runtime_mobile2/product_dvdfab.txt"
    #product_dvdfab_txt= "/Users/DVDFab/Runtime_mobile2/product_dvdfab.txt"
    if os.path.exists(product_dvdfab_txt):
        fp = open(product_dvdfab_txt, "r")
        content = fp.read()
        fp.close()
        DVDFab_9_Beta_version = content.split("|")[0]
    else:
        DVDFab_9_Beta_version = ""

    #DVDFab Retail version
    readme_file = "D:\\Develop\\trunk\\official\\DVDFab_9_mobile2_Official\\Retail_Japan\\V9_Qt\\Readme.txt"
    if os.path.exists(readme_file):
        fp = open(readme_file, "r")
        content_lines = fp.readlines()
        fp.close()
        DVDFab_Retail_version = content_lines[1].strip().split(" ")[1].replace(".", "")
    else:
        DVDFab_Retail_version = ""

    #DVDFabNonDecAll version
    product_dvdfabnondec_txt= "/Volumes/X/Develop/Runtime_mobile2/product_dvdfabnondec.txt"
    if os.path.exists(product_dvdfabnondec_txt):
        fp = open(product_dvdfabnondec_txt, "r")
        content = fp.read()
        fp.close()
        DVDFabNonDecAll_version = content.split("|")[0]
    else:
        DVDFabNonDecAll_version = ""

    #DVDFabNonDecAll German version
    product_dvdfabnondecde_txt= "/Volumes/X/Develop/Runtime_mobile2/product_dvdfabnondecde.txt"
    if os.path.exists(product_dvdfabnondecde_txt):
        fp = open(product_dvdfabnondecde_txt, "r")
        content = fp.read()
        fp.close()
        DVDFabNonDecAll_German_version = content.split("|")[0]
    else:
        DVDFabNonDecAll_German_version = ""

    

    #for DVDFab 8
    if (name.upper() == "DVDFAB 8" or name.upper() == "DVDFAB8") and date and version and changelog:
        return HttpResponse("do not use it!")
        update_update_iss_py = "D:\\Develop\\trunk\official\\DVDFab_alpha\\update_update_iss.py"
        update_iss_py = "D:\\Develop\\trunk\official\\DVDFab_alpha\\update_iss.py"
        changelog_name = "D:\\Develop\\trunk\official\\DVDFab_alpha\\V8_Qt\\Changes.txt"
        temp_file = "D:\\Develop\\trunk\official\\DVDFab_alpha\\V8_Qt\\temp_file.txt"
        type_name = 'official'
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            if "." in version:
                VERSION = version
            else:
                VERSION1 = ''
                for record in version:
                    record = "." + record
                    VERSION1 += record
                    VERSION = VERSION1[1:]
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            for i in content_list:
                if i == content_list[0]:
                    i = content_list[0] + "\n" + "_" * 23 + "\n" + dict[mon] + " " + day + "," + " " + year + "\nDVDFab " + VERSION + " Qt Updated!\n\n" + changelog + "\n"
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)
        os.system("python " + update_update_iss_py + " " + version.replace(".", "") + " " + date + " " + type_name)
        os.system("python " + update_iss_py)
        #return HttpResponseRedirect("/index/")
        return render_to_response("success.html")   
    
    #for DVDFab 9 Official
    if (name.upper() == "DVDFAB 9 OFFICIAL" or name.upper() == "DVDFAB9 OFFICIAL") and date and version and changelog:
        svn_up(product_dvdfab_txt)
        #svnup_cmdline = "svn up  "
        #svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
        #svnup_cmdlist = [svnup_cmdline, product_dvdfab_txt,svnup_params]
        #cmdline = " ".join(cmdlist)
        #subprocess.call(cmdline, stdout=subprocess.PIPE, shell=True)
        
        type_name = "official"
        if version.count(".") == 3:
            final_version = version
        elif 0 < version.count(".") < 3 or version.count(".") > 3:
            return render_to_response("error.html")
            return HttpResponse("version format error")
        elif version.count(".") == 0:
            temp_version = ""
            for record in version:
                record += "."
                temp_version += record
            final_version = temp_version[:-1]
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_dvdfab_txt, "w")
        fp.write(content)
        fp.close()

        changelog_name = "/Volumes/X/Develop/V9_Qt/Changes.txt"
        temp_file = "/Volumes/X/Develop/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            if changelog in contents:
                flag = "xudedong"
                return render_to_response("index.html", locals())
                #return HttpResponseRedirect("/index/")
            else:
                day = date.split('/')[0]
                mon = date.split('/')[1]
                year = date.split('/')[2]
                fp = open(changelog_name, 'r')
                content_list = fp.readlines()
                fp.close()
                fp = open(temp_file, "w")
                for i in content_list:
                    if i == content_list[0]:
                        i = content_list[0] + "\n" + "_" * 23 + "\n" + dict[mon] + " " + day + "," + " " + year + "\nDVDFab " + final_version + " Updated!\n\n" + changelog + "\n"
                    fp.write(i)
                fp.close()
                if os.path.exists(changelog_name):
                    os.remove(changelog_name)
                if os.path.exists(temp_file):
                    os.rename(temp_file, changelog_name)
        else:
            flag = 1
            return
        svnpath = "svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab Changelog, iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfab_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html")
    
    #for DVDFab 9 Beta
    if (name.upper() == "DVDFAB 9 BETA" or name.upper() == "DVDFAB9 BETA") and date and version:
        svn_up(product_dvdfab_txt)
        #svnup_cmdline = "svn up  "
        #svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
        #svnup_cmdlist = [svnup_cmdline, product_dvdfab_txt,svnup_params]
        #cmdline = " ".join(cmdlist)
        #subprocess.call(cmdline, stdout=subprocess.PIPE, shell=True)
        
        type_name = "beta"
        if version.count(".") == 3:
            final_version = version
        elif 0 < version.count(".") < 3 or version.count(".") > 3:
            return render_to_response("error.html")
            return HttpResponse("version format error")
        elif version.count(".") == 0:
            temp_version = ""
            for record in version:
                record += "."
                temp_version += record
            final_version = temp_version[:-1]
        return render_to_response("success.html")
        
        content = final_version + "|" + type_name + "|" + date
        #subprocess.call("sudo chown _www: " + product_dvdfab_txt, shell=True)
        #log("sudo chown _www: " + product_dvdfab_txt)
        fp = open(product_dvdfab_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        #svnpath = "svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab iss file date and version from 170"'
        cmdlist = [svnpath, product_dvdfab_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html")


    #for BluFab 9 Official
    if (name.upper() == "BLUFAB 9 OFFICIAL" or name.upper() == "BluFAB9 OFFICIAL") and date and version and changelog:
        svn_up(product_blufab_txt)
        #svnup_cmdline = "svn up  "
        #svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
        #svnup_cmdlist = [svnup_cmdline, product_blufab_txt,svnup_params]
        #cmdline = " ".join(cmdlist)
        #subprocess.call(cmdline, stdout=subprocess.PIPE, shell=True)
        
        type_name = "official"
        if version.count(".") == 3:
            final_version = version
        elif 0 < version.count(".") < 3 or version.count(".") > 3:
            return render_to_response("error.html")
            return HttpResponse("version format error")
        elif version.count(".") == 0:
            temp_version = ""
            for record in version:
                record += "."
                temp_version += record
            final_version = temp_version[:-1]
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_blufab_txt, "w")
        fp.write(content)
        fp.close()

        changelog_name = "/Volumes/X/Develop/V9_Qt/Changes_BluFab.txt"
        temp_file = "/Volumes/X/Develop/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            if changelog in contents:
                flag = "xudedong"
                return render_to_response("index.html", locals())
                #return HttpResponseRedirect("/index/")
            else:
                day = date.split('/')[0]
                mon = date.split('/')[1]
                year = date.split('/')[2]
                fp = open(changelog_name, 'r')
                content_list = fp.readlines()
                fp.close()
                fp = open(temp_file, "w")
                for i in content_list:
                    if i == content_list[0]:
                        i = content_list[0] + "\n" + "_" * 23 + "\n" + dict[mon] + " " + day + "," + " " + year + "\nBluFab " + final_version + " Updated!\n\n" + changelog + "\n"
                    fp.write(i)
                fp.close()
                if os.path.exists(changelog_name):
                    os.remove(changelog_name)
                if os.path.exists(temp_file):
                    os.rename(temp_file, changelog_name)
        else:
            flag = 1
            return
        svnpath = "svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update BluFab Changelog, iss file date and version from 170!"'
        cmdlist = [svnpath, product_blufab_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html")


    #for BluFab 9 Beta
    if (name.upper() == "BLUFAB 9 BETA" or name.upper() == "BLUFAB9 BETA") and date and version:
        svn_up(product_blufab_txt)
        #svnup_cmdline = "svn up  "
        #svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
        #svnup_cmdlist = [svnup_cmdline, product_blufab_txt,svnup_params]
        #cmdline = " ".join(cmdlist)
        #subprocess.call(cmdline, stdout=subprocess.PIPE, shell=True)
        
        type_name = "beta"
        if version.count(".") == 3:
            final_version = version
        elif 0 < version.count(".") < 3 or version.count(".") > 3:
            return render_to_response("error.html")
            return HttpResponse("version format error")
        elif version.count(".") == 0:
            temp_version = ""
            for record in version:
                record += "."
                temp_version += record
            final_version = temp_version[:-1]
        
        content = final_version + "|" + type_name + "|" + date
        os.system("sudo chmod 777 /Users/DVDFab/Desktop/product_blufab.txt")
        fp = open(product_blufab_txt, "w")
        fp.write(content)
        fp.close()
        
        #svnpath = "svn ci  "
        svnpath = '/opt/local/bin/svn ci  '
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update BluFab iss file date and version from 170!"'
        cmdlist = [svnpath, product_blufab_txt, svn_param]
        cmd = "  ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #p = subprocess.Popen("/opt/local/bin/svn info /Volumes/X/Develop/Runtime_mobile2", stdout=subprocess.PIPE, shell=True)
        log("svn ci output:" +  p.stdout.read())
        log("svn ci output error:" +  p.stderr.read())
        log("-------------------------------------------\n")
        while 1:
            if p.poll() is None:
                time.sleep(1)
            else:
                return HttpResponse("1111111111")
        return render_to_response("success.html")

    #for DVDFab Retail
    if (name.upper() == "DVDFAB RETAIL" or name.upper() == "DVDFABRETAIL") and date and version:
        update_update_iss_py = "D:\\Develop\\trunk\\official\\DVDFab_9_mobile2_Official\\Retail_Japan\\update_update_iss.py"
        update_iss_py = "D:\\Develop\\trunk\\official\\DVDFab_9_mobile2_Official\\Retail_Japan\\update_iss.py"
        type_name = "official"
        os.system("python " + update_update_iss_py + " " + version.replace(".", "") + " " + date + " " + type_name)
        os.system("python " + update_iss_py)
        #return HttpResponseRedirect("/index/")
        return render_to_response("success.html")


    #for DVDFabNonDecAll
    if (name.upper() == "DVDFABNONDECALL" or name.upper() == "DVDFAB NONDECALL") and date and version:
        svn_up(product_dvdfabnondec_txt)
        #svnup_cmdline = "svn up  "
        #svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
        #svnup_cmdlist = [svnup_cmdline, product_dvdfabnondec_txt,svnup_params]
        #cmdline = " ".join(cmdlist)
        #subprocess.call(cmdline, stdout=subprocess.PIPE, shell=True)
        
        type_name = "official"
        if version.count(".") == 3:
            final_version = version
        elif 0 < version.count(".") < 3 or version.count(".") > 3:
            return render_to_response("error.html")
            return HttpResponse("version format error")
        elif version.count(".") == 0:
            temp_version = ""
            for record in version:
                record += "."
                temp_version += record
            final_version = temp_version[:-1]
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_dvdfabnondec_txt, "w")
        fp.write(content)
        fp.close()
        svnpath = "svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabNonDecAll iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfabnondec_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html")

    #for DVDFabNonDecAll German
    if (name.upper() == "DVDFABNONDECALL GERMAN" or name.upper() == "DVDFAB NONDECALL GERMAN") and date and version:
        svn_up(product_dvdfabnondecde_txt)
        #svnup_cmdline = "svn up  "
        #svnup_params = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert'
        #svnup_cmdlist = [svnup_cmdline, product_dvdfabnondecde_txt,svnup_params]
        #cmdline = " ".join(cmdlist)
        #subprocess.call(cmdline, stdout=subprocess.PIPE, shell=True)
        
        type_name = "official"
        if version.count(".") == 3:
            final_version = version
        elif 0 < version.count(".") < 3 or version.count(".") > 3:
            return render_to_response("error.html")
            return HttpResponse("version format error")
        elif version.count(".") == 0:
            temp_version = ""
            for record in version:
                record += "."
                temp_version += record
            final_version = temp_version[:-1]
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_dvdfabnondecde_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabNonDecAll German iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfabnondecde_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html")
    
    #for VDM Server
    #if (name.upper() == "VDM SERVER" or name.upper() == "VDMSERVER") and date and version:
    if (name.upper() == "VDM SERVER" or name.upper() == "VDMSERVER") and version:
        update_iss_py = "D:\\Develop\\trunk\\official\\VDM_Media_Center\\update_iss.py"
        vdmserver_iss = "D:\\Develop\\trunk\\official\\VDM_Media_Center\\VDM_server.iss"
        nas_path = r"\\10.10.2.59\nas3_nas3_Volume5\User\xudedong"
        if type_name == "":
            type_name = "official"
        os.system("python " + update_iss_py + " " + version + " " + type_name)
        
        log("-------------start to call svn-------------")
        svnpath = "svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update date and version from 50!"'
        cmdlist = [svnpath, vdmserver_iss,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        process_name = "svn.exe"
        process=os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name) 
        returncode = process.read().count(process_name)
        if returncode:
            log("svn exists")
        else:
            log("svn does not exist")
        log("here: " + p.stdout.read() + "  end!!")
        content = p.stdout.readlines()
        log(cmd)
        log(content)
        log("-------------------end-------------------\n\n")
        return render_to_response("success.html")
        
    return render_to_response('index.html', locals(),context_instance = RequestContext(request))


@csrf_exempt
def add_name(request):
    name = request.POST.get('name','').strip()
    if name:
        content = ''
        if os.path.exists(filename):
            fp = open(filename, 'r')
            content = fp.read()
            fp.close()
        fp = open(filename, 'a')
        if content:
            fp.write(','+name)
        else:
            fp.write(name)
        fp.close()
        return HttpResponseRedirect('/index/')
    return render_to_response('add_name.html', locals())

