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
LOGPATH = "/Users/DVDFab/log"
LOGNAME = "log.txt"


PRODUCT_WIN_TEMP_FILE = "/Volumes/MacintoshHD/auto_package/product_win_temp.txt"
PRODUCT_WIN_FILE = "/Volumes/MacintoshHD/auto_package/product_win.txt"
PRODUCT_MAC_FILE = "/Volumes/MacintoshHD/auto_package/product_mac.txt"
START_WIN_DAILY_BUILD_FILE = "/Volumes/MacintoshHD/auto_package/start_win_daily_build.txt"
START_MAC_DAILY_BUILD_FILE = "/Volumes/MacintoshHD/auto_package/start_mac_daily_build.txt"

BRANCH_TXT = "/Volumes/MacintoshHD/auto_package/branch.txt"
include_txt = "/Volumes/MacintoshHD/auto_package/include.txt"
bluray_txt = "/Volumes/MacintoshHD/auto_package/bluray.txt"
common_txt = "/Volumes/MacintoshHD/auto_package/common.txt"
DVDFabQxLibs_txt = "/Volumes/MacintoshHD/auto_package/DVDFabQxLibs.txt"
mobile2_txt = "/Volumes/MacintoshHD/auto_package/mobile2.txt"

BRANCH_MAC_TXT = "/Volumes/MacintoshHD/auto_package/branch_mac.txt"
include_mac_txt = "/Volumes/MacintoshHD/auto_package/include_mac.txt"
bluray_mac_txt = "/Volumes/MacintoshHD/auto_package/bluray_mac.txt"
common_mac_txt = "/Volumes/MacintoshHD/auto_package/common_mac.txt"
DVDFabQxLibs_mac_txt = "/Volumes/MacintoshHD/auto_package/DVDFabQxLibs_mac.txt"
mobile2_mac_txt = "/Volumes/MacintoshHD/auto_package/mobile2_mac.txt"
ts_build_txt = "/Volumes/MacintoshHD/auto_package/ts_build.txt"

DVDFabQxLibs_path = "/Volumes/X/DVDFab9_mini/branch/working_branch/goland/projects/DVDFabQxLibs"


default_encoding = 'utf-8'
if sys.getdefaultencoding()!=default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    

def log(info):
    logging.basicConfig(filename = LOGPATH + '/' + LOGNAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 

def svn_up(filename):
    svnup_cmdline = "/opt/local/bin/svn up --accept theirs-full "
    svnup_params = " --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert"
    svnup_cmdlist = [svnup_cmdline, filename,svnup_params]
    cmdline = " ".join(svnup_cmdlist)
    subprocess.call(cmdline, shell=True)
    
def svn_uppath(path):
    cmd = "/opt/local/bin/svn up --accept theirs-full "
    params = " --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert"
    cmdline = " ".join([cmd, path, params])
    subprocess.call(cmdline, shell=True)


def write_files(filename, content):
    fp = open(filename, "a+")
    fp.write(content + "\r\n")
    fp.close()


def read_file(filename):
    fp = open(filename, "r")
    content = fp.read()
    fp.close()
    return content

def get_all_branches(DVDFabQxLibs_path):
    all_branches_list = []
    all_branches_txt = "/Volumes/all_branches.txt"
    git_pull_origin_cmd = "git pull origin"
    p1 = subprocess.Popen(git_pull_origin_cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, cwd = DVDFabQxLibs_path, shell = True)
    fp = open("/Volumes/111.txt", "w")
    fp.write("out: " + p1.stdout.read())
    fp.write("\r\nerr: " + p1.stderr.read())
    fp.write("\r\npath: " + DVDFabQxLibs_path)
    fp.close()
    git_pull_cmd = "git pull"
    subprocess.Popen(git_pull_cmd, cwd = DVDFabQxLibs_path, shell = True)
    cmd = "git branch -a > " + all_branches_txt
    subprocess.call(cmd, cwd = DVDFabQxLibs_path, shell = True)
    fp = open(all_branches_txt, "r")
    all_lines = fp.readlines()
    fp.close()
    #all_branches_list.append(DVDFabQxLibs_path)
    for each_line in all_lines:
        if each_line.strip().startswith("remotes/origin") and each_line.count("origin") == 1:
            branch_name = each_line.split("origin/")[1]
            all_branches_list.append(branch_name)
    return all_branches_list


@csrf_exempt    
def index(request):
    os.system("sudo chmod -R 777 /Volumes/MacintoshHD/auto_package")
    os.system("sudo chown -R _www:_www /Volumes/MacintoshHD/auto_package")
    
    #delete it by xudedong at 2015-02-10
    #svn_up(PRODUCT_WIN_TEMP_FILE)
    #svn_up(PRODUCT_WIN_FILE)
    #svn_up(PRODUCT_MAC_FILE)
    svn_up(BRANCH_TXT)

    flag = ""
    all_name_list = []
    name_list = []
    """
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
    """

    #get all DVDFabQxLibs branch
    all_branches_list = get_all_branches(DVDFabQxLibs_path)

    if os.path.exists(filename):
        fp = open(filename,"r")
        all_lines = fp.readlines()
        fp.close()
        #name_list = all_lines
        for each_line in all_lines:
            name_list.append(each_line.strip())
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
        product_date = current_date
    else:
        DVDFab_8_version = ""
        product_date = current_date

    #BluFab 9  Official version
    product_blufab_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab.txt"
    if os.path.exists(product_blufab_txt):
        content = read_file(product_blufab_txt)
        BluFab_9_Official_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        BluFab_9_Official_version = ""
        product_date = current_date

    #BluFab 9 Beta version
    product_blufab_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab.txt"
    if os.path.exists(product_blufab_txt):
        content = read_file(product_blufab_txt)
        BluFab_9_Beta_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        BluFab_9_Beta_version = ""
        product_date = current_date 

    #DVDFab 9  Official version
    product_dvdfab_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab.txt"
    if os.path.exists(product_dvdfab_txt):
        content = read_file(product_dvdfab_txt)
        DVDFab_9_Official_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFab_9_Official_version = ""
        product_date = current_date

    #DVDFab 9 Beta version
    product_dvdfab_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab.txt"
    if os.path.exists(product_dvdfab_txt):
        content = read_file(product_dvdfab_txt)
        DVDFab_9_Beta_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFab_9_Beta_version = ""
        product_date = current_date
    
    #DVDFabUSANad 9  Official version
    product_dvdfabusanad_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad.txt"
    if os.path.exists(product_dvdfabusanad_txt):
        content = read_file(product_dvdfabusanad_txt)
        DVDFabUSANad_9_Official_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFabUSANad_9_Official_version = ""
        product_date = current_date

    #DVDFabUSANad 9 Beta version
    product_dvdfabusanad_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad.txt"
    if os.path.exists(product_dvdfabusanad_txt):
        content = read_file(product_dvdfabusanad_txt)
        DVDFabUSANad_9_Beta_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFabUSANad_9_Beta_version = ""
        product_date = current_date

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
    product_dvdfabnondec_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabnondec.txt"
    if os.path.exists(product_dvdfabnondec_txt):
        content = read_file(product_dvdfabnondec_txt)
        DVDFabNonDecAll_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFabNonDecAll_version = ""
        product_date = current_date

    #DVDFabNonDecAll German version
    product_dvdfabnondecde_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabnondecde.txt"
    if os.path.exists(product_dvdfabnondecde_txt):
        content = read_file(product_dvdfabnondecde_txt)
        DVDFabNonDecAll_German_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFabNonDecAll_German_version = ""
        product_date = current_date

    #TDMore
    product_tdmore_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd copy.txt"
    if os.path.exists(product_tdmore_txt):
        content = read_file(product_tdmore_txt)
        TDMore_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_version = ""
        product_date = current_date
    
    #TDMore Blu-ray Copy
    product_tdmore_bluray_copy_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore blu-ray copy.txt"
    if os.path.exists(product_tdmore_bluray_copy_txt):
        content = read_file(product_tdmore_bluray_copy_txt)
        TDMore_Bluray_Copy_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_Bluray_Copy_version = ""
        product_date = current_date
    

    #TDMore Blu-ray Converter
    product_tdmore_bluray_converter_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore blu-ray converter.txt"
    if os.path.exists(product_tdmore_bluray_converter_txt):
        content = read_file(product_tdmore_bluray_converter_txt)
        TDMore_Bluray_Converter_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_Bluray_Converter_version = ""
        product_date = current_date
    

    #TDMore DVD Copy
    product_tdmore_dvd_copy_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd copy.txt"
    if os.path.exists(product_tdmore_dvd_copy_txt):
        content = read_file(product_tdmore_dvd_copy_txt)
        TDMore_DVD_Copy_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_DVD_Copy_version = ""
        product_date = current_date
    

    #TDMore Free DVD Copy
    product_tdmore_free_dvd_copy_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore free dvd copy.txt"
    if os.path.exists(product_tdmore_free_dvd_copy_txt):
        content = read_file(product_tdmore_free_dvd_copy_txt)
        TDMore_Free_DVD_Copy_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_Free_DVD_Copy_version = ""
        product_date = current_date

    #TDMore DVD Converter
    product_tdmore_dvd_converter_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd converter.txt"
    if os.path.exists(product_tdmore_dvd_converter_txt):
        content = read_file(product_tdmore_dvd_converter_txt)
        TDMore_DVD_Converter_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_DVD_Converter_version = ""
        product_date = current_date
    

    #TDMore DVD to AVI Converter
    product_tdmore_dvd_to_avi_converter_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd to avi converter.txt"
    if os.path.exists(product_tdmore_dvd_to_avi_converter_txt):
        content = read_file(product_tdmore_dvd_to_avi_converter_txt)
        TDMore_DVD_to_AVI_Converter_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_DVD_to_AVI_Converter_version = ""
        product_date = current_date

    #SafeDVDCopy version
    product_safedvdcopy_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy.txt"
    if os.path.exists(product_safedvdcopy_txt):
        content = read_file(product_safedvdcopy_txt)
        Win_SafeDVDCopy_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Win_SafeDVDCopy_version = ""
        product_date = current_date
    
    #SafeDVDCopy Trial version
    product_safedvdcopy_trial_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy trial.txt"
    if os.path.exists(product_safedvdcopy_trial_txt):
        content = read_file(product_safedvdcopy_trial_txt)
        Win_SafeDVDCopy_Trial_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Win_SafeDVDCopy_Trial_version = ""
        product_date = current_date
    
    #SafeDVDCopy Premium version
    product_safedvdcopy_premium_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium.txt"
    if os.path.exists(product_safedvdcopy_premium_txt):
        content = read_file(product_safedvdcopy_premium_txt)
        Win_SafeDVDCopy_Premium_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Win_SafeDVDCopy_Premium_version = ""
        product_date = current_date
    

    #SafeDVDCopy Premium Trial version
    product_safedvdcopy_premium_trial_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium trial.txt"
    if os.path.exists(product_safedvdcopy_premium_trial_txt):
        content = read_file(product_safedvdcopy_premium_trial_txt)
        Win_SafeDVDCopy_Premium_Trial_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Win_SafeDVDCopy_Premium_Trial_version = ""
        product_date = current_date

    #DVDFab 9  Mac Official version
    product_dvdfab_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab_mac.txt"
    if os.path.exists(product_dvdfab_mac_txt):
        content = read_file(product_dvdfab_mac_txt)
        DVDFab_9_Mac_Official_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFab_9_Mac_Official_version = ""
        product_date = current_date

    #DVDFab 9 Mac Beta version
    product_dvdfab_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab_mac.txt"
    if os.path.exists(product_dvdfab_mac_txt):
        content = read_file(product_dvdfab_mac_txt)
        DVDFab_9_Mac_Beta_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFab_9_Mac_Beta_version = ""
        product_date = current_date
    
    #DVDFabUSANad 9 Mac Official version
    product_dvdfabusanad_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad_mac.txt"
    if os.path.exists(product_dvdfabusanad_mac_txt):
        content = read_file(product_dvdfabusanad_mac_txt)
        DVDFabUSANad_9_Mac_Official_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFabUSANad_9_Mac_Official_version = ""
        product_date = current_date

    #DVDFabUSANad 9 Mac Beta version
    product_dvdfabusanad_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad_mac.txt"
    if os.path.exists(product_dvdfabusanad_mac_txt):
        content = read_file(product_dvdfabusanad_mac_txt)
        DVDFabUSANad_9_Mac_Beta_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        DVDFabUSANad_9_Mac_Beta_version = ""
        product_date = current_date

    #BluFab 9  Mac Official version
    product_blufab_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab_mac.txt"
    if os.path.exists(product_blufab_mac_txt):
        content = read_file(product_blufab_mac_txt)
        BluFab_9_Mac_Official_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        BluFab_9_Mac_Official_version = ""
        product_date = current_date

    #BluFab 9 Mac Beta version
    product_blufab_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab_mac.txt"
    if os.path.exists(product_blufab_mac_txt):
        content = read_file(product_blufab_mac_txt)
        BluFab_9_Mac_Beta_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        BluFab_9_Mac_Beta_version = ""
        product_date = current_date
    

    #Mac SafeDVDCopy version
    product_safedvdcopy_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy_mac.txt"
    if os.path.exists(product_safedvdcopy_mac_txt):
        content = read_file(product_safedvdcopy_mac_txt)
        Mac_SafeDVDCopy_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Mac_SafeDVDCopy_version = ""
        product_date = current_date

    #Mac SafeDVDCopy Trial version
    product_safedvdcopy_trial_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy trial_mac.txt"
    if os.path.exists(product_safedvdcopy_trial_mac_txt):
        content = read_file(product_safedvdcopy_trial_mac_txt)
        Mac_SafeDVDCopy_Trial_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Mac_SafeDVDCopy_Trial_version = ""
        product_date = current_date

    #Mac SafeDVDCopy Premium version
    product_safedvdcopy_premium_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium_mac.txt"
    if os.path.exists(product_safedvdcopy_premium_mac_txt):
        content = read_file(product_safedvdcopy_premium_mac_txt)
        Mac_SafeDVDCopy_Premium_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Mac_SafeDVDCopy_Premium_version = ""
        product_date = current_date
    
    #Mac SafeDVDCopy Premium Trial version
    product_safedvdcopy_premium_trial_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium trial_mac.txt"
    if os.path.exists(product_safedvdcopy_premium_trial_mac_txt):
        content = read_file(product_safedvdcopy_premium_trial_mac_txt)
        Mac_SafeDVDCopy_Premium_Trial_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Mac_SafeDVDCopy_Premium_Trial_version = ""
        product_date = current_date

    #Win VidOnme version
    product_vidonme_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_VidOn Video ToolKit.txt"
    if os.path.exists(product_vidonme_txt):
        content = read_file(product_vidonme_txt)
        Win_VidOnme_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Win_VidOnme_version = ""
        product_date = current_date
    
    #Mac VidOnme version
    product_vidonme_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_VidOn Video ToolKit_mac.txt"
    if os.path.exists(product_vidonme_mac_txt):
        content = read_file(product_vidonme_mac_txt)
        Mac_VidOnme_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        Mac_VidOnme_version = ""
        product_date = current_date
    

    #TDMore Video Converter
    product_tdmore_video_converter_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore video converter.txt"
    if os.path.exists(product_tdmore_video_converter_txt):
        content = read_file(product_tdmore_video_converter_txt)
        TDMore_Video_Converter_version = content.split("|")[0]
        product_date = content.split("|")[2]
    else:
        TDMore_Video_Converter_version = ""
        product_date = current_date





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
        return render_to_response("success.html",locals())   
    
    #for DVDFab 9 Official
    #if (name.upper() == "DVDFAB 9 OFFICIAL" or name.upper() == "DVDFAB9 OFFICIAL") and date and version and changelog:
    if (name.upper() == "DVDFAB 9 OFFICIAL" or name.upper() == "DVDFAB9 OFFICIAL") and date and version:
        svn_up(product_dvdfab_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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

        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            for i in content_list:
                if i == content_list[0]:
                    i = content_list[0] + "\r\n" + "_" * 23 + "\r\n" + dict[mon] + " " + day + "," + " " + year + "\r\nDVDFab " + final_version + " Updated!\r\n\r\n" + changelog + "\r\n"
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab Changelog, iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfab_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for DVDFab 9 Beta
    if (name.upper() == "DVDFAB 9 BETA" or name.upper() == "DVDFAB9 BETA") and date and version:
        svn_up(product_dvdfab_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
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
        fp = open(product_dvdfab_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab iss file date and version from 170"'
        cmdlist = [svnpath, product_dvdfab_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for DVDFabUSANad 9 Official
    if (name.upper() == "DVDFABUSANAD 9 OFFICIAL" or name.upper() == "DVDFABUSANAD9 OFFICIAL") and date and version:
        svn_up(product_dvdfabusanad_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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
        fp = open(product_dvdfabusanad_txt, "w")
        fp.write(content)
        fp.close()

        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_DVDFabUSANad.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            for i in content_list:
                if i == content_list[0]:
                    i = content_list[0] + "\r\n" + "_" * 23 + "\r\n" + dict[mon] + " " + day + "," + " " + year + "\r\nDVDFab " + final_version + " Updated!\r\n\r\n" + changelog + "\r\n"
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabUSANad Changelog, iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfabusanad_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for DVDFabUSANad 9 Beta
    if (name.upper() == "DVDFABUSANAD 9 BETA" or name.upper() == "DVDFABUSANAD9 BETA") and date and version:
        svn_up(product_dvdfabusanad_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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
        fp = open(product_dvdfabusanad_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabUSANad iss file date and version from 170"'
        cmdlist = [svnpath, product_dvdfabusanad_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for BluFab 9 Official
    if (name.upper() == "BLUFAB 9 OFFICIAL" or name.upper() == "BluFAB9 OFFICIAL") and date and version:
        svn_up(product_blufab_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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

        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_BluFab.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "wb")
            for i in content_list:
                if i == content_list[0]:
                    i = content_list[0] + "\r\n" + "_" * 23 + "\r\n" + dict[mon] + " " + day + "," + " " + year + "\r\nBluFab " + final_version + " Updated!\r\n\r\n" + changelog + "\r\n"
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update BluFab Changelog, product file date and version from 170!"'
        cmdlist = [svnpath, product_blufab_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())


    #for BluFab 9 Beta
    if (name.upper() == "BLUFAB 9 BETA" or name.upper() == "BLUFAB9 BETA") and date and version:
        #subprocess.call("sudo chown _www:_www " + product_blufab_txt, shell=True)
        svn_up(product_blufab_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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
        fp = open(product_blufab_txt, "w")
        fp.write(content)
        fp.close()
        
        svnpath = '/opt/local/bin/svn ci  '
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update BluFab iss file date and version from 170!"'
        cmdlist = [svnpath, product_blufab_txt, svn_param]
        cmd = "  ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for DVDFab Retail
    if (name.upper() == "DVDFAB RETAIL" or name.upper() == "DVDFABRETAIL") and date and version:
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        update_update_iss_py = "D:\\Develop\\trunk\\official\\DVDFab_9_mobile2_Official\\Retail_Japan\\update_update_iss.py"
        update_iss_py = "D:\\Develop\\trunk\\official\\DVDFab_9_mobile2_Official\\Retail_Japan\\update_iss.py"
        type_name = "official"
        os.system("python " + update_update_iss_py + " " + version.replace(".", "") + " " + date + " " + type_name)
        os.system("python " + update_iss_py)
        return render_to_response("success.html",locals())


    #for DVDFabNonDecAll
    if (name.upper() == "DVDFABNONDECALL" or name.upper() == "DVDFAB NONDECALL") and date and version:
        svn_up(product_dvdfabnondec_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabNonDecAll iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfabnondec_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for DVDFabNonDecAll German
    if (name.upper() == "DVDFABNONDECALL GERMAN" or name.upper() == "DVDFAB NONDECALL GERMAN") and date and version:
        svn_up(product_dvdfabnondecde_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
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

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabNonDecAll German iss file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfabnondecde_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for TDMore Blu-ray Copy
    if name.upper() == "TDMORE BLU-RAY COPY" and date and version:
        product_tdmore_bluray_copy_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore blu-ray copy.txt'
        product_tdmore_bluray_copy_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore blu-ray copy.txt"'
        svn_up(product_tdmore_bluray_copy_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_bluray_copy_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_Blu-ray_Copy.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore Blu-ray Copy "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore Blu-ray Copy "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_bluray_copy_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for TDMore Blu-ray Converter
    if name.upper() == "TDMORE BLU-RAY CONVERTER" and date and version:
        product_tdmore_bluray_converter_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore blu-ray converter.txt'
        product_tdmore_bluray_converter_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore blu-ray converter.txt"'
        svn_up(product_tdmore_bluray_converter_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_bluray_converter_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_Blu-ray_Converter.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore Blu-ray Converter "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore Blu-ray Converter "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_bluray_converter_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for TDMore DVD Copy
    if name.upper() == "TDMORE DVD COPY" and date and version:
        product_tdmore_dvd_copy_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd copy.txt'
        product_tdmore_dvd_copy_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore dvd copy.txt"'
        svn_up(product_tdmore_dvd_copy_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_dvd_copy_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_DVD_Copy.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore DVD Copy "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore DVD Copy "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_dvd_copy_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    

    #for TDMore Free DVD Copy
    if name.upper() == "TDMORE FREE DVD COPY" and date and version:
        product_tdmore_free_dvd_copy_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore free dvd copy.txt'
        product_tdmore_free_dvd_copy_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore free dvd copy.txt"'
        svn_up(product_tdmore_free_dvd_copy_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_free_dvd_copy_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_Free_DVD_Copy.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore Free DVD Copy "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore Free DVD Copy "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_free_dvd_copy_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())


    #for TDMore DVD Converter
    if name.upper() == "TDMORE DVD CONVERTER" and date and version:
        product_tdmore_dvd_converter_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd converter.txt'
        product_tdmore_dvd_converter_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore dvd converter.txt"'
        svn_up(product_tdmore_dvd_converter_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_dvd_converter_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_DVD_Converter.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore DVD Converter "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore DVD Converter "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_dvd_converter_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    

    #for TDMore DVD to AVI  Converter
    if name.upper() == "TDMORE DVD TO AVI CONVERTER" and date and version:
        product_tdmore_dvd_to_avi_converter_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd to avi converter.txt'
        product_tdmore_dvd_to_avi_converter_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore dvd to avi converter.txt"'
        svn_up(product_tdmore_dvd_to_avi_converter_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_dvd_to_avi_converter_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_DVD_to_AVI_Converter.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore DVD to AVI Converter "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore DVD to AVI Converter "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_dvd_to_avi_converter_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for Win SafeDVDCopy
    if (name.upper() == "WINSAFEDVDCOPY" or name.upper() == "WIN SAFEDVDCOPY") and date and version:
        svn_up(product_safedvdcopy_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
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
        fp = open(product_safedvdcopy_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for Win SafeDVDCopy Trial
    if (name.upper() == "WINSAFEDVDCOPYTRIAL" or name.upper() == "WIN SAFEDVDCOPY TRIAL") and date and version:
        product_safedvdcopy_trial_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy trial.txt"
        product_safedvdcopy_trial_txt1= '/Volumes/MacintoshHD/Runtime_mobile2/"product_safedvdcopy trial.txt"'
        svn_up(product_safedvdcopy_trial_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
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
        fp = open(product_safedvdcopy_trial_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy Trial product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_trial_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    

    #for Win SafeDVDCopy Premium
    if (name.upper() == "WINSAFEDVDCOPYPREMIUM" or name.upper() == "WIN SAFEDVDCOPY PREMIUM") and date and version:
        product_safedvdcopy_premium_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium.txt"
        product_safedvdcopy_premium_txt1= '/Volumes/MacintoshHD/Runtime_mobile2/"product_safedvdcopy premium.txt"'
        svn_up(product_safedvdcopy_premium_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
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
        fp = open(product_safedvdcopy_premium_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy Premium product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_premium_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())


    #for Win SafeDVDCopy Premium Trial
    if (name.upper() == "WINSAFEDVDCOPYPREMIUMTRIAL" or name.upper() == "WIN SAFEDVDCOPY PREMIUM TRIAL") and date and version:
        product_safedvdcopy_premium_trial_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium trial.txt"
        product_safedvdcopy_premium_trial_txt1= '/Volumes/MacintoshHD/Runtime_mobile2/"product_safedvdcopy premium trial.txt"'
        svn_up(product_safedvdcopy_premium_trial_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
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
        fp = open(product_safedvdcopy_premium_trial_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy Premium Trial product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_premium_trial_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())


    #for DVDFab 9 Mac Beta
    if (name.upper() == "DVDFAB 9 MAC BETA" or name.upper() == "DVDFAB9 MAC BETA") and date and version:
        svn_up(product_dvdfab_mac_txt)
        write_files(PRODUCT_MAC_FILE,name)
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
        fp = open(product_dvdfab_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab product file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfab_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())


    #for DVDFab 9 Mac Official
    if (name.upper() == "DVDFAB 9 MAC OFFICIAL" or name.upper() == "DVDFAB9 MAC OFFICIAL") and date and version:
        svn_up(product_dvdfab_mac_txt)
        write_files(PRODUCT_MAC_FILE,name)
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
        fp = open(product_dvdfab_mac_txt, "w")
        fp.write(content)
        fp.close()

        changelog_name = "/Volumes/MacintoshHD/Develop/DVDFab_Mac_Common/Fab9_Mac_Changes.txt"
        temp_file = "/Volumes/MacintoshHD/Develop/DVDFab_Mac_Common/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
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
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab Changelog, product file date and version from 170!"'
        cmdlist = [svnpath, product_dvdfab_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for DVDFabUSANad 9 Mac Official
    if (name.upper() == "DVDFABUSANAD 9 MAC OFFICIAL" or name.upper() == "DVDFABUSANAD9 MAC OFFICIAL") and date and version:
        svn_up(product_dvdfabusanad_mac_txt)
        write_files(PRODUCT_MAC_FILE,name)
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
        fp = open(product_dvdfabusanad_mac_txt, "w")
        fp.write(content)
        fp.close()

        changelog_name = "/Volumes/MacintoshHD/Develop/DVDFabUSANad_Mac_Common/Fab9_Mac_Changes.txt"
        temp_file = "/Volumes/MacintoshHD/Develop/DVDFab_Mac_Common/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            for i in content_list:
                if i == content_list[0]:
                    i = content_list[0] + "\r\n" + "_" * 23 + "\r\n" + dict[mon] + " " + day + "," + " " + year + "\r\nDVDFab " + final_version + " Updated!\r\n\r\n" + changelog + "\r\n"
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabUSANad Changelog, product date and version from 170!"'
        cmdlist = [svnpath, product_dvdfabusanad_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for DVDFabUSANad 9 Mac Beta
    if (name.upper() == "DVDFABUSANAD 9 MAC BETA" or name.upper() == "DVDFABUSANAD9 MAC BETA") and date and version:
        svn_up(product_dvdfabusanad_mac_txt)
        write_files(PRODUCT_MAC_FILE,name)
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
        fp = open(product_dvdfabusanad_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFabUSANad product file date and version from 170"'
        cmdlist = [svnpath, product_dvdfabusanad_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    
    #for BluFab 9 Mac Beta
    if (name.upper() == "BLUFAB 9 MAC BETA" or name.upper() == "BLUFAB9 MAC BETA") and date and version:
        svn_up(product_blufab_mac_txt)
        write_files(PRODUCT_MAC_FILE,name)
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
        fp = open(product_blufab_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab product file date and version from 170!"'
        cmdlist = [svnpath, product_blufab_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())


    #for BluFab 9 Mac Official
    if (name.upper() == "BLUFAB 9 MAC OFFICIAL" or name.upper() == "BLUFAB9 MAC OFFICIAL") and date and version:
        svn_up(product_blufab_mac_txt)
        write_files(PRODUCT_MAC_FILE,name)
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
        fp = open(product_blufab_mac_txt, "w")
        fp.write(content)
        fp.close()

        changelog_name = "/Volumes/MacintoshHD/Develop/BluFab_Mac_Common/Fab9_Mac_Changes.txt"
        temp_file = "/Volumes/MacintoshHD/Develop/BluFab_Mac_Common/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
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
        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update BluFab Changelog, product file date and version from 170!"'
        cmdlist = [svnpath, product_blufab_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for Mac SafeDVDCopy
    if (name.upper() == "MACSAFEDVDCOPY" or name.upper() == "MAC SAFEDVDCOPY") and date and version:
        svn_up(product_safedvdcopy_mac_txt)
        #write_files(PRODUCT_MAC_TEMP_FILE,name)
        write_files(PRODUCT_MAC_FILE,name)
        
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
        fp = open(product_safedvdcopy_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for Mac SafeDVDCopy Trial
    if (name.upper() == "MACSAFEDVDCOPYTRIAL" or name.upper() == "MAC SAFEDVDCOPY TRIAL") and date and version:
        product_safedvdcopy_trial_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy trial_mac.txt"
        product_safedvdcopy_trial_mac_txt1= '/Volumes/MacintoshHD/Runtime_mobile2/"product_safedvdcopy trial_mac.txt"'
        svn_up(product_safedvdcopy_trial_mac_txt1)
        #write_files(PRODUCT_MAC_TEMP_FILE,name)
        write_files(PRODUCT_MAC_FILE,name)
        
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
        fp = open(product_safedvdcopy_trial_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy Trial product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_trial_mac_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    
    #for Mac SafeDVDCopy Premium
    if (name.upper() == "MACSAFEDVDCOPYPREMIUM" or name.upper() == "MAC SAFEDVDCOPY PREMIUM") and date and version:
        product_safedvdcopy_premium_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium_mac.txt"
        product_safedvdcopy_premium_mac_txt1= '/Volumes/MacintoshHD/Runtime_mobile2/"product_safedvdcopy premium_mac.txt"'
        svn_up(product_safedvdcopy_premium_mac_txt1)
        #write_files(PRODUCT_MAC_TEMP_FILE,name)
        write_files(PRODUCT_MAC_FILE,name)
        
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
        fp = open(product_safedvdcopy_premium_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy Premium product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_premium_mac_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for Mac SafeDVDCopy Premium Trial
    if (name.upper() == "MACSAFEDVDCOPYPREMIUMTRIAL" or name.upper() == "MAC SAFEDVDCOPY PREMIUM TRIAL") and date and version:
        product_safedvdcopy_premium_trial_mac_txt= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium trial_mac.txt"
        product_safedvdcopy_premium_trial_mac_txt1= '/Volumes/MacintoshHD/Runtime_mobile2/"product_safedvdcopy premium trial_mac.txt"'
        svn_up(product_safedvdcopy_premium_trial_mac_txt1)
        #write_files(PRODUCT_MAC_TEMP_FILE,name)
        write_files(PRODUCT_MAC_FILE,name)
        
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
        fp = open(product_safedvdcopy_premium_trial_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update SafeDVDCopy Premium Trial product file date and version from 170"'
        cmdlist = [svnpath, product_safedvdcopy_premium_trial_mac_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())

    #for Win VidOnme
    if (name.upper() == "WIN VIDONME" or name.upper() == "WINVIDONME") and date and version:
        svn_up(product_vidonme_txt)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
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
        fp = open(product_vidonme_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab iss file date and version from 170"'
        cmdlist = [svnpath, product_vidonme_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html",locals())
    

    #for Mac VidOnme
    if (name.upper() == "MAC VIDONME" or name.upper() == "MACVIDONME") and date and version:
        svn_up(product_vidonme_mac_txt)
        #write_files(PRODUCT_MAC_TEMP_FILE,name)
        write_files(PRODUCT_MAC_FILE,name)
        
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
        fp = open(product_vidonme_mac_txt, "w")
        fp.write(content)
        fp.close()

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update DVDFab iss file date and version from 170"'
        cmdlist = [svnpath, product_vidonme_mac_txt,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html", locals())

    #for TDMore Video Converter
    if name.upper() == "TDMORE VIDEO CONVERTER" and date and version:
        product_tdmore_video_converter_txt = '/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore video converter.txt'
        product_tdmore_video_converter_txt1 = '/Volumes/MacintoshHD/Runtime_mobile2/"product_tdmore video converter.txt"'
        svn_up(product_tdmore_video_converter_txt1)
        write_files(PRODUCT_WIN_TEMP_FILE,name)
        
        type_name = "official"
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
        
        content = final_version + "|" + type_name + "|" + date
        fp = open(product_tdmore_video_converter_txt, "w")
        fp.write(content)
        fp.close()
        
        changelog_name = "/Volumes/MacintoshHD/V9_Qt/Changes_TDMore_Video_Converter.txt"
        temp_file = "/Volumes/MacintoshHD/V9_Qt/temp_file.txt"
        dict = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        if changelog:
            fp = open(changelog_name, "r")
            contents = fp.read()
            fp.close()
            day = date.split('/')[0]
            mon = date.split('/')[1]
            year = date.split('/')[2]
            fp = open(changelog_name, 'r')
            content_list = fp.readlines()
            fp.close()
            fp = open(temp_file, "w")
            if len(content_list) == 0:
                content = "TDMore Video Converter "+ final_version + " changelog" + "\r\n" + changelog
                fp.write(content)
            for i in content_list:
                if i == content_list[0]:
                    i = "TDMore Video Converter "+ final_version + " changelog" + "\r\n" + changelog + "\r\n\r\n" + content_list[0]
                fp.write(i)
            fp.close()
            if os.path.exists(changelog_name):
                os.remove(changelog_name)
            if os.path.exists(temp_file):
                os.rename(temp_file, changelog_name)

        svnpath = "/opt/local/bin/svn ci  "
        svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update TDMore product file date and version from 170"'
        cmdlist = [svnpath,product_tdmore_video_converter_txt1,svn_param]
        cmd = " ".join(cmdlist)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        
        changelog_cmdlist = [svnpath, changelog_name,svn_param]
        changelog_cmd = " ".join(changelog_cmdlist)
        subprocess.Popen(changelog_cmd, stdout=subprocess.PIPE, shell=True)
        return render_to_response("success.html", locals())


    #for VDM Server
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
   
     
    fp = open(PRODUCT_WIN_TEMP_FILE, "r")
    win_all_lines = fp.readlines()
    fp.close()    
    fp = open(PRODUCT_MAC_FILE, "r")
    mac_all_lines = fp.readlines()
    fp.close()  
    win_all_lines = [i for i in set(win_all_lines) if i.strip()] 
    mac_all_lines = [i for i in set(mac_all_lines) if i.strip()] 
    all_lines = str(win_all_lines + mac_all_lines)
    #return HttpResponse(all_lines)
    
    fp = open(BRANCH_TXT, "r")
    all_branches_win = fp.readlines()
    fp.close()
    all_branches_win = [i for i in set(all_branches_win) if i.strip()]
    
    fp = open(BRANCH_MAC_TXT, "r")
    all_branches_mac = fp.readlines()
    fp.close()
    all_branches_mac = [i for i in set(all_branches_mac) if i.strip()]
    all_branches = all_branches_win + all_branches_mac
    all_branches_length = len(all_branches)
    return render_to_response('index.html', locals(),context_instance = RequestContext(request))

def get_product_info(product_file):
    if os.path.exists(product_file):
        content = read_file(product_file)
        date = content.split("|")[2]
        version = content.split("|")[0]
    else:
        date = ""
        version = ""
    return date, version

def get_change_log(change_log_file, version):
    change_log = []
    if os.path.exists(change_log_file):
        fp = open(change_log_file, "r")
        all_lines = fp.readlines()
        fp.close()
        change_log_list = []
        for each_line in all_lines:
            if version in each_line and "Updated!" in each_line:
                version_index = all_lines.index(each_line)
                horizon_line = all_lines[version_index-2]
                horizon_index = all_lines.index(horizon_line)
                change_log_list = all_lines[horizon_index+1: horizon_index+1+all_lines[horizon_index+1:].index(horizon_line)]
        for each_line in change_log_list:
            change_log.append(each_line)
    return change_log

def get_tdmore_change_log(change_log_file, version):
    change_log = []
    if os.path.exists(change_log_file):
        fp = open(change_log_file, "r")
        all_lines = fp.readlines()
        fp.close()
        change_log_list = []
        for each_line in all_lines:
            if each_line.strip() == "":
                space_index = all_lines.index(each_line)
                change_log_list = all_lines[:space_index]
                break
        for each_line in change_log_list:
            change_log.append(each_line)
    return change_log


def search_info(request):
    name = request.POST.get("name", "").strip()
    current_date=time.strftime('%d/%m/%Y')
    #DVDFab 8
    if name.upper() == "DVDFAB 8" or name.upper() == "DVDFAB8":
        name = name
        date = current_date
        version = ""
        change_log = ""
    
    #DVDFab 9 Beta
    elif name.upper() == "DVDFAB 9 BETA" or name.upper() == "DVDFAB9 BETA":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
 
    #DVDFab 9 Official
    elif name.upper() == "DVDFAB 9 OFFICIAL" or name.upper() == "DVDFAB9 OFFICIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab.txt"
        change_log_file= "/V9_Qt/Changes.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_change_log(change_log_file, version)
    
    #DVDFabUSANad 9 Beta
    elif name.upper() == "DVDFABUSANAD 9 BETA" or name.upper() == "DVDFABUSANAD9 BETA":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #DVDFabUSANad 9 Official
    elif name.upper() == "DVDFABUSANAD 9 OFFICIAL" or name.upper() == "DVDFABUSANAD9 OFFICIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad.txt"
        change_log_file= "/V9_Qt/Changes_DVDFabUSANad.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_change_log(change_log_file, version)
    
    #DVDFabNonDecAll
    elif name.upper() == "DVDFABNONDECALL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabnondec.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Mac DVDFab 9 Beta
    elif name.upper() == "DVDFAB 9 MAC BETA" or name.upper() == "DVDFAB9 MAC BETA":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Mac DVDFab 9 Official
    elif name.upper() == "DVDFAB 9 MAC OFFICIAL" or name.upper() == "DVDFAB9 MAC OFFICIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfab_mac.txt"
        change_log_file = "/Volumes/MacintoshHD/Develop/DVDFab_Mac_Common/Fab9_Mac_Changes.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_change_log(change_log_file, version)
    
    #Mac DVDFabUSANad 9 Beta
    elif name.upper() == "DVDFABUSANAD 9 MAC BETA" or name.upper() == "DVDFABUSANAD9 MAC BETA":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Mac DVDFabUSANad 9 Official
    elif name.upper() == "DVDFABUSANAD 9 MAC OFFICIAL" or name.upper() == "DVDFABUSANAD9 MAC OFFICIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_dvdfabusanad_mac.txt"
        change_log_file = "/Volumes/MacintoshHD/Develop/DVDFabUSANad_Mac_Common/Fab9_Mac_Changes.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_change_log(change_log_file, version)



    #TDMore Blu-ray Copy
    elif name.upper() == "TDMORE BLU-RAY COPY":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore blu-ray copy.txt"
        change_log_file = "/V9_Qt/Changes_TDMore_Blu-ray_Copy.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #TDMore Blu-ray Converter
    elif name.upper() == "TDMORE BLU-RAY CONVERTER":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore blu-ray converter.txt"
        change_log_file = "/V9_Qt/Changes_TDMore_Blu-ray_Converter.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #TDMore DVD Copy
    elif name.upper() == "TDMORE DVD COPY":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd copy.txt"
        change_log_file = "/V9_Qt/Changes_TDMore_DVD_Copy.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #TDMore Free DVD Copy
    elif name.upper() == "TDMORE FREE DVD COPY":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore free dvd copy.txt"
        change_log_file = "/V9_Qt/Changes_Free_TDMore_DVD_Copy.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #TDMore DVD Converter
    elif name.upper() == "TDMORE DVD CONVERTER":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd converter.txt"
        change_log_file = "/V9_Qt/Changes_TDMore_DVD_Converter.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #TDMore DVD to AVI Converter
    elif name.upper() == "TDMORE DVD TO AVI CONVERTER":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore dvd to avi converter.txt"
        change_log_file = "/V9_Qt/Changes_TDMore_DVD_to_AVI_Converter.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #TDMore Video Converter
    elif name.upper() == "TDMORE VIDEO CONVERTER":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_tdmore video converter.txt"
        change_log_file = "/V9_Qt/Changes_TDMore_Video_Converter.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = get_tdmore_change_log(change_log_file, version)

    #Win SafeDVDCopy
    elif name.upper() == "WIN SAFEDVDCOPY":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win SafeDVDCopy Trial
    elif name.upper() == "WIN SAFEDVDCOPY TRIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy trial.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win SafeDVDCopy Premium
    elif name.upper() == "WIN SAFEDVDCOPY PREMIUM":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win SafeDVDCopy Premium Trial
    elif name.upper() == "WIN SAFEDVDCOPY PREMIUM TRIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium trial.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy
    elif name.upper() == "MAC SAFEDVDCOPY":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy Trial
    elif name.upper() == "MAC SAFEDVDCOPY TRIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy trial_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy Premium
    elif name.upper() == "MAC SAFEDVDCOPY PREMIUM":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac SafeDVDCopy Premium Trial
    elif name.upper() == "MAC SAFEDVDCOPY PREMIUM TRIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_safedvdcopy premium trial_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Win VidOnme
    elif name.upper() == "WIN VIDONME":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_VidOn Video ToolKit.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    #Mac VidOnme
    elif name.upper() == "MAC VIDONME":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_VidOn Video ToolKit_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Win BluFab 9 Beta
    elif name.upper() == "BLUFAB 9 BETA" or name.upper() == "BLUFAB9 BETA":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab.txt"
        name = name
        date, version = get_product_info(product_file)
    
    #Win BluFab 9 Official
    elif name.upper() == "BLUFAB 9 OFFICIAL" or name.upper() == "BLUFAB9 OFFICIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""
    
    #Mac BluFab 9 Beta
    elif name.upper() == "BLUFAB 9 MAC BETA" or name.upper() == "BLUFAB9 MAC BETA":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab_mac.txt"
        name = name
        date, version = get_product_info(product_file)
    
    #Mac BluFab 9 Official
    elif name.upper() == "BLUFAB 9 MAC OFFICIAL" or name.upper() == "BLUFAB9 MAC OFFICIAL":
        product_file= "/Volumes/MacintoshHD/Runtime_mobile2/product_blufab_mac.txt"
        name = name
        date, version = get_product_info(product_file)
        change_log = ""

    else:
        name = name
        date = ""
        version = ""
        change_log = ""



    return render_to_response("search_info.html", locals())


def get_all_change_log(change_log_file):
    change_log = []
    if os.path.exists(change_log_file):
        fp = open(change_log_file, "r")
        change_log = fp.read()
        fp.close()

    return change_log


def ci_change_log(change_log_file):
    svnpath = "/opt/local/bin/svn ci  "
    svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update Changelog from 170!"'
    cmdlist = [svnpath, change_log_file,svn_param]
    cmd = " ".join(cmdlist)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)



@csrf_exempt
def update_change_log(request):
    content = read_file("/Users/DVDFab/name_temp.txt")
    name = content.strip()
    changelog = request.POST.get("changelog","").strip()
    if name.upper() == "DVDFAB 9 OFFICIAL":
        change_log_file= "/V9_Qt/Changes.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "DVDFABUSANAD 9 OFFICIAL":
        change_log_file= "/V9_Qt/Changes_DVDFabUSANad.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "DVDFAB 9 MAC OFFICIAL":
        change_log_file= "/Volumes/MacintoshHD/Develop/DVDFab_Mac_Common/Fab9_Mac_Changes.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "DVDFABUSANAD 9 MAC OFFICIAL":
        change_log_file= "/Volumes/MacintoshHD/Develop/DVDFabUSANad_Mac_Common/Fab9_Mac_Changes.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "TDMORE BLU-RAY COPY":
        change_log_file= "/V9_Qt/Changes_TDMore_Blu-ray_Copy.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "TDMORE BLU-RAY CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_Blu-ray_Converter.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "TDMORE DVD COPY":
        change_log_file= "/V9_Qt/Changes_TDMore_DVD_Copy.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "TDMORE FREE DVD COPY":
        change_log_file= "/V9_Qt/Changes_TDMore_Free_DVD_Copy.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "TDMORE DVD CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_DVD_Converter.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    elif name.upper() == "TDMORE VIDEO CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_Video_Converter.txt"
        write_file(change_log_file, changelog)
        ci_change_log(change_log_file)
        return render_to_response("update_changelog_success.html")
    else:
        return HttpResponseRedirect("/modify_change_log/?name=" + name)



def modify_change_log(request):
    name = request.GET.get("name", "").strip()
    write_file("/Users/DVDFab/name_temp.txt", name)
    #DVDFab 9 Official
    if name.upper() == "DVDFAB 9 OFFICIAL":
        change_log_file= "/V9_Qt/Changes.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #DVDFabUSANad 9 Official
    elif name.upper() == "DVDFABUSANAD 9 OFFICIAL":
        change_log_file= "/V9_Qt/Changes_DVDFabUSANad.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #DVDFab 9 Mac Official
    elif name.upper() == "DVDFAB 9 MAC OFFICIAL":
        change_log_file= "/Volumes/MacintoshHD/Develop/DVDFab_Mac_Common/Fab9_Mac_Changes.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #DVDFabUSANad 9 Mac Official
    elif name.upper() == "DVDFABUSANAD 9 MAC OFFICIAL":
        change_log_file= "/Volumes/MacintoshHD/Develop/DVDFabUSANad_Mac_Common/Fab9_Mac_Changes.txt"
        change_log = get_all_change_log(change_log_file)
    
    #TDMore Blu-ray Copy
    elif name.upper() == "TDMORE BLU-RAY COPY":
        change_log_file= "/V9_Qt/Changes_TDMore_Blu-ray_Copy.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #TDMore Blu-ray Converter
    elif name.upper() == "TDMORE BLU-RAY CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_Blu-ray_Converter.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #TDMore DVD Copy
    elif name.upper() == "TDMORE DVD COPY":
        change_log_file= "/V9_Qt/Changes_TDMore_DVD_Copy.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #TDMore Free DVD Copy
    elif name.upper() == "TDMORE FREE DVD COPY":
        change_log_file= "/V9_Qt/Changes_TDMore_Free_DVD_Copy.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #TDMore DVD Converter
    elif name.upper() == "TDMORE DVD CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_DVD_Converter.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #TDMore DVD to AVI Converter
    elif name.upper() == "TDMORE DVD TO AVI CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_DVD_to_AVI_Converter.txt"
        change_log = get_all_change_log(change_log_file) 
    
    #TDMore Video Converter
    elif name.upper() == "TDMORE VIDEO CONVERTER":
        change_log_file= "/V9_Qt/Changes_TDMore_Video_Converter.txt"
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
    if platform.upper() == "WIN":
        write_files(BRANCH_TXT, platform + "=" + project + "=" + branch)
    else:
        write_files(BRANCH_MAC_TXT, platform + "=" + project + "=" + branch)
    return HttpResponseRedirect("/index/") 
    

@csrf_exempt
def modify_branch(request):
    checkbox = request.POST.getlist("checkbox", "")
    #return HttpResponse(checkbox)
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
    #cmd_update = "/opt/local/bin/svn up " + os.path.dirname(BRANCH_TXT)
    #subprocess.call(cmd_update, stdout=subprocess.PIPE, shell=True)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return render_to_response("modify_branch.html", locals()) 
    #return HttpResponseRedirect("/index/") 


@csrf_exempt
def modify_compile(request):
    win_release_DVDFabUI = "/Volumes/MacintoshHD/auto_package/win_release_DVDFabUI.txt"
    mac_release_DVDFabQx = "/Volumes/MacintoshHD/auto_package/mac_release_DVDFabQx.txt"
    platform = request.POST.get("platform","").strip()
    build_name = request.POST.get("build_name","").strip()
    svn_uppath(os.path.splitext(win_release_DVDFabUI)[0])
    if platform.upper() == "WIN":
        if build_name.upper() == "REBUILD":
            cmdline = '"C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\Common7\\IDE\\devenv.com" "X:\\DVDFab9_Ts\\branch\\working_branch\\projects\\DVDFabQxLibs\\DVDFabQx\\DVDFabUI.vcproj" /Rebuild Release /Project DVDFabUI'
        else:
            cmdline = '"C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\Common7\\IDE\\devenv.com" "X:\\DVDFab9_Ts\\branch\\working_branch\\projects\\DVDFabQxLibs\\DVDFabQx\\DVDFabUI.vcproj" /Build Release /Project DVDFabUI'
    
        fp = open(win_release_DVDFabUI, "w")
        fp.write(cmdline)
        fp.close()
    else:
        if build_name.upper() == "REBUILD":
            cmdline = "xcodebuild -project /Volumes/X/DVDFab_slave/trunk/working_branch/goland/projects/DVDFabQxLibs/DVDFabQx/DVDFabQx.xcodeproj -target DVDFabQx clean build -configuration Release -verbose"
        else:
            cmdline = "xcodebuild -project /Volumes/X/DVDFab_slave/trunk/working_branch/goland/projects/DVDFabQxLibs/DVDFabQx/DVDFabQx.xcodeproj -target DVDFabQx  build -configuration Release -verbose"
        fp = open(mac_release_DVDFabQx, "w")
        fp.write(cmdline)
        fp.close()

    svnpath = "/opt/local/bin/svn ci  "
    svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update from 170!"'
    cmdlist = [svnpath, win_release_DVDFabUI, mac_release_DVDFabQx, svn_param]
    cmd = " ".join(cmdlist)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    return render_to_response("modify_compile.html", locals()) 
    return HttpResponseRedirect("/index/") 


@csrf_exempt
def ci_file(request):
    checkbox = request.POST.getlist("checkbox", "")
    write_file(PRODUCT_WIN_TEMP_FILE, "")
    for record in checkbox:
        write_files(PRODUCT_WIN_FILE,record)
        write_files(PRODUCT_WIN_TEMP_FILE,record)
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S")
    write_file(START_WIN_DAILY_BUILD_FILE,cur_time)
    write_file(START_MAC_DAILY_BUILD_FILE,cur_time)
    svnpath = "/opt/local/bin/svn ci  "
    svn_param = ' --username auto_builder --password dvdfab_builder --non-interactive --trust-server-cert -m  "update from 170!"'
    cmdlist = [svnpath,PRODUCT_WIN_TEMP_FILE, PRODUCT_WIN_FILE,PRODUCT_MAC_FILE,START_WIN_DAILY_BUILD_FILE, START_MAC_DAILY_BUILD_FILE, svn_param]
    cmd = " ".join(cmdlist)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return render_to_response("ci_file.html", locals())

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
