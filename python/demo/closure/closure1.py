#-*- encoding:utf-8 -*-
"""
    这是一个闭包的简单例子
"""


def hellocounter(name):
    count = [0]
    def counter():
        print 99999999
        count[0] += 1
        #如果使用逗号连接的话，字符串可以直接跟整型连接。逗号连接中间会多出一个空格来
        print 'Hello, ', name, ',', count[0] , ' access!'
        print 'Hello, '+ name+ ','+ str(count[0]) + ' access!'
    return counter


hello = hellocounter("xudedong")

print hello
hello()
hello()
hello()



