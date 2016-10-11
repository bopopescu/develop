#-*- encoding:utf-8 -*-

'''
Created on 2016-09-07

@author: dedong.xu

@description: 一共两个类,一个类：从指定目录里找到最新的安装包并安装；另一个类：卸载已安装的安装包。
'''

#standard lib
import os
import shutil
import re
import _winreg


build_path = r"\\10.10.2.72\nas\VidOn_package\VidOn_Server\VidOn_Server_for_Windows\MovieBar_Dev_Build"
registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VidOn Server 2_is1"
process_name_list = ["VidOnTray2.exe", "VidOnServer2.exe", "VidOnMysqld.exe"]
dirs_list = [r"C:\Users\Public\Documents\VidOn Server", r"C:\Users\Public\Documents\VidOnCloud", r"C:\Users\Public\Documents\VMS2"]
valuename = "UninstallString"

class Install_Package(object):
    """ 安装 安装包 """
    def __init__(self, src_path):
        """ 初始化设置 """
        self.src_path = src_path


    def find_newest_path(self):
        """ 根据正则表达式匹配指定的目录，获得最新的目录 """
        p = r"\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}"
        reg_com = re.compile(p)
        try:
            newest_dir =  max([i for i in os.listdir(self.src_path) if reg_com.match(i)])
            return os.path.join(self.src_path, newest_dir)
        except Exception as e:
            print (str(e))
            return ""
        
    
    def get_package(self, newest_path):
        """ 获得当前目录下的扩展名为 exe的文件"""
        package_file = ""
        for each_file in os.listdir(newest_path):
            if os.path.splitext(each_file)[1].lower() == ".exe":
                package_file = os.path.join(newest_path, each_file)
                break
        return package_file


    def install_package(self, package_file):
        """ 静默安装 """
        os.system("%s /verysilent" % package_file)
        
        
        
class Uninstall_Package(object):   
    """ 卸载安装包 """
    def __init__(self, registry_path, dirs_list, process_name_list):
        """ 初始化设置 """
        self.registry_path = registry_path   
        self.dirs_list = dirs_list
        self.process_name_list =  process_name_list
        
        
    def uninstall_package(self, uninstall_file):
        """ 静默卸载 """
        os.system("%s /verysilent" % uninstall_file)
    
        
    def get_uninstall_file(self, valuename):
        """ 通过注册表获取卸载程序的路径 """
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, self.registry_path)
            uninstall_file = _winreg.QueryValueEx(key, valuename)[0]
        except Exception as e:
            uninstall_file = ""
            print str(e)
        return uninstall_file
    
    
    def remove_dir(self, path):
        """ 删除目录 """
        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
            print "remove %s" % path
            
            
    def remove_dirs_list(self):
        """ 删除目录列表 """
        for path in self.dirs_list:
            self.remove_dir(path)
        
        
    def kill_process_list(self):
        """ 杀死进程列表 """
        for process_name in self.process_name_list:
            self.kill_process(process_name)
    
        
    def kill_process(self, process_name):
        """ 杀死进程 """
        os.system("taskkill /f /im %s" % process_name)
        


def main_install(build_path):
    """ 安装主程序入口 """
    ip = Install_Package(build_path)
    newest_path = ip.find_newest_path()
    print newest_path
    if newest_path:
        package_file = ip.get_package(newest_path)
        if package_file:
            ip.install_package(package_file)
        else:
            print("not find package file!!")
    else:
        print("not find newest path")


def main_uninstall(registry_path, dirs_list, process_name_list):
    """ 卸载主程序入口 """
    up = Uninstall_Package(registry_path, dirs_list, process_name_list)
    up.kill_process_list()
    up.remove_dirs_list()
    uninstall_file = up.get_uninstall_file(valuename)
    up.uninstall_package(uninstall_file)


if __name__ == "__main__":
    main_uninstall(registry_path, dirs_list, process_name_list)
    main_install(build_path)
    
    
