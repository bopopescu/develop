#-*- encoding:utf-8 -*-

'''
Created on 2016��4��6��

@author: dedong.xu
'''

class Singleton(object):
    __instance = None
    
    #def __init__(self):
    #    self.color = "red"
        
    def __new__(cls, *args, **kwargs):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls, *args, **kwargs)
            print "this is a new object!"
        return Singleton.__instance
    
s = Singleton()
print s._Singleton__instance
s1 = Singleton()
print s1._Singleton__instance



class A(object):
    __ins = None
    def __new__(cls, *args, **kwargs):
        if A.__ins is None:
            A.__ins = object.__new__(cls, *args, **kwargs)
        return A.__ins



class B(A):
    a = 1000
    
    
b1 = B()
b2 = B()
print id(b1)
print id(b2)

print "+"*100
def singleton(cls):
    instance = {}
    def _singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return _singleton

@singleton
class D(object):
    d = 1
    
d1 = D()
d2 = D()
print id(d1)
print id(d2)












