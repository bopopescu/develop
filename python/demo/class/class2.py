#-*- encoding:utf-8 -*-

'''
Created on 2016��4��15��

@author: dedong.xu
'''
"""
__metaclass__ = type
class A(object):
    def __init__(self):
        self.name = "xdd"
        self.age = 67
        name = 8888
    def test(self):
        pass

class B(A):
    asd = ""
    vv = ""
    def __init__(self):
        A.__init__(self)
        super(A, self)
        self.cc = 0
class C:
    def test(self):
        self.aaaa = 909090    
        print self.aaaa
    def test1(self):
        print self.aaaa
        print type(self.aaaa)
  
a = A()
print A.__name__
print a
print A.__dict__
print a.__dict__
print "徐德东 "

print type(A)
print B.__dict__
b = B()
print b.__dict__

print dir(A)
print type(A)
print dir(C)
print type(C)
print "*"*100
c = C()
c.test()
c.test1()
"""
"""
class A(object):
    name = "xdd"
    count = 1
    sex = "female"
    def __init__(self):
        self.age = 45
        self.name = "xdd131"
        self.count +=0
        self.sex = 789
        A.count += 100
        
    def test(self):
        print self.age
        
a = A()
a.test()


print A.__dict__.keys()
print a.__dict__.keys()

print "*"*100
print A.__dict__
print a.__dict__
print A.name
print a.name
print A.count
print a.count
print A.count
print A.count
print "*"*100
b1 = A()
print b1.count, A.count

b1 = A()
print b1.count, A.count
"""
"""
class SortedDict1(dict):
    def keys(self):
        return sorted(self.keys())
    
class SortedDict(dict):
    def keys(self):
        return sorted(super(SortedDict, self).keys())
    
di = {"r":1, "h":2,"a":3,"d":4}    
sd = SortedDict(di)
print sd.keys()
"""


class A(object):
    def __init__(self):
        self.name = 1
        self.age = 2
        
        
class B(A):
    def __init__(self):
        #A.__init__(self)
        super(B, self).__init__()
        
class C(object):
    __c = "xdd"

    def getvalue(self):
        return self.__c
    
b = B()
print b.name
print b.age

c = C()
print c.getvalue()
