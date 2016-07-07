#-*- encoding:utf-8 -*-

'''
Created on 2016��7��7��

@author: dedong.xu
'''

class WriteFile(object):
    def __init__(self, filename, mode = "r", buf = -1):
        self.__fp = open(filename, mode, buf)
        
    def write(self, content):
        self.__fp.write(content.upper())
        
    def __getattr__(self, attr):
        return getattr(self.__fp, attr)
    
    def __repr__(self):
        return "self.__fp"
    
    def __str__(self):
        return str(self.__fp)
        
    
    
wf = WriteFile("d:/test/xdd.txt", "w")
wf.write("adfadadadad")
wf.close()


