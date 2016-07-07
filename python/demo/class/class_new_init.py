
#-*- encoding:utf-8 -*-
'''
Created on 2016��4��6��

@author: dedong.xu
'''

class A1(object):
    def __new__(cls):
        print "in new"
        obj = super(A1, cls).__new__(cls)
        return obj
    
    def __init__(self):
        print "in init"
        
a1 = A1()     

   
print "*"*100
class A(object):
    def __new__(self):
        Object = super(A,self).__new__(self)
        print "in new"
        return Object
    def __init__(self):
        print "in init"
        
        
class B(A):
    def __init__(self):
        print "in B's init"   
        
    def __new__(self):
        print "in B's new"  
        return object.__new__(self) 

B()    

print "+"*100
class Person(object):
    """Silly Person"""
 
 
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print 111111111111111111
 
 
    def __str__(self):
        return 'Person: %s(%s)' % (self.name, self.age)
 
 
if __name__ == '__main__':
    piglei = Person('xdd', 24)
    print piglei.__dict__
    print Person.__dict__
    print piglei    