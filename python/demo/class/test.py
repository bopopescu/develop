#-*- encoding:utf-8 -*-

'''
Created on 2016��6��27��

@author: dedong.xu
'''
import sys

def test():
    if 1:
        print "asdasda"
    else:
        sys.exit()


class Test(object):
    count = 0
    def __init__(self):
        self.name = "xdd"
        Test.count += 1
        
    def getname(self):
        return self.name
    
    def __del__(self):
        Test.count -= 1
        
    def getcount(self):
        return Test.count
        

def format_str():
    a =  "%s" % "xdd"
    b =  "%d" % 131
    print a, type(a)
    print b, type(b)

if __name__ == "__main__":
    test()
    print 88888888888888
    tt = Test()
    aa = tt.getname()
    print aa
    print "*"*100
    print tt.getcount()
    tt1 = Test()
    print tt1.getcount()
    print tt.getcount()
    
    del tt
    print tt1.getcount(),  Test.count
    del tt1
    print Test.count
    format_str()
    tt = Test()
    print dir(tt)
    