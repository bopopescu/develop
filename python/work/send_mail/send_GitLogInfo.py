#-*- encoding:utf-8 -*-

import os,mimetypes
import time
import datetime
import logging
import subprocess
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


GIT_LOG_TXT = r"d:\git_log\share_folders\git_log.txt"
share_folder= "d:/git_log/share_folders/"
LOG_FILENAME = r"d:\git_log\src\sendmail.log"
CONFFIlE = r"d:\git_log\src\gitloginfo.conf"


def initlog(info):     
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info)


def read_ini(field, key):
    cf = ConfigParser.ConfigParser()
    cf.read(CONFFIlE)
    value = cf.get(field, key)
    return value


def read_conf(field):
    cf = ConfigParser.ConfigParser()
    cf.read(CONFFIlE)
    value = cf.items(field)
    return value
	

def get_params():
    title = ""
    filename = ""
    gitpath_dict = ""
    folders_list = []
    mailto_list = []
    users_folders_list = []
    extension_name_list = []
    try:
        title = read_ini("Params","title")
        filename = read_ini("Params","filename")
        users_folders_list = read_conf('USERS_FOLDERS')
        extension_name = read_ini("Params","extension_name")
        print users_folders_list
    except Exception, e:
        initlog(str(e))
    else:
        for record in users_folders_list:
            mailto_list.append(record[0])
            if ';' in record[1]:
                symbool = ';'
            else:
                symbool = ','
            for onerecord in record[1].split(symbool):
                folders_list.append(onerecord.strip())
        folders_list_set = [i for i in set(folders_list)]
        for name in extension_name.split(","):
            extension_name_list.append(name.strip().upper())
        
    return title, filename, mailto_list, users_folders_list, folders_list_set,extension_name_list


def get_service_mail():
    mail_dict = {}
    try:
        mail_host = read_ini('Server_Mails', 'mail_host')
        mail_user = read_ini('Server_Mails', 'mail_user')
        mail_passwd = read_ini('Server_Mails', 'mail_passwd')
        mail_postfix = read_ini('Server_Mails', 'mail_postfix')                 
        mail_dict = {'mail_host':mail_host, 'mail_user':mail_user, 'mail_passwd':mail_passwd, 'mail_postfix':mail_postfix}
    except Exception as e:
        initlog(str(e))
    return mail_dict


def get_all_branches(dest_path):
    all_branches_list = []
    all_branches_txt = share_folder + "all_branches.txt"
    cmd = "git branch -a > " + all_branches_txt
    subprocess.call(cmd, cwd = dest_path, shell = True)
    fp = open(all_branches_txt, "r")
    all_lines = fp.readlines()
    fp.close()
    all_branches_list.append(dest_path)
    for each_line in all_lines:
        if each_line.strip().startswith("remotes/origin") and each_line.count("origin") == 1:
            branch_name = each_line.split("origin/")[1]
            all_branches_list.append(branch_name)
    print "all_branches_list: ", all_branches_list
    return all_branches_list


def get_time():
    t1 = time.localtime()#current date
    t2=datetime.datetime(t1[0],t1[1],t1[2])   
    t3=t2-datetime.timedelta(days=2)
    t3=str(t3)[:-9]
    print t3
    return t3


def get_git_log(date_time,dest_path,branch_name):
    git_pull_cmd = "git pull"
    subprocess.call(git_pull_cmd, cwd = dest_path, shell = True)
    git_checkout_cmd = "git checkout " + branch_name
    subprocess.call(git_checkout_cmd, cwd = dest_path, shell = True)
    subprocess.call(git_pull_cmd, cwd = dest_path, shell = True)
    git_log_cmd = "git log --branches=" + branch_name + " --stat --since=" + date_time + '>' + GIT_LOG_TXT
    #print git_log_cmd,"*****************************************************"
    subprocess.call(git_log_cmd, cwd = dest_path, shell = True)
    p = subprocess.Popen("git remote -v", cwd = dest_path, shell = True, stdout = subprocess.PIPE)
    all_lines = p.stdout.readlines()
    gitpath = ""
    for each_line in all_lines:
        if "(fetch)" in each_line:
            print each_line
            gitpath = each_line.split("(fetch)")[0].strip().split(" ")[-1]
            gitpath = each_line.split("(fetch)")[0].split("origin")[1].strip()
            print gitpath
    return gitpath

    
def get_cur_time_folder():
    cur_time = time.strftime("%Y%m%d%H%M%S")
    return cur_time


def get_diff_content(dest_path,commit_version, cur_time,basefilename):
    patch_path = os.path.join(share_folder, cur_time)
    if not os.path.exists(patch_path):
        os.mkdir(patch_path)
    final_patch_path = os.path.join(patch_path, dest_path.replace("/","_").replace("\\","_").replace(":","_"))
    if not os.path.exists(final_patch_path):
        os.mkdir(final_patch_path)
    patchfile = final_patch_path + "\\" + commit_version + "_" + cur_time + ".patch"
    
    diff_filename = ""
    if basefilename.startswith(".../"):
        basefilename = basefilename[4:].replace("\\","/").strip()
        print basefilename,111111111111111111111111
    else:
        basefilename = basefilename.replace("\\","/").strip()
        
    for roots, dirs, files in os.walk(dest_path):
        for onefile in files:
            filename = os.path.join(roots, onefile).replace("\\","/")

            if basefilename in filename:
                diff_filename = filename
                print "filename: ", filename
                print "basefilename:", basefilename
                break
    if diff_filename:       
        cmd = "git diff " + '"' + commit_version + '^" ' + commit_version + " -- " + diff_filename + ">" + patchfile
        subprocess.call(cmd, cwd = dest_path, shell = True)
    else:
        print "***************************************************************"

    return patchfile
    

def format_git_log(date_time,cur_time,all_branches_list,extension_name_list):
    dest_path = all_branches_list[0]
    html_file_path = dest_path.replace("\\","_").replace(":","_")
    #os.path.join(dest_path, )
    html_file = share_folder + html_file_path + ".html"
    fp = open(html_file, "w")
    fp.close()
    
    for branch_name in all_branches_list[1:]:
            branch_name = branch_name.strip()
            gitpath = get_git_log(date_time,dest_path,branch_name)
            fp = open(GIT_LOG_TXT, "r")
            all_lines = fp.readlines()
            fp.close()

            fp = open(html_file, "a+")
            fp.write("<div style = 'font-size:1.5em'><br /><div>--------------------------------------------------------------------------------------</div><strong>" + gitpath + "</strong></div>")   
            fp.write("<div style = 'font-size:1.5em'><strong>" + branch_name + "</strong></div>")
            for each_line in all_lines:
                if each_line.startswith("commit"):
                    commit_version = each_line.split(" ")[1].strip()
                    fp.write("<div><br /></div><div><span style = 'color:red'>" + each_line.split(" ")[0] + ":</span> " + each_line.split(" ")[1] + "</div>")    
                elif  each_line.startswith("Author:"):
                    fp.write("<div><span style = 'color:red'>Author:</span> " + each_line.replace("Author:","") + "</div>")
                elif each_line.startswith("Date:"):
                    fp.write("<div><span style = 'color:red'>Date:</span> " + each_line.replace("Date:","") + "</div>")
                elif "|" in each_line and "/" in each_line:
                    basefilename = each_line.split("|")[0].strip()
                    patchfile = get_diff_content(dest_path,commit_version, cur_time,basefilename)
                    print "patchfile: ", patchfile
                    
                    changed_filename = basefilename.replace("/","_").replace("\\","_").replace(".","_").replace('"',"_")
                    new_patchfile = os.path.splitext(patchfile)[0] + "_" + changed_filename + "_" + branch_name + os.path.splitext(patchfile)[1]
                    if os.path.exists(patchfile):
                        os.rename(patchfile, new_patchfile)
                    initlog(basefilename)
                    initlog(patchfile)
                    initlog(new_patchfile) 
                    new_patchfile = new_patchfile.replace("/","\\").replace("d:", "\\\\10.10.2.201")

                    if os.path.splitext(basefilename)[1].upper()[1:] in extension_name_list:
                        fp.write('<div><a href = "'+ new_patchfile + '">' + each_line + "</a></div>")
                    else:
                        fp.write("<div>"+ each_line + "</div>")
                else:
                    fp.write("<div>" + each_line + "</div>")

                if each_line.startswith("Date:"):
                    date_index = all_lines.index(each_line)
                    flag = 1
                    while flag:
                        all_lines[date_index + 2] = "<span style = 'color:red'>Message: </span>" + all_lines[date_index + 2]#.decode("gb2312").encode("utf-8")
                        
                        if date_index + 3 > len(all_lines) -1  or all_lines[date_index + 3].strip() == "":
                            flag = 0
                        else:
                            date_index += 1
                            flag = 1
            fp.close()


def send_mail(mail_dict, title, content, mailto_one, filename = ""):
    flag = False    
    if mail_dict:
        me = mail_dict['mail_user'] + '@' + mail_dict['mail_postfix']
        msg = MIMEMultipart()  
        msg.attach(MIMEText(content, _subtype = 'html', _charset = 'utf-8')) 
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = mailto_one
        if filename != None and os.path.exists(filename):  
            ctype, encoding = mimetypes.guess_type(filename)                                                   
            if ctype is None or encoding is not None:                                             
                ctype = "application/octet-stream"                                                       
            _, subtype = ctype.split("/")  
            pf = open(filename, 'rb')
            file_content = pf.read()
            pf.close()
            attachment = MIMEImage(file_content, _subtype = subtype)                                          
            attachment.add_header("Content-Disposition", "attachment", filename = filename)                    
            msg.attach(attachment)
            
        try:
            s = smtplib.SMTP()
            initlog("1111111111111111")
            s.connect(mail_dict['mail_host'], "25")
            initlog("2222222222222222")
            s.starttls()   #启动安全传输模式
            s.login(mail_dict['mail_user'], mail_dict['mail_passwd'])
            initlog("3333333333333333")
            s.sendmail(me, mailto_one, msg.as_string())
            initlog("4444444444444444")
            s.close()
            initlog("5555555555555555")
            flag = True
            initlog("send mail successfully")
        except Exception as e:
            initlog(str(e)+ '    qqqqqqqqqq')
    else:
        initlog('Server_Mails conf error!')
        
    return flag

def start_send_mail(mail_dict, title, content, mailto_one, filename):
    flag = send_mail(mail_dict, title, content, mailto_one, filename)
    if flag:
        initlog('sent to ' + mailto_one + ' successfully!')
    else:
        initlog('failed to send!')
        

def read_file(html_file):
    fp = open(html_file,"r")
    content = fp.read()
    fp.close()
    return content


def send_mail_to_developers(title, filename, mail_dict, mailto_list, users_folders_list):
    for mailto_one in mailto_list:
        for record in users_folders_list:
            if mailto_one in record:
                CONTENT = ''
                for foldername in users_folders_list[users_folders_list.index(record)][1].split(','):
                    if '/' in foldername:
                        name = foldername.replace('/', '_')
                    elif '\\' in foldername:
                        name = foldername.replace('\\', '_')
                    else:
                        name = foldername
                    html_file = share_folder + name.replace("\\","_").replace("/","_").replace(":","_").strip() + '.html'
                    print "html_file is: ", html_file
                    if os.path.exists(html_file):
                        fp = open(html_file, 'r')
                        fcontent_list= fp.readlines()
                        fp.close()
                        fp = open(html_file, 'r')
                        fcontent= fp.read()
                        fp.close()
                        if len(fcontent_list) <= 0:
                            CONTENT += '%s<br /><br />'%fcontent
                        else:
                            CONTENT += fcontent.strip()
                start_send_mail(mail_dict, title, CONTENT, mailto_one, filename)



def main():
    while 1:
        send_time_list = []
        send_time = read_ini("Params", "send_time")
        for onetime in send_time.split(","):
            send_time_list.append(onetime.strip())
          
        if time.strftime("%H:%M:%S") in send_time_list:
            cur_time = get_cur_time_folder()
            date_time = get_time()
            title, filename, mailto_list, users_folders_list, folders_list_set,extension_name_list = get_params()
            for each_folder in folders_list_set:
                all_branches_list = get_all_branches(each_folder)
                format_git_log(date_time,cur_time,all_branches_list,extension_name_list)
                mail_dict = get_service_mail()
            send_mail_to_developers(title, filename, mail_dict, mailto_list, users_folders_list)
            time.sleep(3600*18)
            #break
            

if __name__ == "__main__":
    main()


    
    
