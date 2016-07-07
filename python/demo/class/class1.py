#-*- encoding:utf-8 -*-

'''
Created on 2016��4��6��

@author: dedong.xu
'''
"""只要实例的属性经过改动，那么他就和类属性没有任何关系了；没有改动的实例的属性会读取类属性的值"""

class A():
    a = 10
    
a1 = A()
a2 = A()

print a1.a, a2.a,A.a

a1.a += 10

print a1.a, a2.a,A.a
A.a += 1
print a1.a, a2.a,A.a

def deco(cls):
    instances = {}
    def singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return singleton


@deco
class AA():
    pass
aa1 = AA()
aa2 = AA()
print id(aa1), id(aa2), "  0000000000000000000"

class Singleton(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
    
    
s1 = Singleton()
s2 = Singleton()

print id(s1), id(s2)