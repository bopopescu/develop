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
share_folder= r"d:\git_log\share_folders"
LOG_FILENAME = r"d:\git_log\src\sendmail.log"
CONFFIlE = r"d:\git_log\src\gitloginfo.conf"
SLEEP_TIME = 3600*18


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
            symbool = ';' if ';' in record[1] else ','
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
    all_branches_txt = os.path.join(share_folder, "all_branches.txt")
    cmd = "git branch -a > %s" % all_branches_txt
    subprocess.call(cmd, cwd = dest_path, shell = True)
    all_lines = read_file_lines(all_branches_txt)
    all_branches_list.append(dest_path)
    for each_line in all_lines:
        if each_line.strip().startswith("remotes/origin") and each_line.count("origin") == 1:
            branch_name = each_line.split("origin/")[1]
            all_branches_list.append(branch_name)
    return all_branches_list


def get_time():
    t1 = time.localtime()#current date
    t2=datetime.datetime(t1[0],t1[1],t1[2])   
    t3=t2-datetime.timedelta(days=2)
    t3=str(t3)[:-9]
    print t3
    return t3


def get_git_log(date_time,dest_path,branch_name):
    git_reset_cmd = "git reset --hard"
    git_checkout_cmd = "git checkout %s" % branch_name
    git_pull_cmd = "git pull"
    git_log_cmd = "git log --branches=%s --stat --since=%s>%s" %(branch_name, date_time, GIT_LOG_TXT)
    cmd_list = [git_reset_cmd, git_checkout_cmd, git_pull_cmd, git_log_cmd]
    for cmd in cmd_list:    
        subprocess.call(cmd, cwd = dest_path, shell = True)
		
		
def get_gitpath(dest_path):
    p = subprocess.Popen("git remote -v", cwd = dest_path, stdout = subprocess.PIPE, shell = True)
    all_lines = p.stdout.readlines()
    gitpath = ""
    for each_line in all_lines:
        if "(fetch)" in each_line:
            gitpath = each_line.split("(fetch)")[0].split("origin")[1].strip()
            break
    return gitpath

    
def get_cur_time_folder():
    return time.strftime("%Y%m%d%H%M%S")

	
def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
		
		
def get_diff_file(dest_path, basefilename):
    diff_filename = ""
    for roots, _, files in os.walk(dest_path):
        for onefile in files:
            filename = os.path.join(roots, onefile).replace("\\","/")
            if basefilename in filename:
                diff_filename = filename
                break
    return diff_filename

	
def get_diff_content(dest_path,commit_version, cur_time,basefilename):
    patch_path = os.path.join(share_folder, cur_time)
    create_folder(patch_path)
    final_patch_path = os.path.join(patch_path, dest_path.replace("/","_").replace("\\","_").replace(":","_"))
    create_folder(final_patch_path)
    patchfile = final_patch_path + "\\" + commit_version + "_" + cur_time + ".patch"
    if basefilename.startswith(".../"):
        basefilename = basefilename[4:].replace("\\","/").strip() 
    else:
        basefilename = basefilename.replace("\\","/").strip()
    diff_filename = get_diff_file(dest_path, basefilename)
    if diff_filename:       
        cmd = 'git diff "%s^" %s -- %s>%s' % (commit_version, commit_version, diff_filename, patchfile)
        subprocess.call(cmd, cwd = dest_path, shell = True)
    return patchfile
    
	
def clean_file(filename):
    fp = open(filename, "w")
    fp.close()
	
	
def format_git_log(date_time,cur_time,all_branches_list,extension_name_list):
    dest_path = all_branches_list[0]
    html_file_path = dest_path.replace("\\","_").replace(":","_") + ".html"
    html_file = os.path.join(share_folder, html_file_path)
    clean_file(html_file)
    
    for branch_name in all_branches_list[1:]:
		branch_name = branch_name.strip()
		get_git_log(date_time,dest_path,branch_name)
        gitpath = get_gitpath(dest_path)
		all_lines = read_file_lines(GIT_LOG_TXT)
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
                new_patchfile = "%s_%s_%s%s" % (os.path.splitext(patchfile)[0], changed_filename, branch_name, os.path.splitext(patchfile)[1])
				if os.path.exists(patchfile):
					os.rename(patchfile, new_patchfile)
				initlog(basefilename)
				initlog(patchfile)
				initlog(new_patchfile) 
				new_patchfile = new_patchfile.replace("/","\\").replace("d:", "\\\\10.10.2.201")

				if os.path.splitext(basefilename)[1].upper()[1:] in extension_name_list:
					fp.write('<div><a href = "'+ new_patchfile + '">' + each_line + "</a></div>")
				else:
					fp.write("<div>%s</div>" % each_line)
			else:
				fp.write("<div>%s</div>" % each_line)

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
        me = "%s@%s" % (mail_dict['mail_user'], mail_dict['mail_postfix'])
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
            s.connect(mail_dict['mail_host'], "25")
            s.starttls()   #启动安全传输模式
            s.login(mail_dict['mail_user'], mail_dict['mail_passwd'])
            s.sendmail(me, mailto_one, msg.as_string())
            s.close()
            flag = True
            initlog("send mail successfully")
        except Exception as e:
            initlog("send mail exception; %s" % str(e))
    else:
        initlog('Server_Mails conf error!')
    return flag


def read_file(html_file):
    fp = open(html_file,"r")
    content = fp.read()
    fp.close()
    return content
	
	
def read_file_lines(html_file):
    fp = open(html_file,"r")
    all_list = fp.readlines()
    fp.close()
    return all_list


def send_mail_to_developers(title, filename, mail_dict, mailto_list, users_folders_list):
    for mailto_one in mailto_list:
        for record in users_folders_list:
            if mailto_one in record:
                CONTENT = ''
                for foldername in users_folders_list[users_folders_list.index(record)][1].split(','):
                    name = foldername.replace('/', '_').replace('\\', '_').replace(":","_").strip() + ".html"
                    html_file = os.path.join(share_folder, name)
                    if os.path.exists(html_file):
                        fcontent_list= read_file_lines(html_file)
                        fcontent= read_file(html_file)
                        if len(fcontent_list) <= 0:
                            CONTENT += '%s<br /><br />' % fcontent
                        else:
                            CONTENT += fcontent.strip()
                send_mail(mail_dict, title, CONTENT, mailto_one, filename)


def main():
    while 1:
        send_time = read_ini("Params", "send_time")
        send_time_list = [onetime.strip() for onetime in send_time.split(",")]
        if time.strftime("%H:%M:%S") in send_time_list:
            cur_time = get_cur_time_folder()
            date_time = get_time()
            title, filename, mailto_list, users_folders_list, folders_list_set,extension_name_list = get_params()
            for each_folder in folders_list_set:
                all_branches_list = get_all_branches(each_folder)
                format_git_log(date_time,cur_time,all_branches_list,extension_name_list)
                mail_dict = get_service_mail()
            send_mail_to_developers(title, filename, mail_dict, mailto_list, users_folders_list)
            time.sleep(SLEEP_TIME)
            

if __name__ == "__main__":
    main()


    
    
