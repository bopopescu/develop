#-*- encoding:utf-8 -*-

"""
    假定数据已经按从小到大的顺序排好了
"""
list1 = [1,2,4,5,7,9,12,23,45,56,67,78]



def my_sort(data):
    new_list = []
    if data < list1[0]:
        new_list.append(data)
        for i in list1:
            new_list.append(i)
    elif data > list1[-1]:
        list1.append(data)
        new_list = list1
    else:
        if data in list1:
            index = list1.index(data)
            list1.insert(index, data)
            new_list = list1
        else:
            for i in xrange(len(list1)-1):
                if list1[i] < data < list1[i+1]:
                    new_list.extend(list1[0:i+1])
                    new_list.append(data)
                    new_list.extend(list1[i+1:])

    print new_list
        
            
if __name__ == "__main__":
    print list1
    my_sort(0)
    print "************************"
    my_sort(100)
    print "************************"
    my_sort(12)
    print "************************"
    my_sort(50)
    
