#-*- encoding:utf-8 -*-
"""
    冒泡排序的三种方法，其中两种正序排列和一种倒序排列
"""

list1 = [3,7,8,6,89,109,1,0,65,2,86,22,135,111]
	
#经典冒泡排序	
def maopao1():
    """ 正序排列 """
    for i in xrange(len(list1)-1):
        for j in xrange(i, len(list1)-1):
            if list1[i]>list1[j]:
                list1[i],list1[j] = list1[j], list1[i]
    print list1
	
#经典冒泡排序	
def maopao2():
    """ 倒序排列 """
    for i in xrange(len(list1)-1, -1, -1):
        for j in xrange(i):
            if list1[i]>list1[j]:
                list1[i],list1[j] = list1[j], list1[i]
    print list1
	

#另一种冒泡排序
def maopao3():
    """ 正序排列 """
    flag = 1
    while flag:
        flag = 0
        for i in xrange(len(list1)-1):
            if list1[i] > list1[i+1]:
                list1[i], list1[i+1] = list1[i+1], list1[i]
                flag = 1
                break

    print list1
	
	
if __name__ == "__main__":
    maopao1()
    maopao2()
    maopao3()

























































def maopao():
    for i in xrange(len(list1)-1):
        for j in xrange(len(list1)-i-1):
            if list1[j] > list1[j+1]:
                list1[j], list1[j+1] = list1[j+1],list1[j]
    print list1
