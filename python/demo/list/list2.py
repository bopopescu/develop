#-*- encoding:utf-8 -*-

"""
    对列表排序，例如["a1","a100","a5","a2","a7"]最终排序成["a1","a2","a5","a7","a100"]
"""


li = ["a1","a100","a5","a2","a7"]
temp_new_li = []
new_li = []
for i in li:
    new_i = int(i.replace("a",""))
    print new_i,
    temp_new_li.append(new_i)


print sorted(temp_new_li)
for i in sorted(temp_new_li):
    print i,"a" + str(i)
    new_li.append("a" + str(i))


print new_li
