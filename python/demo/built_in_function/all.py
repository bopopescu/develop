#-*- encoding:utf-8 -*-

'''
Created on 2016-09-06

@author: dedong.xu
'''
iter_list = [1,2,3,4,5,0]

def all(iter_list):
    """ 迭代序列为空或者迭代序列里只要有一个元素为False，则返回False """
    for ele in iter_list:
        if not ele:
            return False
    return True


if __name__ == "__main__":
    print all(iter_list)