#-*- encoding:utf-8 -*-

"""使用类来创建单例模式"""

class Singleton(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
		
s1 = Singleton()
print id(s1)
s2 = Singleton()
print id(s2)

