#-*- encoding:utf-8 -*-

"""
    插入排序
"""

list1 = [5,1,2,3,7,8,18,68,48,49,58,38]

def insertion_sort(sort_list):
    iter_len = len(sort_list)
    if iter_len < 2:
        return sort_list
    for i in range(1, iter_len):
        key = sort_list[i]
        j = i - 1
        while j>=0 and sort_list[j]>sort_list[i]:
            sort_list[j+1] = sort_list[j]
            j -= 1
        sort_list[j+1] = key
    print sort_list
    return sort_list


if __name__ == "__main__":
    insertion_sort(list1)
