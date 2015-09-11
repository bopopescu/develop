import time, os
import codecs
import ConfigParser
import logging
import urllib2
import urllib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import send_mail

CONFFILE = "D:\\auto_report_bug\\dump.conf"
LOGNAME = "D:\\auto_report_bug\\log\\log.txt"
HTTPPOST = "http://10.10.7.105/bug/api/bug_report.php"

def log(info):
    logging.basicConfig(filename =  LOGNAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 


def read_ini(txtfile, field, key):
    cf = ConfigParser.ConfigParser()
    cf.read(txtfile)
    value = cf.get(field, key)
    return value


def record_user_info_file(SimplePath, user_info_txt):
    flag = 1
    if os.path.exists(SimplePath + "record_user_info.txt"):
        fp = open(SimplePath + "record_user_info.txt", "r")
        all_lines = fp.readlines()
        fp.close()
        if user_info_txt in [i.strip() for i in all_lines]:
            print "this user's info has been reported!"
            flag = 0
        else:
            fp = open(SimplePath + "record_user_info.txt", "a")
            fp.write(user_info_txt + "\n\r")
            fp.close()
            log("add %s into record_user_info.txt" % user_info_txt)
    else:
        fp = open(SimplePath + "record_user_info.txt", "a")
        fp.write(user_info_txt + "\n\r")
        fp.close()
        log("add %s into record_user_info.txt" % user_info_txt)


def get_user_info(DestPath, SimplePath):
    user_info = ""
    for onefile in os.listdir(DestPath):
        if os.path.splitext(onefile)[1].upper() == ".ZIP":
            onefile = onefile.replace(os.path.splitext(onefile)[1], ".txt")
            flag = record_user_info_file(SimplePath, onefile)
            if flag:
                filename = os.path.join(DestPath, onefile)
                content = read_ini(filename, "Info", "content")
                if content:
                    content += "; "
                user_info += content
                email = read_ini(filename, "Info", "email")
                if email:
                    email += "; "
                user_info += email
    return user_info


def handler():
    for filename in os.listdir(DestPath):
        if os.path.splitext(filename)[1].upper() == '.ZIP':
            filename1 = filename.replace('.', '_')
            break
    if not os.path.exists(DestPath):
        os.makedirs(DestPath)
    fp = open(DestPath + filename1 + '.txt', 'w')
    fp.write('upload ' + filename + ' failed!!!')
    fp.close()

    
def get_summary(SimplePath):  
    summary = ''
    if os.path.exists(SimplePath + 'version.txt'):
        fp = open(SimplePath + 'version.txt', 'r')
        summary = fp.read()
        summary = summary.split(' ', 1)
        fp.close()
        #log("version_txt is : %sversion.txt" % SimplePath)
    return summary


def get_description(DestPath):
    description = ""
    if os.path.exists(DestPath + "call_stack.txt"):
        fp = open(DestPath + "call_stack.txt", "r")
        description = fp.read()
        fp.close()
    return description


def http_post_report_bug(params):
    result = ""
    try:
        register_openers()          
        print params
        #datagen, headers = multipart_encode({"summary":params[0], "description":params[1], "project":params[2], "category":params[3]})
        datagen, headers = multipart_encode(params)
        # Create a Request object
        request = urllib2.Request(HTTPPOST, datagen, headers)     
        # Actually do POST request
        response = urllib2.urlopen(request)   
        result = response.read() 
        response.close()
        print result
    except Exception as e:
        print str(e)
    return result


def update_bug(DestPath,SimplePath):
    fp = open(SimplePath + "name.txt", "r")
    name = fp.read().strip()
    fp.close()
    user_info = get_user_info(DestPath, SimplePath)
    if user_info:
        send_mail.main(name, user_info)
    else:
        log("users info is empty!!")
    print "update bug"
    return 
    #fp = open(SimplePath + "bug_id.txt", "r")
    #bug_id = fp.read()
    #fp.close()
    #user_info = get_user_info(DestPath, SimplePath) 

      
def report_bug(DestPath, SimplePath):
    print "report bug"
    bug_id = ""
    fp = open(SimplePath + "name.txt", "r")
    name = fp.read().strip()
    fp.close()
    summary = get_summary(SimplePath)
    description = get_description(DestPath)
    user_info = get_user_info(DestPath, SimplePath)
    #130 means project, Function means category
    params = dict(summary=summary, description=description,project="130",category ="Function")
    #params = [summary, description, "130", "Function"]
    bug_id = http_post_report_bug(params)
    return bug_id


def write_file(filename, content):
    fp = open(filename, "w")
    fp.write(content)
    fp.close()

 
def record_bug(bug_file_path, bug_name, bug_id):
    bug_file = bug_file_path + "bug_name_id.txt"
    if os.path.exists(bug_file):
        fp = open(bug_file, "r")
        all_lines = fp.readlines()
        fp.close()
        bug_list = [i.strip() for i in all_lines]
        if (bug_name + "=" + bug_id) in bug_list:
            log("the bug has been reported!")
        else:
            fp = open(bug_file, "a")
            fp.write(bug_name + "=" + bug_id + "\n\r")
            fp.close()
            log("this is a new bug!")
    else:
        fp = open(bug_file, "a")
        fp.write(bug_name + "=" + bug_id + "\n\r")
        fp.close()
        log("this is a new bug!")
    

def main(DestPath):
    bug_id = ''
    #DestPath = read_ini(CONFFILE, 'FilePath', 'DestPath')
    SimplePath = read_ini(CONFFILE, 'FilePath', 'SimplePath')
    if DestPath.endswith("/") or DestPath.endswith("\\"):
        pass
    else:
        DestPath += "\\"
    if SimplePath.endswith("/") or SimplePath.endswith("\\"):
        pass
    else:
        SimplePath += "\\"
    if not os.path.exists(DestPath):
        os.makedirs(DestPath)
    bug_name = ''
    if os.path.exists(SimplePath + "bug_name.txt"):
        fp = open(SimplePath + "bug_name.txt", "r")
        bug_name = fp.read().strip()
        fp.close()
        #log("bug_name.txt is : %sbug_name.txt" % SimplePath)
    if bug_name:
        if os.path.exists(SimplePath + "bug_name_id.txt"):
            fp = open(SimplePath + "bug_name_id.txt", "r")
            all_lines = fp.readlines()
            fp.close()
            if bug_name in [i.strip().split("=")[0] for i in all_lines]:
                update_bug(DestPath,SimplePath)
            else:
                bug_id = report_bug(DestPath, SimplePath)
                write_file(SimplePath + "bug_id.txt", bug_id)			
                record_bug(SimplePath, bug_name, bug_id)
            #log("bug_name_id.txt is : %sbug_name_id.txt" % SimplePath)
            
        else:
            bug_id = report_bug(DestPath, SimplePath)
            write_file(SimplePath + "bug_id.txt", bug_id)			
            record_bug(SimplePath, bug_name, bug_id)
    else:
        log("No such bug: %s" % bug_name)
        print "No such bug!"

        
if __name__ == '__main__':    
    main()


    




