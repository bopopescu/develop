#-*- encoding:utf-8 -*-
'''
Created on 2016��4��6��

@author: dedong.xu
'''
def singleton(cls):
    instances = {}
    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getInstance


@singleton        
class A(object):
    pass



@singleton
class B(object):
    pass


a1=A()
a2=A()
b1=B()
b2=B()

print id(a1),id(a2)
print id(b1),id(b2)



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
assert id(s1) == id(s2)
print type(s1)
print isinstance(s1, object)
