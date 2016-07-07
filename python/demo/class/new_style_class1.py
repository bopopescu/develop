#-*- encoding:utf-8 -*-
'''
Created on 2016��4��5��
@author: dedong.xu
'''
# -*- coding:utf-8 -*-  
class A(object):
    attr = "a"
    
class E(object):
    attr = "e"
    
class B(A):
    pass

class C(E):
    attr = "c"
    
class D(B,C):
    pass

d = D()
print d.attr
"""
print type(A)
#print A.__class__
print type(B)
print type(C)
print 999999999, type(D), 999999999
print type(E)
print E.__class__
"""