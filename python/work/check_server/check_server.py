#-*- encoding:utf-8 -*-
'''
Created on 2016-08-04

@author: dedong.xu
@description: 该程序的作用是定期检查当前的server ip是否被封。
'''
#standard lib
import subprocess
import json
import urllib2
import time

#3rd lib
import pycurl

allnode_file = "allnode.htm"
shadowsocks_file = "shadowsocks.json"
local_file = "/home/tool/shadowsocks/shadowsocks/shadowsocks/local.py"
CHECK_URL = "http://api.douban.com/v2/movie/subject/7054604"
SLEEP_TIME = 600  #单位是秒
      

def get_server_list(data_dict):
    """ 获取所有的server列表 """
    
    server_list = []
    if "configs" in data_dict:
        for record in  data_dict["configs"]:
            if "server" in record:
                server_list.append(record["server"])
    return server_list


def read_file(filename):
    """ 读文件，返回字符串格式的数据 """
    
    try:
        fp = open(filename, "r")
        c = fp.read()
        fp.close()
    except:
        c = ""
    return c
    
    
def get_json_data(c):
    """ 返回json格式的数据 """
    
    try:
        data_dict = json.loads(c)
    except Exception as e:
        data_dict = {}
        print str(e)
    return data_dict


def replace_server(c_shadowsocks, server_url, replace_str):
    """ 替换shadowsocks.json文件里的server """
    
    return c_shadowsocks.replace(server_url, replace_str)   


def get_shadowsocks_server(shadowsocks_dict):
    """ 获取shadowsocks.json文件里的server """
    
    if "server" in shadowsocks_dict:
        server = shadowsocks_dict["server"]
    else:
        server = ""
    return server


def write_file(filename, c):
    """ 写文件 """
    
    try:
        fp = open(filename, "w")
        fp.write(c)
        fp.close()
    except Exception as e:
        print str(e)
        
        
def isSuccess_old(url):
    """
        param: url, 待访问的地址
        return: flag, 布尔值类型
        url是否可以访问,如果不能正常访问，则有可能时无效地址或者是被墙了
    """
    try:
        res = urllib2.urlopen(url)
        if res.code == 200:
            flag = True
        else:
            flag = False
    except Exception as e:
        print str(e)
        flag = False
    return flag


def isSuccess(url):
    """
        param: url, 待访问的地址
        return: flag, 布尔值类型
        url是否可以访问,如果不能正常访问，则有可能时无效地址或者是被墙了 
    """
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.perform()
        code = c.getinfo(c.HTTP_CODE)   #获取http的状态码返回值
        if not str(code).startswith("4"):
            flag = True
        else:
            flag = False
    except Exception as e:
        print str(e)
        flag = False
    return flag

def restart_service(local_file, shadowsocks_file):
    cmd = "python %s -c %s -d restart" % (local_file, shadowsocks_file)
    subprocess.call(cmd, shell = True)
  

def main(allnode_file, shadowsocks_file, CHECK_URL, SLEEP_TIME):
    c_allnode = read_file(allnode_file)
    allnode_dict = get_json_data(c_allnode)
    server_list = get_server_list(allnode_dict)
    num = 1
    for server in server_list:
        c_shadowsocks = read_file(shadowsocks_file)
        shadowsocks_dict = get_json_data(c_shadowsocks)
        server_url = get_shadowsocks_server(shadowsocks_dict)  #获shadowsocks.json文件里的server
        if server_url:
            """替换server """
            c_shadowsocks = replace_server(c_shadowsocks, server_url, server)
            print num, " %s -------------> %s" % (server_url, server)
            flag = isSuccess(CHECK_URL)
            while flag:  
                time.sleep(SLEEP_TIME)
                flag = isSuccess(CHECK_URL)  
            write_file(shadowsocks_file, c_shadowsocks)
            restart_service(local_file, shadowsocks_file)
        num += 1
    

if __name__ == "__main__":
    main(allnode_file, shadowsocks_file, CHECK_URL, SLEEP_TIME)
    
    
    