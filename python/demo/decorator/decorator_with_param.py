#-*-:encoding:utf-8 -*-

import functools

"""
    下面这个函数是装饰带有参数的函数。
"""

def deco(func):
    @functools.wraps(func)
    def wrapper(x):
        print "start"
        func(x)
        print "end"
    return wrapper


@deco
def foo(x):
    print "In foo"
    print "I have a param: %s" % x


foo("asd")
