#-*- encoding:utf-8 -*-

'''
Created on 2016��7��4��

@author: dedong.xu
'''

class RoundFloat(object):
    def __init__(self, value):
        assert isinstance(value, float), "the second argument param must be float!"
        self.value = round(value, 3)
        
    def __str__(self):
        return "%.2f" % self.value
    
    __repr__ = __str__
        
    
        
aa = RoundFloat(1.0)



class Time60(object):
    def __init__(self, hr, min):
        self.hr = hr
        self.min = min
        
    def __str__(self):
        return "%d:%d" % (self.hr, self.min)
    
    def __add__(self, other):
        return self.__class__(self.hr + other.hr, self.min + other.min)
    
    def __iadd__(self, other):
        self.hr += other.hr
        self.min += other.min
        return self
        
    
t6 = Time60(12,35)
print t6
t7 = Time60(11,20)
print t7

print t6 + t7
print id(t6)
t6 += t7
print t6
print id(t6)