#-*- encoding:utf-8 -*-

'''
Created on 2017-03-01

@author: dedong.xu

@description: 输入是一个文件或者一个目录，输出是一个文件。还有一些关键字条件。
'''

import os
import sys
import time

""" 可以是目录，也可以是文件 """
path = r"Z:\other\users\xudedong\backup_DVDFab\Package_folder\package_path_2016_08_11_16_50_30\Common_Retail\log"

""" 需要保留的关键字列表 """
keyworld_list = []

""" 需要排除的关键字列表 """
not_keyworld_list = []

class FilterKeyWorldFile(object):
    """ 根据给定的文件和条件，过滤关键字，然后 生成新的文件"""
    
    def __init__(self):
        """ 初始化变量 """
        self.file_list = []
    
    def isfile(self, path):
        """ 判断是否是一个文件 """
        return os.path.isfile(path)
    
    def isdir(self, path):
        """ 判断是否是一个目录 """
        return os.path.isdir(path)
    
    def add_list(self,path):
        """ 添加文件到列表 """
        self.file_list.append(path)
    
    def transval_dir(self, path):
        """ 遍历目录获得所有的文件 """
        for roots, _, files in os.walk(path):
            for each_file in files:
                self.add_list(os.path.join(roots, each_file))
    
    def has_keyworld(self, the_str, keyworld):
        """ 过滤关键字 """
        if keyworld in the_str:
            return True
        return False
    
class Handle_File(object):
    """ 写文件 """
        
    def open(self, filename, mode):
        """ 打开文件 """
        self.fp = open(filename, mode)
        
    def write(self, c):
        """ 写文件 """
        self.fp.write(c)
        
    def read_by_lines(self):
        """ 按行读文件 """
        return self.fp.readlines()
        
    def close(self):
        """ 关闭文件 """
        self.fp.close()
    
if __name__ == "__main__":
    new_list = []
    fkwf = FilterKeyWorldFile()
    hf = Handle_File()
    newlogname = "%s.log" % time.strftime("%Y-%m-%d-%H-%M-%S")
    if fkwf.isfile(path):
        fkwf.add_list(path)
        print "当前的输入是一个文件"
    elif fkwf.isdir(path):
        fkwf.transval_dir(path)
        print "当前的输入是一个目录"
    else:
        print "既不是目录，也不是文件。请注意检查!"
        sys.exit(0)
    print fkwf.file_list
    
    for each_file in fkwf.file_list:
        hf.open(each_file, "r")
        all_lines = hf.read_by_lines()
        new_list.append("%s%s%s" % ("*"*20, each_file, "*"*20))
        for each_line in all_lines:
            if all([fkwf.has_keyworld(each_line, i) for i in keyworld_list]) and not any([fkwf.has_keyworld(each_line, i) for i in not_keyworld_list]):
                new_list.append(each_line)
        new_list.append("\n\n")
        hf.close()
        
    hf.open(newlogname, "w")
    for each_line in new_list:
        hf.write(each_line)
    hf.close()
    
    
    
    