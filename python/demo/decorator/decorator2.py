import functools
def log1(function):
    def wrapper(*args, **kwargs):
        print 'before function [%s()] run.' % function.__name__
        rst = function(*args, **kwargs)
        print 'after function [%s()] run.' % function.__name__
        return rst
    return wrapper 


def log(func):
    print func.__name__
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print func.__name__
        print "before"
        func(*args, **kwargs)
        print "after"
    return wrapper

@log
def func_test(a):
    print 'func() run. %s' % a
    return 111111111111111111111

if '__main__' == __name__:
    func_test("asdsada")
    print func_test.__name__

