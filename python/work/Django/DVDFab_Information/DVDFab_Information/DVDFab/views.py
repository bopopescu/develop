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
import ConfigParser
filename = r'/home/goland/name.txt'
LOGPATH = r"/home/goland/log"
LOGNAME = "dvdfab.log"
GIT_LOCAL_PATH = r"/home/goland/dvdfab_build"
CONFFILE_PATH = r"/home/goland/dvdfab_build/products"


projects_path = []
default_encoding = 'utf-8'
if sys.getdefaultencoding()!=default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    
def log(info):
    logging.basicConfig(filename = LOGPATH + '/' + LOGNAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 

def git_pull(filename, cur_path):
    subprocess.call("git pull " + filename, cwd = cur_path, shell = True)
    
def svn_uppath(path):
    cmd = "svn up --accept theirs-full "
    params = " --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert"
    cmdline = " ".join([cmd, path, params])
    subprocess.call(cmdline, shell=True)
	
def write_file(filename, content):
    try:
        fp = open(filename, "w")
        fp.write(content + os.linesep)
        fp.close()
    except Exception, e:
        log("write file exception: %s" % str(e))

def write_files(filename, content):
    try:
        fp = open(filename, "a+")
        fp.write(content + os.linesep)
        fp.close()
    except Exception, e:
        log("write files exception: %s" % str(e))

def read_file(filename):
    try:
        fp = open(filename, "r")
        content = fp.read().strip()
        fp.close()
    except Exception, e:
        content = ""
        log("read file exception: %s" % str(e))
    return content

def read_file_lines(filename):
    try:
        fp = open(filename, "r")
        all_lines = fp.readlines()
        fp.close()
    except Exception, e:
        all_lines = []
        log("read file lines exception: %s" % str(e))
    return all_lines
	
def get_all_branches(projects_path):
    all_branches_list = []
    return all_branches_list


def get_version(filename):
    current_date=time.strftime('%d/%m/%Y')
    content = read_file(filename)
    if content:
        version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        version = ""
        product_date = current_date
    return version, product_date


def run_cmd(cmd, filepath):
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, cwd = filepath, shell = True)	
    stdout = p.stdout.read()
    stderr = p.stderr.read()
    log("cmd is: " + cmd)
    log("stdout: " + stdout)
    log("stderr: " + stderr)
	
	
def git_push(filename_list, filepath):
    git_pull_cmd = 'git pull'
    git_add_cmd = 'git add %s' % " ".join(filename_list)
    git_commit_cmd = 'git commit %s -m "update version and date from 64 web page"' % " ".join(filename_list)
    git_push_cmd = 'git push origin main'
    for cmd in [git_pull_cmd, git_add_cmd, git_commit_cmd, git_push_cmd]:
        run_cmd(cmd, filepath)


def update_readme_version_date(readme_file, app_vername, type_name = None):
    all_lines = read_file_lines(readme_file)
    fp = open(readme_file, "w")
    for each_line in all_lines:
        if each_line.find(" DVDFab ") != -1 and each_line.find(".") != -1 and each_line.find("/") != -1:
            if type_name == "Non-Decryption":
                each_line = "    %s%s \n" % (app_vername, type_name)
            else:
                each_line = "    %s \n" % app_vername
        fp.write(each_line)
    fp.close()

def update_mac_readme_version_date(readme_file, version, date, type_name):
    if type_name.lower() == "official":
        app_vername = "DVDFab %s (%s) %s" % (version, date, type_name)
    else:
        app_vername = "DVDFab %s (%s) " % (version, date)
    all_lines = read_file_lines(readme_file)
    fp = open(readme_file, "w")
    for each_line in all_lines:
        if each_line.find(" DVDFab ") != -1 and each_line.find(".") != -1 and each_line.find("/") != -1:
            each_line = "    %s \n" % app_vername
        fp.write(each_line)
    fp.close()

def update_iss_version_date(iss_file, version, date, type_name):
    app_vername = ""
    output_basefilename = ""
    check_changelog = ""
    new_version = version.replace(".", "")
    if type_name.lower() == "beta":
        output_basefilename = "DVDFab%s%s" % (new_version, type_name)
        app_vername = "DVDFab %s (%s) %s" % (version, date, type_name)
        check_changelog = "Filename: {app}\Changes.txt; Description: {cm:WhatsNew}; Flags: nowait postinstall skipifsilent shellexec unchecked"
    else:
        output_basefilename = "DVDFab%s" % new_version
        app_vername = "DVDFab %s (%s) " % (version, date)
        check_changelog = "Filename: {app}\Changes.txt; Description: {cm:WhatsNew}; Flags: nowait postinstall skipifsilent shellexec "
    all_lines = read_file_lines(iss_file)
    fp = open(iss_file, "w")
    for each_line in all_lines:
        if each_line.startswith("OutputBaseFilename"):
            each_line = "OutputBaseFilename=%s\n" % output_basefilename
        elif each_line.startswith("AppVerName"):
            each_line = "AppVerName=%s\n" % app_vername
        elif each_line.find("{app}\Changes.txt;") != -1 and each_line.find("{cm:WhatsNew};") != -1:
            each_line = check_changelog + "\n"
        fp.write(each_line)
    fp.close()
    return app_vername
        

def update_version_date(name, version, date, type_name, changelog, product_file,changelog_name = None):
    #type_name = "official"	
    if version.count(".") == 3:
        final_version = version
    elif 0 < version.count(".") < 3 or version.count(".") > 3:
        return render_to_response("error.html")
    elif version.count(".") == 0:
	temp_version = ""
	for record in version:
            record += "."
            temp_version += record
        final_version = temp_version[:-1]
    #update product file version and date
    content = final_version + "|" + type_name + "|" + date
    if os.path.isfile(product_file):
        write_file(product_file, content)
    else:
        log("product file: %s is not a file.The ini file that product_file is empty!!!" % product_file)
    if changelog and changelog_name:
        linesep = os.linesep
        month_dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        day, mon, year = date.split('/')[0], date.split('/')[1], date.split('/')[2]
        content_list = read_file_lines(changelog_name)
        fp = open(changelog_name, "w")
        for i in content_list:
            if i == content_list[0]:
                #i = content_list[0] + linesep + "_" * 23 + linesep + month_dict[mon] + " " + day + "," + " " + year + linesep + "DVDFab " + final_version + " Updated!" + linesep * 2 + changelog + linesep
                #i = content_list[0] + "\n" + "_" * 23 + "\n" + month_dict[mon] + " " + day + "," + " " + year + "\n" + "DVDFab " + final_version + " Updated!" + "\n" * 2 + changelog + "\n"
                #i = content_list[0] + "\n" + "_" * 23 + month_dict[mon] + " " + day + "," + " " + year + "DVDFab " + final_version + " Updated!" + linesep + changelog
                i = content_list[0] + "\r\n" + "_" * 23 + "\r\n" + month_dict[mon] + " " + day + "," + " " + year + "\r\nDVDFab " + final_version + " Updated!\r\n\r\n" + changelog + "\r\n"
            fp.write(i)
        fp.close()
        #git_push(changelog_name)
		
def read_ini(filename,field, key):
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(filename)
        value = cf.get(field, key)
    except Exception, e:
        value = ""
        log("read ini exception: %s" % str(e))
    return value	
	
	
def get_all_ini_content(filename, field):
    product_file = read_ini(filename, field, "product_file")
    iss_file = read_ini(filename, field, "iss_file")
    readme_file = read_ini(filename, field, "readme_file")
    changelog_file = read_ini(filename, field, "changelog_file")
    dict_ini = {"product_file":product_file, "iss_file":iss_file, "readme_file": readme_file, "changelog_file": changelog_file}
    return dict_ini
	
@csrf_exempt    
def index(request):
    git_pull(GIT_LOCAL_PATH, GIT_LOCAL_PATH)
    #svn_uppath(BASE_PATH)

    flag = ""
    all_name_list = []
    name_list = []
    current_date=time.strftime('%d/%m/%Y')

    #get all DVDFabQxLibs branch
    all_branches_list = [i for i in set(get_all_branches(projects_path))]
    all_lines = read_file_lines(filename)
    for each_line in all_lines:
        name_list.append(each_line.strip())
	
    #Win DVDFab version
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab.ini"),"win_dvdfab")
    win_dvdfab_product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
    win_dvdfab_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["iss_file"])
    win_dvdfab_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["readme_file"])
    win_dvdfab_changelog = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
    DVDFab_9_Official_version, product_date = get_version(win_dvdfab_product_file)
    DVDFab_9_Beta_version = DVDFab_9_Official_version
    #Win DVDFab Retail
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab_retail.ini"),"win_dvdfab_retail")
    win_dvdfab_retail_product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
    win_dvdfab_retail_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["iss_file"]) 
    win_dvdfab_retail_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["readme_file"])
    DVDFab_Retail_version, product_date = get_version(win_dvdfab_retail_product_file)
    #Win DVDFab NonDec
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab_nondec.ini"),"win_dvdfab_nondec")
    win_dvdfab_nondec_product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
    win_dvdfab_nondec_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["iss_file"])
    win_dvdfab_nondec_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["readme_file"])
    DVDFabNonDecAll_version, product_date = get_version(win_dvdfab_nondec_product_file)
    """
    #Win SafeDVDCopy
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy.ini"),"win_safedvdcopy")
    win_safedvdcopy_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    win_safedvdcopy_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["iss_file"])
    win_safedvdcopy_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Win_SafeDVDCopy_version, product_date = get_version(win_safedvdcopy_product_file)
    #Win SafeDVDCopy Trial
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy_trial.ini"),"win_safedvdcopy_trial")
    win_safedvdcopy_trial_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    win_safedvdcopy_trail_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["iss_file"])
    win_safedvdcopy_trial_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Win_SafeDVDCopy_Trial_version, product_date = get_version(win_safedvdcopy_trial_product_file)
    #Win SafeDVDCopy Premium
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy_premium.ini"),"win_safedvdcopy_premium")
    win_safedvdcopy_premium_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    win_safedvdcopy_premium_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["iss_file"])
    win_safedvdcopy_premium_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Win_SafeDVDCopy_Premium_version, product_date = get_version(win_safedvdcopy_premium_product_file)
    #Win SafeDVDCopy Premium Trial
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy_premium_trial.ini"),"win_safedvdcopy_premium_trial")
    win_safedvdcopy_premium_trial_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    win_safedvdcopy_premium_trial_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["iss_file"])
    win_safedvdcopy_premium_trial_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Win_SafeDVDCopy_Premium_Trial_version, product_date = get_version(win_safedvdcopy_premium_trial_product_file)
	"""
    #Mac DVDFab
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/mac_dvdfab.ini"),"mac_dvdfab")
    mac_dvdfab_product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
    mac_dvdfab_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["readme_file"])
    mac_dvdfab_changelog = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
    DVDFab_9_Mac_Official_version, product_date = get_version(mac_dvdfab_product_file)
    DVDFab_9_Mac_Beta_version = DVDFab_9_Mac_Official_version
    """
    #Mac SafeDVDCopy
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy.ini"),"mac_safedvdcopy")
    mac_safedvdcopy_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    mac_safedvdcopy_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Mac_SafeDVDCopy_version, product_date = get_version(mac_safedvdcopy_product_file)
    #Mac SafeDVDCopy Trial
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy_trial.ini"),"mac_safedvdcopy_trial")
    mac_safedvdcopy_trial_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    mac_safedvdcopy_trial_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Mac_SafeDVDCopy_Trial_version, product_date = get_version(mac_safedvdcopy_trial_product_file)
    #Mac SafeDVDCopy Premium
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy_premium.ini"),"mac_safedvdcopy_premium")
    mac_safedvdcopy_premium_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    mac_safedvdcopy_premium_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Mac_SafeDVDCopy_Premium_version, product_date = get_version(mac_safedvdcopy_premium_product_file)
    #Mac SafeDVDCopy Premium Trial
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy_premium_trial.ini"),"mac_safedvdcopy_premium_trial")
    mac_safedvdcopy_premium_trial_product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
    mac_safedvdcopy_premium_trial_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["readme_file"])
    Mac_SafeDVDCopy_Premium_Trial_version, product_date = get_version(mac_safedvdcopy_premium_trial_product_file)
    #Win VidOnme
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "VidOnme/win_vidonme.ini"),"win_vidonme")
    win_vidonme_product_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["product_file"])
    win_vidonme_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["iss_file"])
    win_vidonme_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["readme_file"])
    Win_VidOnme_version, product_date = get_version(win_vidonme_product_file)
    #Mac VidOnme
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "VidOnme/mac_vidonme.ini"),"mac_vidonme")
    mac_vidonme_product_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["product_file"])
    mac_vidonme_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["readme_file"])
    Mac_VidOnme_version, product_date = get_version(mac_vidonme_product_file)
    #Win Sothink
    dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "Sothink/win_sothink.ini"),"win_sothink")
    win_sothink_product_file = os.path.join(os.path.join(CONFFILE_PATH, "Sothink"), dict_ini["product_file"])
    win_sothink_iss_file = os.path.join(os.path.join(CONFFILE_PATH, "Sothink"), dict_ini["iss_file"])
    win_sothink_readme_file = os.path.join(os.path.join(CONFFILE_PATH, "Sothink"), dict_ini["readme_file"])
    Win_Sothink_version, product_date = get_version(win_sothink_product_file)
    """
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        date = request.POST.get('date', '').strip()
        version = request.POST.get('version', '').strip()
        type_name = request.POST.get('type_name', '').strip()
        changelog = request.POST.get('changelog', '').strip()
        #DVDFab 9 Official
	if (name.upper() == "DVDFAB 9 OFFICIAL" or name.upper() == "DVDFAB9 OFFICIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_dvdfab_product_file,win_dvdfab_changelog)
	    app_vername = update_iss_version_date(win_dvdfab_iss_file, version, date, "official")
            update_readme_version_date(win_dvdfab_readme_file, app_vername)
            #git_push([win_dvdfab_product_file, win_dvdfab_iss_file, win_dvdfab_readme_file, win_dvdfab_changelog], os.path.dirname(win_dvdfab_product_file))

            update_version_date(name, version, date, "official", changelog, win_dvdfab_nondec_product_file)
	    app_vername = update_iss_version_date(win_dvdfab_nondec_iss_file, version, date, "official")
            update_readme_version_date(win_dvdfab_nondec_readme_file, app_vername, "Non-Decryption")
            git_push([win_dvdfab_product_file, win_dvdfab_iss_file, win_dvdfab_readme_file, win_dvdfab_changelog, win_dvdfab_nondec_product_file, win_dvdfab_nondec_iss_file, win_dvdfab_nondec_readme_file], os.path.dirname(win_dvdfab_product_file))
	    return render_to_response("success.html",locals())
	#DVDFab 9 Beta
	elif (name.upper() == "DVDFAB 9 BETA" or name.upper() == "DVDFAB9 BETA") and date and version:
	    update_version_date(name, version, date, "beta", changelog, win_dvdfab_product_file)
	    app_vername = update_iss_version_date(win_dvdfab_iss_file, version, date, "beta")
            update_readme_version_date(win_dvdfab_readme_file, app_vername)
            git_push([win_dvdfab_product_file, win_dvdfab_iss_file, win_dvdfab_readme_file], os.path.dirname(win_dvdfab_product_file))
	    return render_to_response("success.html",locals())
	#DVDFab Retail
	elif (name.upper() == "DVDFAB RETAIL" or name.upper() == "DVDFABRETAIL") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_dvdfab_retail_product_file)
	    app_vername = update_iss_version_date(win_dvdfab_retail_iss_file, version, date, "official")
            update_readme_version_date(win_dvdfab_retail_readme_file, app_vername)
            git_push([win_dvdfab_retail_product_file, win_dvdfab_retail_iss_file, win_dvdfab_retail_readme_file], os.path.dirname(win_dvdfab_retail_product_file))
	    return render_to_response("success.html",locals())
	#DVDFabNonDecAll
	elif (name.upper() == "DVDFABNONDECALL" or name.upper() == "DVDFAB NONDECALL") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_dvdfab_nondec_product_file)
	    app_vername = update_iss_version_date(win_dvdfab_nondec_iss_file, version, date, "official")
            update_readme_version_date(win_dvdfab_nondec_readme_file, app_vername)
            git_push([win_dvdfab_nondec_product_file, win_dvdfab_nondec_iss_file, win_dvdfab_nondec_readme_file], os.path.dirname(win_dvdfab_nondec_product_file))
	    return render_to_response("success.html",locals())
	#for Win SafeDVDCopy
	elif (name.upper() == "WINSAFEDVDCOPY" or name.upper() == "WIN SAFEDVDCOPY") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_safedvdcopy_product_file)
	    app_vername = update_iss_version_date(win_safedvdcopy_iss_file, version, date, "official")
            update_readme_version_date(win_safedvdcopy_readme_file, app_vername)
            git_push([win_safedvdcopy_product_file, win_safedvdcopy_iss_file, win_safedvdcopy_readme_file], os.path.dirname(win_safedvdcopy_product_file))
	    return render_to_response("success.html",locals())
	#SafeDVDCopy Trial version
	elif (name.upper() == "WINSAFEDVDCOPYTRIAL" or name.upper() == "WIN SAFEDVDCOPY TRIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_safedvdcopy_trial_product_file)
	    app_vername = update_iss_version_date(win_safedvdcopy_trial_iss_file, version, date, "official")
            update_readme_version_date(win_safedvdcopy_trial_readme_file, app_vername)
            git_push([win_safedvdcopy_trial_product_file, win_safedvdcopy_trial_iss_file, win_safedvdcopy_trial_readme_file], os.path.dirname(win_safedvdcopy_trial_product_file))
	    return render_to_response("success.html",locals())
	#SafeDVDCopy Premium version
	elif (name.upper() == "WINSAFEDVDCOPYPREMIUM" or name.upper() == "WIN SAFEDVDCOPY PREMIUM") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_safedvdcopy_premium_product_file)
	    app_vername = update_iss_version_date(win_safedvdcopy_premium_iss_file, version, date, "official")
            update_readme_version_date(win_safedvdcopy_premium_readme_file, app_vername)
            git_push([win_safedvdcopy_premium_product_file, win_safedvdcopy_premium_iss_file, win_safedvdcopy_premium_readme_file], os.path.dirname(win_safedvdcopy_premium_product_file))
	    return render_to_response("success.html",locals())
	#SafeDVDCopy Premium Trial version
	elif (name.upper() == "WINSAFEDVDCOPYPREMIUMTRIAL" or name.upper() == "WIN SAFEDVDCOPY PREMIUM TRIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_safedvdcopy_premium_trial_product_file)
	    app_vername = update_iss_version_date(win_safedvdcopy_premium_trial_iss_file, version, date, "official")
            update_readme_version_date(win_safedvdcopy_premium_trial_readme_file, app_vername)
            git_push([win_safedvdcopy_premium_trial_product_file, win_safedvdcopy_premium_trial_iss_file, win_safedvdcopy_premium_trial_readme_file], os.path.dirname(win_safedvdcopy_premium_trial_product_file))
	    return render_to_response("success.html",locals())
	#DVDFab 9 Mac Official version
	elif (name.upper() == "DVDFAB 9 MAC OFFICIAL" or name.upper() == "DVDFAB9 MAC OFFICIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, mac_dvdfab_product_file, mac_dvdfab_changelog)
            update_mac_readme_version_date(mac_dvdfab_readme_file, version, date, "official")
            git_push([mac_dvdfab_product_file, mac_dvdfab_readme_file, mac_dvdfab_changelog], os.path.dirname(mac_dvdfab_product_file))
	    return render_to_response("success.html",locals())
	#DVDFab 9 Mac Beta version
	elif (name.upper() == "DVDFAB 9 MAC BETA" or name.upper() == "DVDFAB9 MAC BETA") and date and version:
	    update_version_date(name, version, date, "beta", changelog, mac_dvdfab_product_file)
            update_mac_readme_version_date(mac_dvdfab_readme_file, version, date, "beta")
            git_push([mac_dvdfab_product_file, mac_dvdfab_readme_file], os.path.dirname(mac_dvdfab_product_file))
	    return render_to_response("success.html",locals())
	#Mac SafeDVDCopy version
	elif (name.upper() == "MACSAFEDVDCOPY" or name.upper() == "MAC SAFEDVDCOPY") and date and version:
	    update_version_date(name, version, date, "official", changelog, mac_safedvdcopy_product_file)
	    update_mac_readme_version_date(mac_safedvdcopy_readme_file, version, date, "official")
            git_push([mac_safedvdcopy_product_file, mac_safedvdcopy_readme_file], os.path.dirname(mac_safedvdcopy_product_file))
	    return render_to_response("success.html",locals())
	#Mac SafeDVDCopy Trial version
	elif (name.upper() == "MACSAFEDVDCOPYTRIAL" or name.upper() == "MAC SAFEDVDCOPY TRIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, mac_safedvdcopy_trial_product_file)
	    update_mac_readme_version_date(mac_safedvdcopy_trial_readme_file, version, date, "official")
            git_push([mac_safedvdcopy_trial_product_file, mac_safedvdcopy_trial_readme_file], os.path.dirname(mac_safedvdcopy_trial_product_file))
	    return render_to_response("success.html",locals())
	#Mac SafeDVDCopy Premium version
	elif (name.upper() == "MACSAFEDVDCOPYPREMIUM" or name.upper() == "MAC SAFEDVDCOPY PREMIUM") and date and version:
	    update_version_date(name, version, date, "official", changelog, mac_safedvdcopy_premium_product_file)
	    update_mac_readme_version_date(mac_safedvdcopy_premium_readme_file, version, date, "official")
            git_push([mac_safedvdcopy_premium_product_file, mac_safedvdcopy_premium_readme_file], os.path.dirname(mac_safedvdcopy_premium_product_file))
	    return render_to_response("success.html",locals())
	#Mac SafeDVDCopy Premium Trial version
	elif (name.upper() == "MACSAFEDVDCOPYPREMIUMTRIAL" or name.upper() == "MAC SAFEDVDCOPY PREMIUM TRIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, mac_safedvdcopy_premium_trial_product_file)
	    update_mac_readme_version_date(mac_safedvdcopy_premium_trial_readme_file, version, date, "official")
            git_push([mac_safedvdcopy_premium_trial_product_file, mac_safedvdcopy_premium_trial_readme_file], os.path.dirname(mac_safedvdcopy_premium_trial_product_file))
	    return render_to_response("success.html",locals())
	#Win VidOnme version
	elif (name.upper() == "WIN VIDONME" or name.upper() == "WINVIDONME") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_vidonme_product_file)
	    app_vername = update_iss_version_date(win_vidonme_iss_file, version, date, "official")
            update_readme_version_date(win_vidonme_readme_file, app_vername)
            git_push([win_vidonme_iss_file, win_vidonme_iss_file, win_vidonme_readme_file], os.path.dirname(win_vidonme_iss_file))
	    return render_to_response("success.html",locals())
	#Mac VidOnme version
	elif (name.upper() == "MAC VIDONME" or name.upper() == "MACVIDONME") and date and version:
	    update_version_date(name, version, date, "official", changelog, mac_vidonme_product_file)
	    update_mac_readme_version_date(mac_vidonme_readme_file, version, date, "official")
            git_push([mac_vidonme_product_file, mac_vidonme_readme_file], os.path.dirname(mac_vidonme_product_file))
	    return render_to_response("success.html",locals())
	#Win Sothink version
	elif (name.upper() == "WIN SOTHINK OFFICIAL" or name.upper() == "WIN SOTHINK OFFICIAL") and date and version:
	    update_version_date(name, version, date, "official", changelog, win_sothink_product_file)
	    app_vername = update_iss_version_date(win_sothink_iss_file, version, date, "official")
            update_readme_version_date(win_sothink_readme_file, app_vername)
            git_push([win_sothink_product_file, win_sothink_iss_file, win_sothink_readme_file], os.path.dirname(win_sothink_product_file))
	    return render_to_response("success.html",locals())
	elif (name.upper() == "WIN SOTHINK BETA" or name.upper() == "WINSOTHINK BETA") and date and version:
	    update_version_date(name, version, date, "beta", changelog, win_sothink_product_file)   
	    app_vername = update_iss_version_date(win_sothink_iss_file, version, date, "beta")
            update_readme_version_date(win_sothink_readme_file, app_vername)
            git_push([win_sothink_product_file, win_sothink_iss_file, win_sothink_readme_file], os.path.dirname(win_sothink_product_file))
	    return render_to_response("success.html",locals())
    all_lines = str([])	
    all_branches = []
    all_branches_length = len(all_branches)
    return render_to_response('index.html', locals(),context_instance = RequestContext(request))
	
def get_product_info(product_file):
    try:
        content = read_file(product_file)
        date = content.split("|")[2]
        version = content.split("|")[0]
    except Exception, e:
        date = ""
        version = ""
        log("get product info exception: %s" % str(e))
    return date, version

def get_change_log(change_log_file, version):
    change_log = []
    if os.path.exists(change_log_file):
        all_lines = read_file_lines(change_log_file)
        change_log_list = []
        for each_line in all_lines:
            if version in each_line and "Updated!" in each_line:
                try:
                    version_index = all_lines.index(each_line)
                    horizon_line = all_lines[version_index-2]
                    horizon_index = all_lines.index(horizon_line)
                    change_log_list = all_lines[horizon_index+1: horizon_index+1+all_lines[horizon_index+1:].index(horizon_line)]
                except Exception, e:
                    log("get_change_log exception: %s" % str(e))
        #for each_line in change_log_list:
        #    change_log.append(each_line)
        change_log = change_log_list
    return change_log


def search_info(request):
    name = request.GET.get("name", "").strip()
    current_date=time.strftime('%d/%m/%Y')
   
    #DVDFab 9 Beta
    if name.upper() == "DVDFAB 9 BETA" or name.upper() == "DVDFAB9 BETA":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab.ini"),"win_dvdfab")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
 
    #DVDFab 9 Official
    elif name.upper() == "DVDFAB 9 OFFICIAL" or name.upper() == "DVDFAB9 OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab.ini"),"win_dvdfab")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
        change_log_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = get_change_log(change_log_file, version)
    
    #DVDFabNonDecAll
    elif name.upper() == "DVDFABNONDECALL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab_nondec.ini"),"win_dvdfab_nondec")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Mac DVDFab 9 Beta
    elif name.upper() == "DVDFAB 9 MAC BETA" or name.upper() == "DVDFAB9 MAC BETA":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/mac_dvdfab.ini"),"mac_dvdfab")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Mac DVDFab 9 Official
    elif name.upper() == "DVDFAB 9 MAC OFFICIAL" or name.upper() == "DVDFAB9 MAC OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/mac_dvdfab.ini"),"mac_dvdfab")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["product_file"])
        change_log_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = get_change_log(change_log_file, version)
    

    #Win SafeDVDCopy
    elif name.upper() == "WIN SAFEDVDCOPY":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy.ini"),"win_safedvdcopy")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win SafeDVDCopy Trial
    elif name.upper() == "WIN SAFEDVDCOPY TRIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy_trial.ini"),"win_safedvdcopy_trial")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win SafeDVDCopy Premium
    elif name.upper() == "WIN SAFEDVDCOPY PREMIUM":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy_premium.ini"),"win_safedvdcopy_premium")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win SafeDVDCopy Premium Trial
    elif name.upper() == "WIN SAFEDVDCOPY PREMIUM TRIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/win_safedvdcopy_premium_trial.ini"),"win_safedvdcopy_premium_trial")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy
    elif name.upper() == "MAC SAFEDVDCOPY":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy.ini"),"mac_safedvdcopy")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy Trial
    elif name.upper() == "MAC SAFEDVDCOPY TRIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy_trial.ini"),"mac_safedvdcopy_trial")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy Premium
    elif name.upper() == "MAC SAFEDVDCOPY PREMIUM":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy_premium.ini"),"mac_safedvdcopy_premium")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy Premium Trial
    elif name.upper() == "MAC SAFEDVDCOPY PREMIUM TRIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "SafeDVDCopy/mac_safedvdcopy_premium_trial.ini"),"mac_safedvdcopy_premium_trial")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "SafeDVDCopy"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win VidOnme
    elif name.upper() == "WIN VIDONME":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "VidOnme/win_vidonme.ini"),"win_vidonme")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac VidOnme
    elif name.upper() == "MAC VIDONME":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "VidOnme/mac_vidonme.ini"),"mac_vidonme")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "VidOnme"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    

    #Win Sothink Beta
    elif name.upper() == "WIN SOTHINK BETA":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "Sothink/win_sothink.ini"),"win_sothink")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "Sothink"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
    
    #Win Sothink Official
    elif name.upper() == "WIN SOTHINK OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "Sothink/win_sothink.ini"),"win_sothink")
        product_file = os.path.join(os.path.join(CONFFILE_PATH, "Sothink"), dict_ini["product_file"])
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    else:
        name = name
        date = ""
        version = ""
        change_log = ""
    #return HttpResponse(version)
    return render_to_response("search_info.html", locals())


def get_all_change_log(change_log_file):
    change_log = []
    if os.path.exists(change_log_file):
        fp = open(change_log_file, "r")
        change_log = fp.read()
        fp.close()
    return change_log


@csrf_exempt
def update_change_log(request):
    content = read_file(r"d:\xudedong\name_temp.txt")
    name = content.strip()
    changelog = request.POST.get("changelog","").strip()
    if name.upper() == "DVDFAB 9 OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab.ini"),"win_dvdfab")
        change_log_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
        write_file(change_log_file, changelog)
        git_push([change_log_file], os.path.dirname(win_dvdfab_product_file))
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "DVDFAB 9 MAC OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/mac_dvdfab.ini"),"mac_dvdfab")
        change_log_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
        write_file(change_log_file, changelog)
        git_push([change_log_file], os.path.dirname(win_dvdfab_product_file))
        return render_to_response("update_changelog_success.html")
    else:
        return HttpResponseRedirect("/modify_change_log/?name=" + name)


def modify_change_log(request):
    name = request.GET.get("name", "").strip()
    write_file(r"d:\xudedong\name_temp.txt", name)
    #DVDFab 9 Official
    if name.upper() == "DVDFAB 9 OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/win_dvdfab.ini"),"win_dvdfab")
        change_log_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
        change_log = get_all_change_log(change_log_file) 
    #DVDFab 9 Mac Official
    elif name.upper() == "DVDFAB 9 MAC OFFICIAL":
        dict_ini = get_all_ini_content(os.path.join(CONFFILE_PATH, "DVDFab/mac_dvdfab.ini"),"mac_dvdfab")
        change_log_file = os.path.join(os.path.join(CONFFILE_PATH, "DVDFab"), dict_ini["changelog_file"])
        change_log = get_all_change_log(change_log_file) 
    else:
        change_log = "" 
 
    return render_to_response("modify_change_log.html", locals())       

def write_file(filename, content):
    fp = open(filename, "w")
    fp.write(content)
    fp.close()

@csrf_exempt
def add_branch(request):
    platform = request.POST.get("platform","").strip()
    project = request.POST.get("project","").strip()
    branch = request.POST.get("branch","").strip()
   
    manual_branch = request.POST.get("manual_branch","").strip()
    if manual_branch:
        branch_name = manual_branch
    else:
        branch_name = branch
    
    if platform.upper() == "WIN":
        write_files(BRANCH_TXT, platform + "=" + project + "=" + branch_name)
    else:
        write_files(BRANCH_MAC_TXT, platform + "=" + project + "=" + branch_name)
    return HttpResponseRedirect("/index/") 
    

@csrf_exempt
def modify_branch(request):
    checkbox = request.POST.getlist("checkbox", "")
    svn_uppath(os.path.splitext(BRANCH_TXT)[0])
    write_file(BRANCH_TXT, "")
    write_file(BRANCH_MAC_TXT, "")
    for record in checkbox:
        if record.upper().startswith("WIN=INCLUDE"):
            write_file(include_txt, record)
            write_files(BRANCH_TXT, record) 
        elif record.upper().startswith("WIN=BLURAY"):
            write_file(bluray_txt, record)
            write_files(BRANCH_TXT, record) 
        elif record.upper().startswith("WIN=COMMON"):
            write_file(common_txt, record)
            write_files(BRANCH_TXT, record) 
        elif record.upper().startswith("WIN=DVDFABQXLIBS"):
            write_file(DVDFabQxLibs_txt, record)
            write_files(BRANCH_TXT, record) 
        elif record.upper().startswith("WIN=MOBILE2"):
            write_file(mobile2_txt, record)
            write_files(BRANCH_TXT, record) 
        elif record.upper().startswith("MAC=INCLUDE"):
            write_file(include_mac_txt, record)
            write_files(BRANCH_MAC_TXT, record) 
        elif record.upper().startswith("MAC=BLURAY"):
            write_file(bluray_mac_txt, record)
            write_files(BRANCH_MAC_TXT, record) 
        elif record.upper().startswith("MAC=COMMON"):
            write_file(common_mac_txt, record)
            write_files(BRANCH_MAC_TXT, record) 
        elif record.upper().startswith("MAC=DVDFABQXLIBS"):
            write_file(DVDFabQxLibs_mac_txt, record)
            write_files(BRANCH_MAC_TXT, record) 
        elif record.upper().startswith("MAC=MOBILE2"):
            write_file(mobile2_mac_txt, record)
            write_files(BRANCH_MAC_TXT, record) 
        elif record.upper().startswith("WIN=TS"):
            write_file(ts_build_txt, record)
        else:
            pass

    svnpath = "/opt/local/bin/svn ci  "
    svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update from 170!"'
    cmdlist = [svnpath, BRANCH_TXT, BRANCH_MAC_TXT,include_txt, bluray_txt, common_txt, DVDFabQxLibs_txt, mobile2_txt, include_mac_txt, bluray_mac_txt, common_mac_txt, DVDFabQxLibs_mac_txt, mobile2_mac_txt, ts_build_txt, svn_param]
    cmd = " ".join(cmdlist)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
    out = p.stdout.read()
    err = p.stderr.read()
    log("out1111: " + out)
    log("err2222: " + err)
    return render_to_response("modify_branch.html", locals()) 

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
	
