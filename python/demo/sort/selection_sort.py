#-*- encoding:utf-8 -*-
"""
    选择排序
"""

list1 = [56,3,7,1,2,87,99,57,123,67]

def select_sort(sort_list):
    if len(sort_list) < 2:
        return sort_list

    for i in xrange(len(sort_list)-1):
        smallest = sort_list[i]
        location = i
        for j in xrange(i, len(sort_list)):
            if sort_list[j] <smallest:
                smallest = sort_list[j]
                location = j

        if i != location:
            sort_list[i], sort_list[location] = sort_list[location], sort_list[i]

    print sort_list
    return sort_list


def test(li):
   for i in xrange(len(li)-1):
     s = li[i]
     l = i
     for j in xrange(i, len(li)):
         if li[j] < s:
             s=li[j]
             l=j
   print li




if __name__ == "__main__":
    #select_sort(list1)
    test(list1)
