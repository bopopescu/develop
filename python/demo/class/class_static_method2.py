#-*- encoding:utf-8 -*-
'''
Created on 2016��4��22��

@author: dedong.xu
'''
class BaseColor(object):
    _color = "color"
    
    def values(self):
        return self.color
    
    
class Red(BaseColor):
    _color = "Red111111111111111"
    
class Green(BaseColor):
    _color = "Green111111111111111"
    
    
r = Red()
print r._color

g = Green()
print g._color

print "*"*100
class A(object):
    _color = 111
    #@classmethod
    def test(self):
        #print 111111111#, #self.__name__
        self._color = 99
        
    @staticmethod
    def smethod():
        print 2222222222
        _color = 789987
        
print "_color is: ", A._color       
print "_color is: ", A()._color  
#A.test()
A().test()
A.smethod()
A().smethod()
print "_color is: ",A._color
print "_color is: ",A()._color  

print A.__dict__
a = A()
print a.__dict__
a.test()
print "instance color is: ", a._color
print "class color is: ",A._color


