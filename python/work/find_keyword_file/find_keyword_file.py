#-*- encoding:utf-8 -*-

'''
Created on 2017-1-3

@author: dedong.xu

@description: 该程序找出给定的文件或者目录下的所有包含指定关键字的文件
'''

import sys
import os


class FindKeyWordFile(object):
    def __init__(self, filepath, keywordfile):
        """ 初始化变量 """
        self.filepath = filepath
        self.keywordfile = keywordfile

    def read_file(self, filename):
        """ 读取文件全部内容，返回字符串"""
        with open(filename, "r") as f:
            return f.read()
        
    def __read_file_lines(self, filename):
        """ 按行读取文件，返回一个列表 """
        with open(filename, "r") as f:
            return f.readlines()
     
    def get_all_keywords(self):
        """ 获得所有的关键字 """
        return [i.strip() for i in self.__read_file_lines(self.keywordfile) if i.strip()]
    
    def get_all_files(self):
        """ 获得所有的待检测的文件 """
        return [os.path.join(self.filepath, i) for i in os.listdir(self.filepath)]
    
    def find_keyword(self, keywords_list, filecontent):
        """ 查找关键字 """
        for keyword in keywords_list:
            if keyword in filecontent:
                return keyword
        return False
    
def main(filepath, keywordfile):
    """ 程序入口 """
    dir_flag = True if os.path.isdir(filepath) else False
    fkwf = FindKeyWordFile(filepath, keywordfile)
    keywords_list = fkwf.get_all_keywords()
    all_files = fkwf.get_all_files() if dir_flag else [filepath]
    for each_file in all_files:
        content = fkwf.read_file(each_file)
        keyword = fkwf.find_keyword(keywords_list, content)
        if keyword:
            print "%s contains keyword: %s" % (each_file, keyword)
   
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "this script needs 2 parameters"
        sys.exit(0)
    filepath = sys.argv[1]
    keywordfile = sys.argv[2]
    if not os.path.isfile(keywordfile):
        print "%s is not a file, it should be the keyword file" % keywordfile
        sys.exit(0)
    main(filepath, keywordfile)
    
    

    
    
    
    
    