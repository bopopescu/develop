#-*- encoding:utf-8 -*-

list1 = [7,8,6,89,109,1,0,65,2]
print list1

#经典冒泡排序
def maopao1():
    for i in xrange(len(list1)-1):
        for j in xrange(len(list1)-1):
            if list1[j]>list1[j+1]:
                list1[j],list1[j+1] = list1[j+1], list1[j]
    print list1


#另一种冒泡排序
def maopao2():
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

























































def maopao():
    for i in xrange(len(list1)-1):
        for j in xrange(len(list1)-i-1):
            if list1[j] > list1[j+1]:
                list1[j], list1[j+1] = list1[j+1],list1[j]
    print list1
