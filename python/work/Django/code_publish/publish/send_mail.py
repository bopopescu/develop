#-*- coding:utf-8 -*-
'''
Created on 2017-06-02

@author: dedong.xu
'''

import os
import smtplib
import threading
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart  


def set_service_mailbox(): 
    """ 设置邮箱服务器信息 """
    mail_dict = {}
    mail_dict["mail_host"] = "10.10.7.100"         #connect server
    mail_dict["mail_user"] = "buildbot"            #user
    mail_dict["mail_passwd"] = "123456"            #passwd 
    mail_dict["mail_postfix"] = "goland.cn"        #user postfix
    return mail_dict

def multi_send_mail(mail_host, mail_user, mail_passwd, mail_postfix, title, content, mail_list, filename):
    """ 多线程发送 """
    for mailto_one in mail_list:
        t = threading.Thread(target = send_mail, args = (mail_host, mail_user, mail_passwd, mail_postfix, title, content, mailto_one, filename))
        t.start()

def read_file(filename):
    """ 写文件	"""
    with open(filename, "rb") as f:
        return f.read()
		
def send_mail(mail_host, mail_user, mail_passwd, mail_postfix, title, content, mailto_one, filename = None):
    """ 发邮件 """
    me = "%s<%s@%s>" % (mail_user, mail_user, mail_postfix)
    msg = MIMEMultipart()  
    msg.attach(MIMEText(content)) 
    msg["Subject"] = title
    msg["From"] = me
    msg["To"] = mailto_one
    if filename != None and os.path.exists(filename):  
        ctype, encoding = mimetypes.guess_type(filename)    #check file's type
        if ctype is None or encoding is not None:           #.rar file
            ctype = "application/octet-stream"              #ya suo bao
        _, subtype = ctype.split("/")  
        attachment = MIMEImage(read_file(filename), _subtype = subtype)         #guess image MIME subtype
        attachment.add_header("Content-Disposition", "attachment", filename = os.path.basename(filename))     #Content-Disposition can set file type
        msg.attach(attachment)             #tian jia fu jian   
    try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.starttls()   #启动安全传输模式
		s.login(mail_user,mail_passwd)
		s.sendmail(me,mailto_one,msg.as_string())
		s.close()
		print "sent successfully!"
    except Exception, e:
        print str(e)
        return


def main(title, content, mail_list, filename = None):
    mail_dict = set_service_mailbox()
    mail_host = mail_dict["mail_host"]
    mail_user = mail_dict["mail_user"]
    mail_passwd = mail_dict["mail_passwd"]
    mail_postfix = mail_dict["mail_postfix"]
    multi_send_mail(mail_host, mail_user, mail_passwd, mail_postfix, title, content, mail_list, filename)


if __name__ == "__main__":
    main(TITLE, CONTENT, MAIL_LIST, FILENAME)
    

