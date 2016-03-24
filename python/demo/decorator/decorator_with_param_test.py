#-*-:encoding:utf-8 -*-

import functools

"""
    该函数也是装饰一个带参数的函数，传递魔法参数，即可把有参函数和无参函数的情况合并了
"""

def deco():
    #print "begin to decorator"
    def newdeco(func):
        @functools.wraps(func)
        def test(a, b,z,c):
            aa = func(a,b,z,c)
            #print aa
            #return aa
        return test
    return newdeco

def deco2(func):
    @functools.wraps(func)
    def warpper(*args, **kwargs):
        aa = func(*args, **kwargs)
    return warpper

@deco()
#@deco2
def mytest(x,y,z,c):
    if x > y:
        print x
    else:
        print y
    return 345

print "function name is: ", mytest.__name__
mytest(3,4,5,7)



