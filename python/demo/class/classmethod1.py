#-*- encoding:utf-8 -*-

'''
Created on 2016��4��3��

@author: dedong.xu
'''

class Person(object):
    __weight = 75
    name = "123"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod    
    def getname(cls, name, age, sex):
        print "class method!!! %s, My name is, %s,%s, %s" % (cls,name,age,sex)
        #print cls("qqqq", 89).__dict__
    
    @staticmethod
    def getage(age):
        print "static method!!!", age
        
    @classmethod    
    def cmethod(cls):
        print 111111111111, cls
        
    @staticmethod
    def smethod():
        print 2222222222222222
        
    def test(self):
        print 444444444444

        
        
p = Person("xdd", 27)        
Person.getname(1,2,3)
Person.getage(111)        
Person.cmethod()     
p.smethod()     
p.test()
Person.smethod() 
        
        
        
        
        
        
        
#p = Person("xdd", 27)
#Person.getname("gl", 88, 90)
#print "*"*100
#Person.getage(111)
#print Person.__dict__
#print p.__dict__
