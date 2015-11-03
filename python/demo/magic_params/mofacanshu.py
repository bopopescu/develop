# -*- coding:utf-8 -*-

"""
    魔法参数    反转过程
    *args表示任何多个无名参数(位置参数)，是一个tuple；**kwargs表示关键字参数，是一个dict。
    并且同时使用*args和**kwargs时，必须*args参数列要在**kwargs前
"""

"""
    test1函数在定义时，参数前使用*或者**来收集参数，那么为该函数传递元组或者字典时，
    需要在实参前也相应的加上*或者**来对实参进行反转
"""
def test1(*args,**kwargs):
    for i in args:
        print i
    for i in kwargs:
        print i


"""
    test2函数在定义时，形参是一个普通参数，那么为该函数传递元组或者字典时，
    不用在实参前面加*或者**了，直接在函数内部将该参数作为元组或字典使用
"""
def test2(args,kwargs):
    for i in args:
        print i
    for i in kwargs:
        print i


def test3(args,**kwargs):
    for i in args:
        print i
    for i in kwargs:
        print i
        

if __name__ == "__main__":
    test1(1,2,3,a=4,b=5,c=6,d=7)
    print "********************************"
    test1(*(1,2,3),a=4,b=5,c=6,d=7)
    print "*********************************"
    test1(*(1,2,3,4),**{"a":5,"b":6,"c":7})
    print "************************************************************************"
    test2((1,2,3,4),{"a":5,"b":6,"c":7})
    print "*************************************************************************"
    test3((1,2,3,4),**{"a":5,"b":6,"c":7})
