#-*- encoding:utf-8 -*-

'''
Created on 2016-12-13

@author: dedong.xu

@description: 按照规范的格式生成一个info.log文件，然后将所有的log打包成zip包发送到log系统。
'''

#standard lib
import os
import socket
import uuid
import time
import pprint
import zipfile
import urllib2
import json
import sys

#3rd lib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers 

#local lib
from settings import LOG_PATH_IN_BOX, LOG_PATH, INFO_FILE, POSTFIX_ZIPFILENAME, HTTP_URL, EXTEND_NAME




class Format_Log(object):
    """ 组织log内容的格式并写入到log文件 """
    def __init__(self, log_path, info_file):
        """ 初始化变量 """
        self.__total_dict = {}
        self.log_path = log_path
        self.info_file = os.path.join(self.log_path, "%s-%s") % (self.get_logfile_prefix(), info_file)
        

    def get_logfile_dict(self, info_file, extend_name):
        """ 获取log文件列表 """
        logfile_dict = {}
        file_list = [each_file for each_file in os.listdir(self.log_path) if each_file.startswith(self.get_logfile_prefix()) and each_file.endswith(extend_name)]
        cur_info_file = "%s-%s" % (self.get_logfile_prefix(), info_file)
        if cur_info_file not in file_list:
            file_list.append(cur_info_file)
        for i in xrange(len(file_list)):
            logfile_dict[str(i)] = file_list[i]
        return logfile_dict
        
    def get_ip(self):
        """ 获取本机的IP """
        return socket.gethostbyname(socket.gethostname())
    
    def get_mac_address(self):
        """ 获取本机mac地址 """
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
        return "-".join([mac[e:e+2] for e in range(0,11,2)])
    
    def get_logfile_prefix(self):
        """ 获取当前的日期作为log文件的前缀 """
        return time.strftime("%Y%m%d")
    
    def get_cur_date(self):
        """ 获取当前的日期 """
        return time.strftime("%Y-%m-%d")
    
    def get_platform_name(self):
        """ 获取操作系统名称 """
        if os.name == "nt":
            platform_name = "Windows"
        elif os.name == "posix":
            platform_name = "Ubuntu"
        else:
            platform_name = ""
        return platform_name
    
    def write_file(self, filename, c):
        """ 写文件 """
        with open(filename, "w") as f:
            f.write(c)
    
    def get_log_content(self, info_file, extend_name):
        """ 组织log内容 """
        product_dict = {"name":"", "os": self.get_platform_name()}
        self.__total_dict["version"] = ""
        self.__total_dict["time"] = self.get_cur_date()
        self.__total_dict["ip"] = self.get_ip()
        self.__total_dict["mac"] = self.get_mac_address()
        self.__total_dict["product"] = product_dict
        self.__total_dict["filelist"] = self.get_logfile_dict(info_file, extend_name)
        #pprint.pprint(self.total_dict)
        return pprint.pformat(self.__total_dict)
    
    def main(self, info_file, extend_name):
        """ 将log内容写入log文件 """
        log_content = self.get_log_content(info_file, extend_name)
        print 111111111111, log_content
        self.write_file(self.info_file, log_content)
        

class ZipFile(object):
    """ 压缩文件,压缩后的文件名字前缀是当前的日期，后缀则由传递的参数决定  """   
    def __init__(self, log_path, postfix_zipfilename, mode = "w"):
        """ 初始化变量 """
        self.log_path = log_path
        self.zipfilename = os.path.join(self.log_path, "%s-%s") % (self.get_logfile_prefix(), postfix_zipfilename)
        self.mode = mode
        self.zf = zipfile.ZipFile(self.zipfilename, self.mode, compression = zipfile.zlib.DEFLATED)
        
    def get_logfile_prefix(self):
        """ 获取当前的日期作为log文件的前缀 """
        return time.strftime("%Y%m%d")
    
    def zipfile(self, filename):
        """ 将文件写入到压缩包里，其中第一个参数代表要压缩的文件，第二个参数代表压缩到压缩包里的文件名称"""
        self.zf.write(filename, os.path.split(filename)[1], zipfile.ZIP_DEFLATED)    
    
    def close(self):
        """ 关闭打开的文件对象 """
        self.zf.close()        
       

def post_file(url, params):
    """ 模拟HTTP POST请求上传文件 """
    try:
        register_openers()          
        datagen, headers = multipart_encode(params)
        # Create a Request object
        request = urllib2.Request(url, datagen, headers)    
        # Actually do POST request
        response = urllib2.urlopen(request)
        result = response.read() 
        response.close()   
        print json.loads(result)["result"]
        return json.loads(result)["result"]
    except Exception, e:
        print str(e)
        return 0
    
    
def main(log_path, info_file, postfix_zipfilename, http_url, extend_name):
    fl = Format_Log(log_path, info_file)
    fl.main(info_file, extend_name)
    logfile_set = set([os.path.join(log_path, each_file) for each_file in fl.get_logfile_dict(info_file, extend_name).values()])
    logfile_set.add(fl.info_file) 
    zf = ZipFile(log_path, postfix_zipfilename)
    print logfile_set
    for logfile in logfile_set:
        zf.zipfile(logfile)
    zf.close()
    params = {"file": open(zf.zipfilename, "rb")}
    print http_url
    post_flag = post_file(http_url, params)  
    if post_flag == 1:
        print "POST success!!!"
        sys.exit(0)
    else:
        print "POST failed!!!"
        sys.exit(1)
    return

    
if __name__ == "__main__":
    main(LOG_PATH, INFO_FILE, POSTFIX_ZIPFILENAME, HTTP_URL, EXTEND_NAME)

    
    
    