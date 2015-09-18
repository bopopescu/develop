#-*- encoding:utf-8 -*-
a=1
x=2
y=3
"""
    当 a为真时，输出x，否则输出y
"""

print "first: ", a and x or y
print "second: ", (a and [x] or [y])[0]
