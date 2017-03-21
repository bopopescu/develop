#-*- encoding:utf-8 -*-

'''
Created on 2016-12-7

@author: dedong.xu

@description: 使用adb命令远程安装apk包
'''

import subprocess
import threading

#ip_list = []
#apk_path = r""

class  Adb_Install(object):
    """ 使用adb命令远程安装apk包 """
    
    def __init__(self):
        """ 初始化变量 """
        #self.ip_list = ip_list
        #self.apk_path = apk_path
		
		
		
    def adb_devices(self):
        """ 查看盒子 """
        subprocess.call("adb devices", shell = True)
        print "adb devices"
        
    def disconnect_box(self):
        """ 断开盒子 """
        try:
            subprocess.call("adb disconnect", shell = True)
            print "adb disconnect"
        except Exception, e:
            print str(e)
        return
    
    def connect_box(self, ip):
        """ 连接盒子 """
        subprocess.call("adb connect %s" % ip, shell = True)
        
    def install_apk(self, ip, apk_path):
        """ 安装apk """
        subprocess.call("adb -s %s:5555 install -r %s" % (ip, apk_path), shell = True)
        
    def mutil_connect_box(self, ip_list):
        """ 多线程连接盒子 """
        print "mutil_connect_box", ip_list
        t_list = []
        for ip in ip_list:
            print "connect %s" % ip
            t = threading.Thread(target = self.connect_box, args = (ip,))
            t_list.append(t)
        for i in t_list:
            i.start()
        for j in t_list:
            j.join(5)
        
    def mutil_install_apk(self, ip_list, apk_path):
        """ 多线程进行安装 """
        print "mutil_install_apk, 安装一次"
        t_list = []
        for ip in ip_list:
            t = threading.Thread(target = self.install_apk, args = (ip,apk_path))
            t_list.append(t)
        for i in t_list:
            i.start()
        for j in t_list:
            j.join(60)
            
    def adb_push_file(self, ip, localfile, remote_path):
        """ adb推送文件至盒子 """
        cmd = "adb -s %s:5555 push %s %s" % (ip, localfile, remote_path)
        print "adb push file: %s" % cmd
        subprocess.call(cmd, shell = True)
            
    def start_apk(self, ip, filename):
        """ 启动apk """
        cmd = "adb -s %s:5555 shell am start -n org.vidonme.vvplayer/org.vidonme.vvplayer.activity.VideoView -d %s" % (ip, filename)
        print "start apk cmd: %s" % cmd
        subprocess.call(cmd, shell = True)
        
    def adb_pull_file(self, ip, filename, local_path):
        """ adb从盒子上拉取文件下来 """
        cmd = "adb -s %s:5555 pull %s %s" % (ip, filename, local_path)
        print "adb pull file : ", cmd
        subprocess.call(cmd, shell = True)
		
    def adb_remove_file(self, ip, filename):
        """ adb删除盒子上的文件 """
        cmd = "adb -s %s:5555 shell rm %s" % (ip, filename)
        print "adb remove file : ", cmd
        subprocess.call(cmd, shell = True)
        
            
if __name__ == "__main__":
    adb = Adb_Install()
    adb.disconnect_box()
    adb.mutil_connect_box()
    adb.mutil_install_apk()
        
        
        
        
        
        
        
        
        