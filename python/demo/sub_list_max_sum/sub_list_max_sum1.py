#-*- encoding:utf-8 -*-

'''
Created on 2015-4-21

@author: dedong.xu
'''

li = [-9,-1,5,3,-7,3,-3,10,-14,-16]

def sub_list_max_sum1(li):
    curSum = 0
    maxSum = 0
    L1 = 0
    L2 = 0
    for i in li:
        curSum += i
        if curSum < 0:
            curSum = 0
            L1 = li.index(i) + 1
        else:
            if maxSum < curSum:
                maxSum = curSum
                L2 = li.index(i)
    if maxSum == 0:
        L2 = []
        maxSum = li[0]
        for i in xrange(len(li)):
            if li[i] > maxSum:
                maxSum = li[i]
                
    print maxSum
    print li[L1:L2 + 1]



li = [-9,-1,-5,-3,-7,3,-2,10,14,-16]
"""该函数可以获取到列表里面子列表的最大和，还有起始和结束下标，以及子列表"""
def sub_list_max_sum(li):
    maxSum = 0
    curSum = 0
    start_index = 0
    end_index = 0
    for i in xrange(len(li)):
        curSum += li[i]
        if curSum < 0:
            curSum = 0
            start_index = i + 1
            continue
        
        if maxSum < curSum:
            maxSum = curSum
            end_index = i
                
    if maxSum == 0:
        maxSum = li[0]
        for i in xrange(len(li)):
            if maxSum < li[i]:
                maxSum = li[i]
    print "最大和为: ", maxSum   
    print "开始下标: ", start_index, ", 结束下标: ", end_index   
    print "子列表为: ", li[start_index: end_index+1] 



if __name__ == "__main__":
    sub_list_max_sum(li)























