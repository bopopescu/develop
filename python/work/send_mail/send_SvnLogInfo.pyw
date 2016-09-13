#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, mimetypes
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart  
import logging
import time
import re
import ConfigParser

CONFFIlE = os.getcwd() + '/svnloginfo_xudedong.conf'
LOG_FILENAME = os.getcwd() + '/sendmail.log'
TXTFILENAME = 'svnlog_info.txt'


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


def get_params():
    folders_list = []
    mailto_list = []
    title = ''
    filename = ''
    date = ''
    users_folders_list = []
    shared_folder = ''
    extension_name_list = []
    try:
        title = read_ini('Params', 'title')
        filename = read_ini('Params', 'filename')
        date = read_ini('Params', 'date')
        shared_folder = read_ini('Params', 'shared_folder')
        local_ip_address = read_ini('Params', 'local_ip_address')
        svn_path = read_ini('Params', 'svn_path')
        common_path = read_ini('Params', 'common_path')
        extension_name = read_ini('Params', 'extension_name')
        username = read_ini('SvnUser', 'username')
        password = read_ini('SvnUser', 'password')
        users_folders_list = read_conf('USERS_FOLDERS')
    except Exception, e:
        initlog(str(e))
    else:
        if common_path.endswith('/') or common_path.endswith('\\'):
            pass
        else:
            common_path += '/'
        for name in extension_name.split(','):
            extension_name_list.append(name.strip().upper())
        for record in users_folders_list:
            mailto_list.append(record[0])
            if ';' in record[1]:
                symbool = ';'
            else:
                symbool = ','
            for onerecord in record[1].split(symbool):
                folders_list.append(onerecord.strip())
        folders_list_set = [i for i in set(folders_list)]
        if shared_folder.endswith('/') or shared_folder.endswith('\\'):
            pass
        else:
            shared_folder += '/'
    return title, filename, date, mailto_list, users_folders_list, shared_folder, local_ip_address, svn_path, common_path, extension_name_list, username, password,folders_list_set


def set_service_mailbox():
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


def send_mail(mail_dict, title, content, mailto_one, filename):
    flag = False
    
    
    if mail_dict:
        #me = mail_dict['mail_user'] + '[' + mail_dict['mail_user'] + '@' + mail_dict['mail_postfix'] + ']'
        me = mail_dict['mail_user'] + '@' + mail_dict['mail_postfix']
        msg = MIMEMultipart()  
        msg.attach(MIMEText(content, _subtype = 'html', _charset = 'gb2312')) 
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
        except Exception as e: 
            initlog(str(e)+ '    qqqqqqqqqq')
    else:
        initlog('Server_Mails conf error!')
        
    return flag


def start_send_mail(mail_dict, title, CONTENT, mailto_one, filename):
    flag = send_mail(mail_dict, title, CONTENT, mailto_one, filename)
    if flag:
        initlog('sent to ' + mailto_one + ' successfully!')
    else:
        initlog('failed to send!')
        

def initlog(info):     
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 
	
def format_time(mytime):
    if mytime < 10:
        mytime = '0%s' % mytime
    return mytime
        

def get_date(date):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    if date == '':
        date = 0
    end = time.time() - int(date) * 3600 * 24.0
    end = time.localtime(end)
    end_hour = format_time(str(end[3]))
    end_min = format_time(str(end[4]))
    end_sec = format_time(str(end[5]))
    end_time = "%s-%s-%s %s:%s:%s" % (str(end[0]), str(end[1]), str(end[2]), end_hour, end_min, end_sec)
    return start_time, end_time  
	
def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
		
def remove_file(filename):	
    if os.path.exists(filename):
        os.remove(filename)	
		
		
def get_svn_log_cmdline(folder_full_path, start_time, end_time, user_name, pass_word, txtfile):
    if username:
		user_name = '--username ' + username
	else:
		user_name = ''
	if password:
		pass_word = ' --password ' + password
	else:
		pass_word = ''
    cmdline = 'svn log '+ folder_full_path + ' -r {"' + start_time +'"}:{"' + end_time + '"} -v ' + user_name  + pass_word + ' --stop-on-copy>' + txtfile
    return cmdline
	
def increase_file(filename, c):
    fp = open(filename, 'a')
	fp.write(c)
	fp.close()

def deal_with_file(start_time, end_time, shared_folder, local_ip_address, extension_name_list, username, password, svn_path, common_path, folders_list_set):
    CONTENT = ''
    txtfile = shared_folder + TXTFILENAME
    each_folder = time.strftime('%Y%m%d%H%M%S')
    base_path = os.path.join(shared_folder, each_folder)
    create_folder(base_path)
    for folder in folders_list_set:
        folder = folder.strip()
        initlog("begin to deal with " + folder)
        folder_full_path = os.path.join(common_path, folder)
        base_path_folder = os.path.join(base_path, folder.replace('/', '_').replace('\\', '_'))
        create_folder(base_path_folder)
        htmlfile = shared_folder + folder + '.html'
        remove_file(htmlfile)
        _list = []
        cmdline = get_svn_log_cmdline(folder_full_path, start_time, end_time, user_name, pass_word, txtfile)
        try:
            os.system(cmdline)
        except Exception, e:
            initlog(str(e))
        if os.path.exists(txtfile):
            p_0 = '[^-]+[^\n]+'
            content_0 = read_file(txtfile)
            result = re.findall(p_0, content_0)
            CONTENT = folder_full_path + '\n'
            increase_file(htmlfile, CONTENT)
            fcontent_list = read_file_lines(txtfile)
            #--------------------------------------------------------------------------------------------
            p = '^[-]+'
            for line in fcontent_list:
                if re.findall(p, line):
                    _list.append(line)
                    break
            num = 0
            #upon message
            for content in fcontent_list: 
                try:
                    index1 = fcontent_list.index(_list[0], num)
                    if index1 == len(fcontent_list) - 1:
                        break 
                    else:
                        fcontent_list[index1] = '     ' + fcontent_list[index1]
                        fcontent_list[index1 + 1] = '     ' + fcontent_list[index1 + 1]
                        fcontent_list[index1 + 2] = '     ' + fcontent_list[index1 + 2]
                        revision = fcontent_list[index1 + 1].strip().split('|')[0].strip()[1:]
                        num = index1 + 1
                except Exception, e:
                    initlog(str(e))
    
            p = 'Changed paths:'
            changed_list = []
            for line in fcontent_list:
                if re.findall(p, line):
                    changed_list.append(line)
                    break
            flag = 1
            fcontent_list_copy = fcontent_list
            if fcontent_list_copy:
                while flag:
                    if 'Changed paths' in fcontent_list_copy[-1]:
                        f_len = len(fcontent_list_copy)
                        flag = 0
                    else:
                        fcontent_list_copy = fcontent_list_copy[:-1]
                        if not fcontent_list_copy:
                            flag = 0
            else:
                initlog(folder_full_path + ' does not have svn log info!')
            #give file the full path
            count = 0
            if result:
                for content in fcontent_list:
                    try:
                        index = fcontent_list.index(changed_list[0], count)
                        revision = fcontent_list[index-1].strip().split('|')[0].strip()[1:]
                        index_1 = index + 1
                        flag = 1
                        Sum = 0
                        while flag:
                            if fcontent_list[index_1].strip("\n"):
                                fullpath_filename = os.path.join(svn_path, fcontent_list[index_1].strip().split(' ')[1])
                                fullpath = fullpath_filename.replace('/', '_').replace('\\', '_').replace(':', '_')
                                patch_file = base_path_folder + '/' + fullpath + '.' + revision + '.patch'
                                if os.path.splitext(fullpath)[1].upper()[1:] in extension_name_list:
                                    try:
                                        os.system('svn diff -r ' + str(int(revision) - 1) + ':' + revision + ' ' + fullpath_filename + '>' + patch_file)
                                    except Exception, e:
                                        initlog(str(e))
                                    else:
                                        content_lines = read_file_lines(patch_file)
                                        length = len(content_lines)
                                        Sum += length
                                        fcontent_list[index_1] = '&nbsp;&nbsp;&nbsp;'+fcontent_list[index_1].strip().split(' ')[0]+\
                                                                 ' <a href ='+'\\\\'+local_ip_address+'\\'+shared_folder.split('/')[-2]+\
                                                                 '\\'+each_folder+'\\'+patch_file.split('/')[-2]+'\\'+patch_file.split('/')[-1]+'>'+\
                                                                 fcontent_list[index_1].strip().split(' ')[1]+'</a>'+'  <span style = "color:red">patch file lines: ' + str(length) +'</span>\n'
                                else:
                                    fcontent_list[index_1] = '&nbsp;&nbsp;&nbsp;' + fcontent_list[index_1].strip().split(' ')[0] + ' <a href = ' + fullpath_filename + '>' + fcontent_list[index_1].strip().split(' ')[1] + '</a>\n'
                                index_1 += 1
                            else:
                                flag = 0
                        if Sum != 0:
                            fcontent_list[index] = "<span style = 'color:red'> Total patch file lines: " + str(Sum) + '</span><br />&nbsp;&nbsp;' + fcontent_list[index]
                        if index == f_len - 1:
                            break
                        count = index + 1
                    except Exception, e:
                        initlog(str(e))
            if result:
                fp = open(htmlfile, 'a')
                for content in fcontent_list:     
                    if content:
                        fp.write('<div style = "font-size:0.8em">&nbsp;&nbsp;' + "<b>" + content + "</b>" + '</div>') 
                fp.write('<p>&nbsp;</p>')
                fp.close()
        else:
            initlog('%s does not exists' % txtfile)
                   
            
def send_mail_to_developers(title, filename, mail_dict, mailto_list, users_folders_list, shared_folder, common_path):
    for mailto_one in mailto_list:
        for record in users_folders_list:
            if mailto_one in record:
                CONTENT = ''
                for foldername in users_folders_list[users_folders_list.index(record)][1].split(','):
                    name = foldername.replace('/', '_').replace('\\', '_').strip()
                    html_file = shared_folder + name.strip() + '.html'
                    if os.path.exists(html_file):
                        fcontent_list= read_file_lines(html_file)
                        fcontent= read_file(html_file)
                        if len(fcontent_list) <= 1:
                            CONTENT += '%s<br /><br />' % (common_path + foldername.strip())
                        else:
                            CONTENT += fcontent
                start_send_mail(mail_dict, title, CONTENT, mailto_one, filename)


def main():
    while 1:    
        send_time_list = []
        send_time = read_ini('Params', 'send_time')
        for onetime in send_time.split(','):
            send_time_list.append(onetime.strip())
        if time.strftime('%H:%M:%S') not in send_time_list:
            start=time.time()
            initlog("Start: " + str(start))
            title, filename, date, mailto_list, users_folders_list, shared_folder, local_ip_address, svn_path, common_path, extension_name_list, username, password, folders_list_set = get_params()
            start_time, end_time = get_date(date)
            initlog('start deal_with_file function')
            deal_with_file(start_time, end_time, shared_folder, local_ip_address, extension_name_list, username, password, svn_path, common_path, folders_list_set)
            
            initlog('start set_service_mailbox Function')
            mail_dict = set_service_mailbox()
            initlog('start send_mail_to_developers Function')
            send_mail_to_developers(title, filename, mail_dict, mailto_list, users_folders_list, shared_folder, common_path)
            end=time.time()
            total = end-start
            initlog("End: " + str(end))
            initlog("Total time: " + str(total) + "\n")
            time.sleep(21*3600)
                    
                              
if __name__ == '__main__': 
    main()



