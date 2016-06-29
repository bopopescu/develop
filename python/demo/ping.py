#-*- encoding:utf-8 -*-
"""
    create by
    author: dedong.xu
    time:   2016-06-12
"""


import time
import os
import subprocess
import logging
import re

PING_COUNT = 10
COUNT = 2
SLEEP_TIME = 5
LOGPATH = os.path.join(os.getcwd(), "log")
LOGFILE = "log.txt"
web_site_list = ["www.asdfg.com", "www.dvdfab.cn", "www.baidu.com", "www.qq.com"]


def log(info):
    if not os.path.exists(LOGPATH):
        os.mkdir(LOGPATH)
    logging.basicConfig(filename = os.path.join(LOGPATH, LOGFILE), level = logging.NOTSET, filemode = "a", format = "%(asctime)s : %(message)s")
    logging.info(info)

def read_file_lines(filename):
    try:
        fp = open(filename, "r")
        all_lines = fp.readlines()
        fp.close()
    except Exception, e:
        all_lines= []
        log(str(e))
    return all_lines

def read_file(filename):
    try:
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
    except Exception, e:
        content = 0
        log(str(e))
    return content

def write_file(filename, content = "0"):
    try:
        fp = open(filename, "w")
        fp.write(content)
        fp.close()
    except Exception, e:
        log(str(e))


def ping(web_site):
    log("current web site is %s" % web_site)
    filepath = os.path.join(os.getcwd(), "ping_dir")
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filename = os.path.join(filepath, web_site)
    ping_cmd = "ping %s -c %d" % (web_site, PING_COUNT)
    try:
        os.system("%s > %s" % (ping_cmd, filename))
    except Exception, e:
        log("ping exception: " + str(e))
    log("*"*50)
    return filename


def call_php_program(web_site):
    cmd = "php /path/to/sms %s warning" % web_site
    os.system(cmd)


def bad_net_work(filename, count_filename, web_site):
    content = read_file(count_filename)
    if int(content) < COUNT - 1:
        #count file + 1
        write_file(count_filename, str(int(content) + 1))
        log("%s net work is bad!" % os.path.basename(filename))
    else:
        #call php program
        log("call php program")
        call_php_program(web_site)
        #clear count file
        write_file(count_filename)

    
def analyze_ping_result(filename, web_site):
    count_filename = os.path.join(os.path.dirname(filename), os.path.basename(filename) + "_count")
    all_lines = read_file_lines(filename)
    analyze_line = ""
    for each_line in all_lines:
        if each_line.find("packet") != -1 and each_line.find("loss") != -1 and each_line.find("%") != -1:
            analyze_line = each_line
            break

    pattern = r"\d+\%"
    search_result = re.search(pattern, analyze_line)
    if search_result:
        loss_result = search_result.group()
        log("loss result is: %s" % loss_result)
        if loss_result == "100%":
            bad_net_work(filename, count_filename, web_site)
        else:
            #clear count file
            write_file(count_filename)
            log("%s net work is ok!" % os.path.basename(filename))
    else:
        log("could not get packet loss rate")


def main():
    while 1:
        for web_site in web_site_list: 
            filename = ping(web_site)
            analyze_ping_result(filename, web_site)
        if SLEEP_TIME > 1:
            minute = "minutes"
        else:
            minute = "minute"
        log("waiting %d %s for next loop %s" % (SLEEP_TIME, minute, os.linesep))
        time.sleep(SLEEP_TIME*60)



if __name__ == "__main__":
    main()


