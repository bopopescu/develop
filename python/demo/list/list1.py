#-*- encoding:utf-8 -*-
"""
    这里的教训是：不要一边遍历 list，一边修改它本身。  还有   不要在循环的时候删除，否则就会出现index问题
"""

array = [i for i in xrange(10) if i%2==0]
array = range(10)
print array
#所以这里用了array[:]
for i in array[:]:
    if i < 5:
        print i, array.index(i)
        array.pop(0)
        print array



