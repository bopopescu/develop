#-*- encoding:utf-8 -*-
'''
Created on 2017-3-9

@author: dedong.xu

@description: 重载python运算符
'''

class NumStr(object):
    
    def __init__(self, num, strs):
        """ 初始化变量 """
        self.num = num
        self.strs = strs
    
    def __str__(self):
        """ 转化为字符串形式 """
        return "[%s::%s]" % (self.num, self.strs)
    
    __repr__ = __str__
    
    def __add__(self, other):
        """ 加法重载 """
        return self.__class__(self.num + other.num, self.strs + other.strs)
    
    def __mul__(self, n):
        """ 乘法重载 """
        return self.__class__(self.num * n, self.strs * n)
    
        
t1 = NumStr(12, "qwe")
t2 = NumStr(13, "asd")

print t1+t2
print t1*10



        