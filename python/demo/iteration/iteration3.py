#-*- encoding:utf-8 -*-

"""
    文件对象生成的迭代器会自动调用readline()的方法，这样循环遍历就可以访问文本文件的所有行。
"""

myfile = open('iteration1.py')
for each_line in myfile:
    print each_line



fp = open('iteration1.py',"r")
content = fp.read()
fp.close()
print content
