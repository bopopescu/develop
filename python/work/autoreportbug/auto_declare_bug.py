#-*- enocding:utf-8 -*-
#!/usr/bin/env python
import os
import string
import time
import subprocess
import shutil
from shutil import Error
from shutil import copystat
from shutil import copy2
import GetDVDFabDump 
import ConfigParser
import urllib2, cookielib, urllib, re
import auto_report_bug

CONFFILE = os.getcwd() + "\\dump.conf"

def read_ini(field, key):
    cf = ConfigParser.ConfigParser()
    cf.read(CONFFILE)
    value = cf.get(field, key)
    return value

def find_pdbfile(pdb_path, version):  
    full_pdb_path = ''
    pdb_list = []
    ctime_list = []
    if os.path.exists(pdb_path + '\\' + version):
        full_pdb_path = pdb_path + '\\' + version
        for all_roots, _, all_files in os.walk(full_pdb_path):
            for onefile in all_files:
                filename = os.path.join(all_roots, onefile)
                if filename.endswith(".pdb"):
                    ctime = time.mktime(time.localtime(os.stat(filename).st_mtime))
                    pdb_list.append(filename)
                    ctime_list.append(ctime)
        if ctime_list:
            max_time = max(ctime_list)
            full_pdb_path = pdb_list[ctime_list.index(max_time)].replace(os.path.basename(pdb_list[ctime_list.index(max_time)]), "")
        else:
            GetDVDFabDump.log("Sorry, no DVDFab.pdb file!!!")
    else:
        GetDVDFabDump.log('pdb_path does not exist!!')
    return full_pdb_path

def copy_exe_pdb_to_localpath(version, pdb_file_path):
    for onefile in os.listdir(pdb_file_path):
        filename = os.path.join(pdb_file_path, onefile)
        try:
            exe_pdb_destpath = read_ini("FilePath", "EXE_PDB_DESTPATH")
            copy_file(filename, exe_pdb_destpath)
            if filename.endswith(".exe"):
                shutil.copy2(filename, exe_pdb_destpath + "\\Fab.exe")
                shutil.copy2(filename, exe_pdb_destpath + "\\DVDFab.exe")
            if filename.endswith(".pdb"):
                shutil.copy2(filename, exe_pdb_destpath + "\\Fab.pdb")
                shutil.copy2(filename, exe_pdb_destpath + "\\DVDFab.pdb")
            GetDVDFabDump.log("success to copy %s" % filename)
        except Exception, e:
            GetDVDFabDump.log("failed to copy " + filename + "; " + str(e))
		
def call_DumpAnalyze(DumpAnalyze_path, zip_file_path, s_version):
    zip_path = zip_file_path.replace(os.path.basename(zip_file_path), "")
    cmd_string = DumpAnalyze_path + " "  + zip_path + " " + zip_path + " " + s_version
    GetDVDFabDump.log("cmd_string: " + cmd_string)
    try:
        os.system(cmd_string)
        GetDVDFabDump.log('success to call ZipTypeAnalyze.exe')      
    except Exception, e:
        print str(e)
        GetDVDFabDump.log('failed to call ZipTypeAnalyze.exe' + str(e))

def copy_file(src_file, dest_path):  
    if os.path.isfile(src_file): 
        if os.path.isdir(dest_path):      
            pass
        else:
            os.makedirs(dest_path)
        errors = []                             
        srcname = src_file    
        filename = os.path.basename(src_file)
        dstname = os.path.join(dest_path, filename)   
        try:                                
            if os.path.isfile(srcname):        
                copy2(srcname, dstname) 
            elif os.path.isdir(dstname):          
                os.remove(dstname)
                copy2(srcname, dstname)       
        except Exception, e:
            result = 'failed to copy %s' % src_file
            GetDVDFabDump.log(result + str(e))
            
        try:                               
            copystat(srcname, dstname)           
        except Exception, e:
            result = 'failed to copystat %s' % src_file
            GetDVDFabDump.log(result + str(e))
        if errors:                          
            raise Error(errors)             

def check_call_stack_content(name_path):
    content = ''
    call_stack = os.path.join(name_path, 'call_stack.txt')
    if os.path.exists(call_stack):
        fp = open(call_stack, 'r')
        content = fp.read()
        fp.close()
    return content


def delete_file(dest_path):
    if os.path.exists(dest_path):
        for filename in os.listdir(dest_path):
            file_path = os.path.join(dest_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception, e:
                    GetDVDFabDump.log('failed to remove ' + file_path + '; ' + str(e))
            else:
                GetDVDFabDump.log("%s is not file!" % file_path)
    else:
        GetDVDFabDump.log("%s does not exist!" % dest_path)
          
def check_process_exists(process_name):
    returncode = ''   
    try:
        p = os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name) 
        returncode = p.read().count(process_name)   
    except Exception, e:
        GetDVDFabDump.log(str(e))
    else:
        if returncode:
            GetDVDFabDump.log(process_name + ' exists')    
    return returncode
        
def kill_process(process_name):
    try: 
        os.system('taskkill /f /im ' + process_name) 
        GetDVDFabDump.log('%s is killed now' % process_name) 		
    except Exception, e:
        GetDVDFabDump.log('failed to kill process; ' + str(e))         
        
			
def write_file(filename, content, mode = "w"):
    fp = open(filename, mode)
    fp.write(content)
    fp.close()
 
def get_analyzed_zip_file(zip_file_path):
    zip_filename = ""
    bugname_username = ""
    bug_name = ""
    username = ""
    name_path = ""
    zipfile_list = []
    filename = os.path.basename(zip_file_path)
    zip_path = zip_file_path.replace(filename, "")
    for all_roots, _, all_files in os.walk(zip_path):
        for onefile in all_files:
            if onefile == filename:
                zip_filename = os.path.join(all_roots, onefile).replace("/", "\\")
                bugname_username =  zip_filename.split("\\")[-2]
                bug_name = string.join(bugname_username.split("_")[2:-1], "_")
                username = bugname_username.split("_")[-1]
                name_path = string.join(zip_filename.split("\\")[:-1], "\\")
                break
    for onefile in os.listdir(zip_filename.replace(os.path.basename(zip_filename), "")):
        if os.path.splitext(onefile)[1].upper() == ".ZIP":
            zipfile_list.append(file)

    zipfile_number = len(zipfile_list)
    return zip_filename, bug_name, username, name_path, zipfile_number


def check_version_1(version):
    flag = False
    GetDVDFabDump.VERSION_LIST.append(version)
    if len(GetDVDFabDump.VERSION_LIST) < 2:
        flag = True
    else:
        if GetDVDFabDump.VERSION_LIST[-1] == GetDVDFabDump.VERSION_LIST[-2]:
            GetDVDFabDump.VERSION_LIST = [i for i in set(GetDVDFabDump.VERSION_LIST)]
        else:
            GetDVDFabDump.VERSION_LIST = GetDVDFabDump.VERSION_LIST[-1:]
            flag = True
    return flag      
  
def check_version(version):
    flag = False
    if GetDVDFabDump.ZIP_VERSION == "":
        GetDVDFabDump.ZIP_VERSION = version
        flag = True
    else:
        if GetDVDFabDump.ZIP_VERSION != version:
            GetDVDFabDump.ZIP_VERSION = version
            flag = True
        GetDVDFabDump.log("check_version , %s" % flag)
    return flag

def get_bug_id():
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    postdata=urllib.urlencode({
        "return":"index.php",
        'username':'Crashrpt ',
        'password':'crash',
        "secure_session":"on"
    })

    headers = {
        "Host":"10.10.7.150",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"
    }

    req = urllib2.Request(
        url = 'http://10.10.7.150/bug/login.php',
        data = postdata,
        headers = headers)

    content = urllib2.urlopen(req).read()
    data = content.split("Reported by Me")[1]
    pattern = ">\d+<"
    bug_id = re.findall(pattern, data)[0][1:-1]
    bug_id = str(int(bug_id))
    GetDVDFabDump.log("successfully use spider to get bug_id,  it is %s" % bug_id)
    return bug_id
	
def read_file_lines(filename):
    fp = open(filename, "r")
    all_lines = fp.readlines()
    fp.close()
    return all_lines
	
	
def record_bug(bug_file_path, bug_name, bug_id):
    bug_file = bug_file_path + "bug_name_id.txt"
    if os.path.exists(bug_file):
        all_lines = read_file_lines(bug_file)
        bug_list = [i.strip() for i in all_lines]
        if (bug_name + "=" + bug_id) in bug_list:
            GetDVDFabDump.log("the bug has been reported!")
        else:
            write_file(bug_file, bug_name + "=" + bug_id + "\n\r", mode = "a")
            GetDVDFabDump.log("this is a new bug!")
    else:
        write_file(bug_file, bug_name + "=" + bug_id + "\n\r", mode = "a")
        GetDVDFabDump.log("this is a new bug!")
		
def changepath(path):
    if not (path.endswith("/") or path.endswith("\\")):
        path += "/" 
    return path
	
def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
def main(version, zip_file_path, DumpAnalyze_path, PdbPath):  
    SimplePath = read_ini("FilePath", "SimplePath")  
    create_folder(SimplePath)
    SimplePath = changepath(SimplePath)
    pdb_file_path = find_pdbfile(PdbPath, version)
    flag = check_version(version)
    if flag:
        copy_exe_pdb_to_localpath(version, pdb_file_path)
        GetDVDFabDump.log("success to copy exe and pdb!!, version is %s!" % version)
    else:
        GetDVDFabDump.log("zip file version does not change, still %s!!" % version)
    #delete_file(DestPath)
    call_DumpAnalyze(DumpAnalyze_path, zip_file_path, version)
    time.sleep(5)
    zip_filename, bug_name, username, name_path, zipfile_number = get_analyzed_zip_file(zip_file_path)
    write_file(SimplePath + "bug_name.txt", bug_name)
    standrad_zipfile_number  = read_ini("FilePath","standrad_zipfile_number")
    if int(zipfile_number) >= int(standrad_zipfile_number):
        GetDVDFabDump.log("%s zipfile number is %s, equal to %s or bigger than %s!" % (bug_name,zipfile_number,standrad_zipfile_number,standrad_zipfile_number ))
        write_file(SimplePath + "name.txt", username)
        content = check_call_stack_content(name_path)
        if content:
            print "call_stack.txt is not empty, could report bug"
            #auto_report_bug.main(name_path)
        else:
            GetDVDFabDump.log('call_stack.txt does not have anything!!')
    else:
        GetDVDFabDump.log("%s zipfile number is %s, less than %s!" % (bug_name, zipfile_number, standrad_zipfile_number )) 


if  __name__ == "__main__":
    main("9138", r"\\10.10.2.72\nas\DVDFab_Dump\DVDFab\20140408\9138\209588c680864bfa1d68f4fdb245d577.zip", "D:\auto_report_bug\ZipTypeAnalyze.exe", r"\\10.10.2.72\nas\DVDFab_Dump\BluFab\___DVDFab9")

    
