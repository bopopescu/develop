#-*-:encoding:utf-8 -*-

import time
import functools

"""
  个人认为，装饰器应该返回一个函数对象，该函数应该是经过包装装饰之后的原函数
"""

"""
  timeit函数里返回了一个wrapper函数对象，timeit的作用是给func进行装饰，
  wrapper函数就是装饰过的func。
"""



def timeit(func):
    """下面这句代码保证了函数名字是最初被调用的函数foo，而不是函数名wrapper"""
    @functools.wraps(func)
    
    def wrapper():
        start = time.clock()
        func()
        end = time.clock()
        print end - start
        print "*****************"
    return wrapper



"""
    被装饰的函数不带参数
"""
@timeit
def foo():
    print 111111

print foo
print "function name is: ",foo.__name__
foo()




