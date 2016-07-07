#-*- encoding:utf-8 -*-

'''
Created on 2016-07-05

@author: dedong.xu
'''

"""
格式: [num::'str']
加, 乘操作符重载
"""

class NumStr(object):
    def __init__(self, num = 0, strs = ""):
        self.__num = num
        self.__str = strs
        
    def __str__(self, *args, **kwargs):
        return "[%d::%r]" % (self.__num, self.__str)
    
    __repr__ = __str__
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.__num + other.__num, self.__str + other.__str)
        else:
            raise TypeError, "Illegal argument type for built-in operation"
    
    def __mul__(self, n):
        if isinstance(n, int):
            return self.__class__(self.__num * n, self.__str * n)
        else:
            raise TypeError, "Illegal argument type for built-in operation"
    
    
ns1 = NumStr(13, "ad")
ns2 = NumStr(43, "12ad")
print ns1
print ns2
print ns1 + ns2
print ns1 * 4
print "*"*100

class A(object):
    a1 = 100
    __b1 = 10
    
    def __test(self):
        print 111111111111111
    
    
class B(A):
    a1 = 99
    __b1 = 12
    
    def __test(self):
        print 2222222222222
    
a = A()
print a.a1, a._A__b1, a._A__test()

b = B()
print b.a1, b._B__b1, b._B__test()

