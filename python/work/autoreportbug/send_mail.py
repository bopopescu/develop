#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2013-2-2
@author: dedong.xu
'''
import os, mimetypes
import smtplib
#import threading
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart  
import logging
import json
import ConfigParser


LOG_FILENAME = os.getcwd() + '/log/log.txt'
CONFFILE = os.getcwd() + '/send_mail.conf'
    
def read_ini(field, key):
    cf = ConfigParser.ConfigParser()
    cf.read(CONFFILE)
    value = cf.get(field, key)
    return value


def read_conf(field):
    cf = ConfigParser.ConfigParser()
    cf.read(CONFFILE)
    value = cf.items(field)
    return value


def get_params():
    TITLE = ""
    USERNAME_DICT = ""
    try:
        TITLE = read_ini('Params', 'TITLE')
        Default_Recipient = read_ini('Params', 'Default_Recipient')
        Recipients = read_conf("Recipients")
    except Exception, e:
        initlog(str(e))
    return TITLE, Default_Recipient, Recipients


def set_service_mailbox():   
    mail_host = read_ini('Mails', 'mail_host')
    mail_user = read_ini('Mails', 'mail_user')
    mail_passwd = read_ini('Mails', 'mail_passwd')
    mail_postfix = read_ini('Mails', 'mail_postfix')  
    mail_dict = {'mail_host':mail_host, 'mail_user':mail_user, 'mail_passwd':mail_passwd, 'mail_postfix':mail_postfix}
    return mail_dict


def send_mail(mail_dict, title, content, mailto_one):
    flag = False
    me = mail_dict['mail_user'] + '@' + mail_dict['mail_postfix']
    msg = MIMEMultipart()  
    msg.attach(MIMEText(content))
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = mailto_one
    ctype, encoding = mimetypes.guess_type(content)                                                                           
            
    try:
        s = smtplib.SMTP()
        s.connect(mail_dict['mail_host'])
        s.login(mail_dict['mail_user'], mail_dict['mail_passwd'])
        s.sendmail(me, mailto_one, msg.as_string())
        s.close()
        flag = True
    except Exception, e: 
        initlog(str(e))
    finally:
        return flag


def start_send_mail(mail_dict, TITLE, CONTENT, mailto_one):
    flag = send_mail(mail_dict, TITLE, CONTENT, mailto_one)
    if flag:
        initlog('sent mail to ' + mailto_one + ' successfully!')
    else:
        initlog('failed to send mail to ' + mailto_one + '!')
        


def initlog(info):     
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info)


def get_mail_recipient(name,Default_Recipient, Recipients):
    mailto_one = ""
    for record in Recipients:
        if name in record:
            mailto_one = record[1]
            break
    if not mailto_one:
        mailto_one = Default_Recipient
        print Default_Recipient
    return mailto_one


def main(name, content):
    TITLE, Default_Recipient, Recipients = get_params()
    mailto_one = get_mail_recipient(name,Default_Recipient, Recipients)
    mail_dict = set_service_mailbox()
    start_send_mail(mail_dict, TITLE, content, mailto_one)


if __name__ == '__main__':
    main(name, content)
    initlog('ok, this is end!\n')

