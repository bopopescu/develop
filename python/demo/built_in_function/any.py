#-*- encoding:utf-8 -*-

'''
Created on 2016-09-06

@author: dedong.xu
'''

iter_list = ["", 0, None, False, 9]

def any(iter_list):
    """ 迭代序列为空或者迭代序列里只要有一个元素为True，则返回True """
    for ele in iter_list:
        if ele:
            return True
    return False

if __name__ == "__main__":
    print any(iter_list)