#-*-:encoding:utf-8 -*-

import time

"""
  timeit函数里返回了一个wrapper函数对象，timeit的作用是给func进行装饰，
  wrapper函数就是装饰过的func。
"""

"""
def timeit(func):
    def wrapper():
        start = time.clock()
        func()
        end = time.clock()
        print end - start
        print "*****************"
    return wrapper

def foo1():
    print 2222222222222222222222222222
    
foo1 = timeit(foo1)

foo1()
"""


def timeit(func):
    def wrapper():
        start = time.clock()
        func()
        end = time.clock()
        print end - start
        print "*****************"
    return wrapper

@timeit
def foo():
    print 1111111111

print foo
print "function name is: ", foo.__name__
foo()



