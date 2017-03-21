#-*- encoding:utf-8 -*-

'''
Created on 2016-12-7

@author: dedong.xu

@description: 主程序入口
'''

#standard lib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import re
import shutil
import threading

#local lib
from adb_install import Adb_Install
from read_excel_file import Read_Excel
from parse_xml import Parse_Xml
import log
from settings import EXCEL_FILE, MOVIE_EXCEL_FILE, PLAYBACK_XML, LOG_PATH_IN_BOX, LOG_PATH, INFO_FILE, POSTFIX_ZIPFILENAME, HTTP_URL, EXTEND_NAME, PLAYER_LOG_EXTEND_NAME, PING_COUNT, REMOTE_LOG_PATH


def ping(ip):
    """ ping ip """
    ping_file = os.path.join(os.getcwd(), "ping", ip)
    ping_cmd = "ping %s -n %d > %s" % (ip, PING_COUNT, ping_file)
    try:
        os.system(ping_cmd)
    except Exception as e:
        pass
    return ping_file
	
def read_file_lines(filename):
    with open(filename, "r") as f:
        return f.readlines()

def analyze_ping_result(ping_file):
    """ analyze ping result """
    all_lines = read_file_lines(ping_file)
    analyze_line = ""
    for line in all_lines:
        if line.find("%") != -1:
            analyze_line = line
            break
    pattern = r"(\d+)(\%)"
    search_result = re.search(pattern, analyze_line)
    if search_result:
        loss_result = int(search_result.group(1))
    else:
        loss_result = 100
    return True if loss_result < 100 else False


class Plcore_Auto_Test(object):
    def __init__(self):
        """ 初始化变量 """
        #self.adb_install = Adb_Install
        #self.re = Read_Excel
        #self.px = Parse_Xml
        
    def __write_file(self, filename, c):
        """ 写文件  """
        with open(filename, "w") as f:
            f.write(c)
            
    def __delete_file(self, filename, num = 5):
        """ 删除文件 """
        for i in xrange(num):
            try:
                os.remove(filename)
                print "delete success"
                break
            except Exception, e:
                time.sleep(1)
                print str(e)
		
    def get_cur_date(self):
        """ 获取当前的日期 """
        return time.strftime("%Y%m%d")
		
    def get_movie_name(self, xml_str):
        """ 正则表达式获得电影名字全路径 """
        p = r"<filepath path=(.*?)/>"
        return re.search(p, the_str).group(1)
		
    def get_logname(self, log_extendname):
        """ 获得盒子上的log的名字 """
        return "%s-%s" % (self.get_cur_date(), log_extendname)
		
    def set_local_logname(self, ip, log_extendname):
        """ 设置从盒子上取下来的log在本地的名字 """
        return "%s-%s-%s" % (ip, self.get_cur_date(), log_extendname)
		
    def get_logfile_list(self, local_log_path):
        """ 获得log文件 """
        logfile_list = []
        cur_date = time.strftime("%Y%m%d")  
        for eachfile in os.listdir(local_log_path):	
            if eachfile.startswith(cur_date):
                print os.path.join(local_log_path, eachfile)		
                logfile_list.append(os.path.join(local_log_path, eachfile))
        return logfile_list
		
    def get_working_ip_list(self, ip_list):
        """ 获取开机的盒子ip列表 """
        new_ip_list = []
        for ip in ip_list:
            ping_file = ping(ip)
            result = analyze_ping_result(ping_file)
            if result:
                new_ip_list.append(ip)
        return new_ip_list
		
    def install_run(self, data_dict, key, index, rel, adbi, px):
        """ 执行自动化程序 """
        print "只安装一次"
        #apk_version = rel.get_apk_version(key, index)
        apk_update_conf_content = rel.get_apk_update_conf_content(key, index)
        play_conf_content = data_dict[key][index][3]
        root = px.parse(apk_update_conf_content)
        #movie_full_path_name = px.parse(play_conf_content).getElementsByTagName("section")[0].getElementsByTagName("filepath")[0].getAttribute("path")
        node_apk = px.get_xmlnode(root, "section")[0]
        apk_path = px.get_apk_path(node_apk)
        ip_list = px.get_ip_list(node_apk)
        ip_list = self.get_working_ip_list(ip_list)
        root = px.parse(play_conf_content)
        node_play = px.get_xmlnode(root, "section")[0]
        #remote_path = px.get_xml_path(node_play)
        adbi.mutil_connect_box(ip_list)
        adbi.mutil_install_apk(ip_list, apk_path)
		
    def run(self, data_dict, key, index, rel, adbi, px, box_log_path, local_log_path, log_extendname, remote_log_path):
        """ 执行自动化程序 """
        apk_version = rel.get_apk_version(key, index)
        apk_update_conf_content = rel.get_apk_update_conf_content(key, index)
        #play_conf_content = rel.get_play_conf_content(key, index) 
        play_conf_content = data_dict[key][index][3]
        root = px.parse(apk_update_conf_content)
        movie_full_path_name = px.parse(play_conf_content).getElementsByTagName("section")[0].getElementsByTagName("filepath")[0].getAttribute("path")
        print "movie_name full path name is: %s" % movie_full_path_name
        node_apk = px.get_xmlnode(root, "section")[0]
        apk_path = px.get_apk_path(node_apk)
        ip_list = px.get_ip_list(node_apk)
        print "所有的盒子: ", ip_list
        ip_list = self.get_working_ip_list(ip_list)
        print "开机的盒子：", ip_list
        root = px.parse(play_conf_content)
        node_play = px.get_xmlnode(root, "section")[0]
        remote_path = px.get_xml_path(node_play)
        adbi.mutil_connect_box(ip_list)
        #adbi.mutil_install_apk(ip_list, apk_path)
        filename = "player%d.xml" % index
        self.__write_file(filename, play_conf_content)
        local_path = os.getcwd()
        for ip in ip_list:
            pull_file = px.get_xml_file(node_play)
            adbi.adb_remove_file(ip, pull_file)
            local_xml_file = os.path.join(local_path, os.path.basename(pull_file))
            adbi.adb_push_file(ip, filename, os.path.join(remote_path, filename).replace("\\", "/"))
            adbi.start_apk(ip, os.path.join(remote_path, filename).replace("\\", "/"))
        n = 0
        while 1:
            ip_list = [i for i in ip_list if i.strip()]
            if not ip_list:
                break
            print "start", "*" * 100, ip_list
            for ip in ip_list:
                if os.path.exists(local_xml_file):
                    self.__delete_file(local_xml_file)
                adbi.adb_pull_file(ip, pull_file, local_path)
                if os.path.exists(local_xml_file):
                    root = px.parse_xmlfile(local_xml_file)
                    state = px.get_attrvalue(px.get_xmlnode(root, "runningstate")[0], "state")
                    flag = self.__check_state(state)
                    if flag:
                        local_logfile = os.path.join(local_log_path, self.set_local_logname(ip, log_extendname))
                        adbi.adb_pull_file(ip, os.path.join(box_log_path, self.get_logname(log_extendname)), local_logfile)
                        shutil.copy2(local_logfile, remote_log_path)
                        self.__delete_file(local_logfile)
                        ip_list[ip_list.index(ip)] = ""
                else:
                    print "current ip : %s; %s does not exist! check next box! \nwaitting for 5 seconds! n is: %s" % (ip, local_xml_file, n)
                    time.sleep(5)
                    n += 1
                    if n == 10:
                        print "该盒子: %s一直没有info.xml，故而剔除! 电影名字： %s" % (ip, movie_full_path_name)
                        ip_list[ip_list.index(ip)] = "" 
                        n = 0
            print "end", "*" * 100
			
    def __update_data(self, data_dict, movie_list, update_xml):
        """ 替换xml的内容 """
        for key in data_dict:
            for index in xrange(0, len(data_dict[key])):
                try:
                    print data_dict[key][index][3]
                    data_dict[key][index][3] = update_xml(data_dict[key][index][3], movie_list[index-1])
                except Exception, e:
                    print key, str(e), "EXCEPTION"
					
    def __get_movie_list(self, movie_excel_file):
        """ 获取所有的电影列表,只取标志位为1的那些电影 """
        rel_movie = Read_Excel(movie_excel_file)
        #movie_list = [j[0] for i in rel_movie.get_all_data().values() for j in i if int(j[1]) == 1]
        movie_list = []
        for i in rel_movie.get_all_data().values():
            for j in i:
                if j[1] == 1:
                    movie_list.append(j[0])	
        return movie_list			

    def mutil_run(self, excel_file, movie_excel_file, playback_xml, box_log_path, local_log_path, log_extendname, remote_log_path):
        """ 多线程执行自动化测试程序 """
        if os.path.exists(playback_xml):
            self.__delete_file(playback_xml)
        rel = Read_Excel(excel_file)
        adbi = Adb_Install()
        px = Parse_Xml()
        movie_list = self.__get_movie_list(movie_excel_file)
        if not movie_list:
            print "没有可以测试的电影!!"
            return
        print movie_list
        data_dict = rel.get_all_data()
        #开始替换xml文件内容
        print "长度为:  ", len(data_dict["Sheet1"])
        install_thread_list = []
        #安装,因为data_dict只有一个key， 就是Sheet1，所以只安装一次
        for key in data_dict:
			for index in xrange(0, len(data_dict[key])):
				t = threading.Thread(target = self.install_run, args = (data_dict, key, index, rel, adbi, px))
				install_thread_list.append(t)
				t.start()
			for i in install_thread_list:
				i.join()
        #播放电影		
        length = len(data_dict["Sheet1"])
        for i in xrange(0, len(movie_list), length):
            print "number", i, "begin to play! %s" % time.strftime("%Y-%m-%d %H:%M:%S"), movie_list[i: i+length]
            self.__update_data(data_dict, movie_list[i: i+length], px.update_xml)
            thread_list = []
            for key in data_dict:
                for index in xrange(0, len(data_dict[key])):
                    t = threading.Thread(target = self.run, args = (data_dict, key, index, rel, adbi, px, box_log_path, local_log_path, log_extendname, remote_log_path))
                    thread_list.append(t)
                for t in thread_list:
                    t.start()
                for i in thread_list:
                    i.join()
        print "playing over!!!"
        adbi.disconnect_box()
                
    def __check_state(self, state):
        """ 检查状态 """
        if state.lower() == "running":
            time.sleep(60)
            print "the movie is running"
            return False
        elif state.lower() == "done":
            print "the movie is done"
            return True
        else:
            print "the movie is stopped"
            return True
    

            
if __name__ == "__main__":
    pat = Plcore_Auto_Test()
    pat.mutil_run(EXCEL_FILE, MOVIE_EXCEL_FILE, PLAYBACK_XML, LOG_PATH_IN_BOX, LOG_PATH, PLAYER_LOG_EXTEND_NAME, REMOTE_LOG_PATH)
    #log.main(LOG_PATH, INFO_FILE, POSTFIX_ZIPFILENAME, HTTP_URL, EXTEND_NAME)
    
    