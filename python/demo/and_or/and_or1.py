#-*- encoding:utf-8 -*-
a=1
x=0
y=3
"""
    当 a为真时，输出x，否则输出y
"""

#这种写法是不对的，x为0时，输出有误
print "first: ", a and x or y
#这种写法是正确的，可以保证x为0时，仍能正确输出结果
print "second: ", (a and [x] or [y])[0]
