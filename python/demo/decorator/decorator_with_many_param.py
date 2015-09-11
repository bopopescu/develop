#-*- encoding:utf-8 -*-

"""
    该脚本里装饰器装饰的是参数列表不一样的多个函数，此时就用到了python的魔法参数。
    定义函数时：*args 收集其余的位置参数，返回元组。**kwargs 收集其余的关键字参数，返回字典。
    调用函数时：*args 将元组拆分为位置参数传入， **kwargs 将字典拆分为关键字参数传入

    注：位置参数 就是 普通参数，位置参数和关键字参数联合使用的时候，位置参数必须在前
    关键字参数就是 类似 :a = 1 这样
"""

def deco(func):
    def wrapper(*args,**kwargs):
        print "start"
        func(*args,**kwargs)
        print "end"
    return wrapper



@deco
def foo(x):
    print "In foo"
    print "I have a param: %s" % x


@deco
def bar(x,y):
    print "In bar"
    print "I have two params: %s,%s" % (x,y) 

@deco
def foo_dict(x,y="dict_para"):
    print "In foo_dict"
    print "I have two params: %s,%s" % (x,y) 



if __name__ == "__main__":
    foo("aaa")
    print "********************"
    bar("qqq","www")
    print "********************"
    foo_dict("zzz",y="eee")

