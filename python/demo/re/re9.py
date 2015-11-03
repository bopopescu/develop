#-*- encoding:utf-8 -*-

"""
   在正则表达式中，可以使用()来将部分正则表达式分组且编号，编号从1开始，使用数字来使用，
   例如1 2 3，(?p<name>)还可以给分组命名, 使用（？p=name）来使用命名的组。
"""

import re

pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"

mystr = "2015-10-20, I am very happy!"

m = re.match(pattern, mystr)

if m:
    print m.group()




