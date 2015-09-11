# -*- coding:utf-8 -*-

 
def deco(func):
    def _deco(a, b):
        print 1111111111111111111111111
        ret = func(a, b)
        print ret
        print 2222222222222222222
        return ret
    return _deco
 
@deco
def myfunc(a, b):
    print(33333333333333333333, (a, b))
    return a + b
 
myfunc(1, 2)


