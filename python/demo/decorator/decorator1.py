#-*- encoding:utf-8 -*-

def outer(func):
    def inner():
        print "inside function name: ", func.__name__
        func()
    return inner

@outer
def test():
    print 11111111111111


test()

#写个装饰器logger
#一个函数被调用时，在日志里记录其名称和被调用的实际参数

print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "++++++++++++++++++++++++++++++++++++++++++++++++++++"




def logger(func):
    def inner(*args, **kvargs):
        print "function name is: ", func.__name__, ", arguments is: ", args, kvargs
        func(*args, **kvargs)
    return inner

@logger
def xdd(a,b,c):
    print a,b,c

xdd(1,2,c=9)

print "*******************************************"
print "*******************************************"
print "*******************************************"

def logger(func):
    def inner(*args, **kvargs):
        print func.__name__, " called, arguments: ", args, kvargs
        func(*args, **kvargs)
    return inner

@logger
def func(x,y,z,a):
    print x,y,z,a

func(1,2,3,a=90)




















