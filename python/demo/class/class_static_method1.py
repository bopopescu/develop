#-*- encoding:utf-8 -*-

'''
Created on 2016��4��22��

@author: dedong.xu
'''

class BaseColor(object):
    __color = (0,0,0)
    
    @classmethod
    def values(cls):
        if cls.__name__ == "Red":
            cls.__color = (255,0,0)
        if cls.__name__ == "Green":
            cls.__color = (0,255,0)
        return cls.__color
    
class Red(BaseColor):
    pass
class Green(BaseColor):
    pass
red = Red()
print red.values()
red = Green()
print red.values()