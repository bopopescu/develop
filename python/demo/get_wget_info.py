#-*- encoding:utf-8 -*-

'''
Created on 2016年11月28日

@author: dedong.xu
'''

import re
import time
import os
import subprocess
import threading
import smtplib
from email.mime.text import MIMEText

URL = "http://www.dvdfab.cn/mlink/download.php?g=DVDFAB10"      #请求的地址
SLEEP_TIME = 60 * 30                                            #每一次请求的间隔，单位是秒
SAVED_FILE = "savefile.txt"                                     #分析后的结果保存的文件
FAILED_COUNTS = 3                                               #允许失败的次数
count = 0                                                       #统计失败次数

MAIL_HOST="xx.xx.x.xxx"                                         #mail server
MAIL_USER="xxxxxxxx"                                            #用户名
MAIL_PASS="xxxxxx"                                              #密码
MAIL_POSTFIX="xxxxxxxxx"                                        #邮箱后缀

MAIL_TITLE = "title"                                            #邮件标题
MAIL_CONTENT = "content"                                        #邮件正文
MAIL_LIST = ["xxxx"]                                            #收件人列表


def multi_send_mail(mail_list, sub, content):
    """ 多线程发送邮件 """
    for mail_to_one in mail_list:
        t = threading.Thread(target = send_mail, args = (mail_to_one, sub, content))
        t.start()


def send_mail(to_one,sub,content):
    """ 发邮件 """
    me="hello"+"<"+MAIL_USER+"@"+MAIL_POSTFIX+">"
    msg = MIMEText(content,_subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_one
    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        server.starttls()
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(me, to_one, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


class Wget(object):
    """ 获取wget的标准输出，并进行分析，得到想要的信息 """
    def __init__(self, url, tmpfile = "tmpfile"):
        """ 初始化变量 """
        self.url = url
        self.tmpfile = tmpfile
        
    def get_wget_output(self):
        """ 运行命令行，获取wget标准输出到文本 """
        cmd = "wget -o %s %s" % (self.tmpfile, self.url)
        subprocess.call(cmd, shell = True)
        
    def __get_file_size(self, line):
        """ 获取文件大小 """
        p = r"(\()([0-9.]+\w+)(\))"
        filesize = re.search(p, line).group(2)
        return filesize
    
    def __get_average_speed(self, line):
        """ 获取平均速度 """
        p = r"(\()([0-9.]+[A-Za-z\s\/]+)(\))"
        average_speed = re.search(p, line).group(2)
        return average_speed
        
    def parse_output(self):
        """ 解析输出内容 """
        filesize = date = average_speed = ""
        p = r"\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}"
        if os.path.exists(self.tmpfile):
            output_lines = self.__read_file_by_lines()
            for each_line in output_lines:
                date_line = re.match(p, each_line.strip())
                if each_line.strip().startswith("Length:"):
                    filesize = self.__get_file_size(each_line)
                elif date_line:
                    date = date_line.group()
                    average_speed = self.__get_average_speed(each_line)
        return filesize, date, average_speed  
    
    def __read_file_by_lines(self):
        """ 按行读取文件的所有内容 """
        with open(self.tmpfile, "r") as f:
            return f.readlines()
        
    def delete_file(self):
        """ 删除文件 """
        for each_file in os.listdir(os.getcwd()):
            if each_file.startswith("index.html"):
                filename = os.path.join(os.getcwd(), each_file)
                if os.path.isfile(filename):
                    os.remove(filename)
                

def write_file(filename, c):
    """ 写文件 """        
    with open(filename, "a") as f:
        f.write(c)
        
        
if __name__ == "__main__":
    w = Wget(URL)   
    while 1:
        w.get_wget_output() 
        filesize, date, average_speed = w.parse_output()
        print filesize, date, average_speed
        if filesize:
            write_file(SAVED_FILE, "%s, file size is :%s, average speed is: %s\n" % (date, filesize, average_speed))
            w.delete_file()
        else:
            count += 1
            if count == FAILED_COUNTS:
                multi_send_mail(MAIL_LIST, MAIL_TITLE, MAIL_CONTENT)
                count = 0
        time.sleep(SLEEP_TIME)

        