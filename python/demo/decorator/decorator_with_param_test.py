#-*-:encoding:utf-8 -*-

import functools

"""
    该函数也是装饰一个带参数的函数，但是还没看懂
"""

def deco():
    print "begin to decorator"
    def newdeco(func):
        @functools.wraps(func)
        def test(a, b,z,c):
            aa = func(a,b,z,c)
            #print aa
            #return aa
        return test
    return newdeco

@deco()
def mytest(x,y,z,c):
    if x > y:
        print x
    else:
        print y
    return 345

print "function name is: ", mytest.__name__
mytest(3,4,5,7)



