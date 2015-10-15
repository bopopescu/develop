#-*- encoding:utf-8 -*-

import re

strs = "(fw467%&*@#$%^<>?.)/)"
print re.search("(.*)",strs).group(), "  #匹配括号内的所有字符"

print re.search("(?#fw)",strs).group(),  "  #注释，忽略括号内的内容"      
print "**********************************************************"

print "#匹配表达式test之前的字符串，在字符串xddtest中(?=test)会匹配xdd"
print re.search(".*(?=test)","xddtest").group()
print re.search("xdd(?=test)","xddtest").group() 

print "#匹配后面不跟表达式test的字符串，如果字符串xddtest后面不是test，那么(?!test)会匹配xdd"
print re.search("xudedong(?!=test)","xudedong7678st").group()
print re.search("\w+(?!=test)","xudedong7678st").group()


print "#跟在表达式’…’后面的字符串符合括号之后的正则表达式"
print "#截头去尾   截头(?<=abc)， 去尾(?=a)"
print re.search("(?<=abc)\w*(?=a)","7777abcdefabc").group(),11111111111111

print "#跟在表达式’…’后面的字符串符合括号之后的正则表达式"
print re.search("(?<=abcdef)\w+","abcdefurthjrthjth14124312341rthrt").group()

print "#括号之后的正则表达式不跟在’…’的后面,这里是...表示的是 xdd"
print re.search("(?<!xdd)\w+","xdd13123131a4312341rthrt").group()



