#-*- encoding:utf-8 -*-
"""
    created by
    author: dedong.xu
    date: 2016-06-29
    this script is to be used to backup database data, and joins the windows scheduled task
"""

import os
import time, datetime
import shutil
import logging


SRC_PATH = r"D:\Atlassian\Application Data\JIRA\export"
DEST_PATH = r"E:\backup_jira\backdata\export"
LOG_FILENAME = r"D:\copyfile.log"

def log(info):
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = "a", format = "%(asctime)s : %(message)s")
    logging.info(info) 

class Copy_Files(object):
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def copy_file(self, filename, dest_path):
        try:
            shutil.copy2(filename, dest_path)
            print "copy %s to %s" % (filename, dest_path)
            log("copy %s to %s" % (filename, dest_path))
        except Exception, e:
            print "copy file failed: %s" % str(e)
            log("copy file failed: %s" % str(e))

    def transform_time(self, modify_time):
        transfered_time = time.localtime(modify_time)
        year, mon, day = transfered_time.tm_year, transfered_time.tm_mon, transfered_time.tm_mday
        if mon < 10:
            str_mon = "0" + str(mon)
        else:
            str_mon = str(mon)
        if day < 10:
            str_day = "0" + str(day)
        else:
            str_day = str(day)
        format_time = "%s-%s-%s" % (str(year), str_mon, str_day)
        return format_time

    def get_file_mtime(self, filename):
        return os.stat(filename).st_mtime

        
    def get_cur_date(self):
        return time.strftime("%Y-%m-%d")

    def get_yesterday(self):
        t1 = time.localtime()#current date
        t2=datetime.datetime(t1[0],t1[1],t1[2])   
        t3=t2-datetime.timedelta(days=1)
        yesterday_date = str(t3)[:-9]
        return yesterday_date



class Main(object):
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.cf = Copy_Files(self.src_path, self.dest_path)

    def run(self):
        yesterday_date = self.cf.get_yesterday()
        log("\n")
        log("*****************************   start to backup files   *****************************")
        log("backup files' date is %s" % yesterday_date)
        for each_file in os.listdir(self.src_path):
            if each_file.startswith(yesterday_date[0:4]):
                filename = os.path.join(self.src_path, each_file)
                modify_time = self.cf.get_file_mtime(filename)
                format_time = self.cf.transform_time(modify_time)
                if format_time == yesterday_date:
                    self.cf.copy_file(filename, self.dest_path)
                    #break

if __name__ == "__main__":
    main = Main(SRC_PATH, DEST_PATH)
    main.run()








    
    
