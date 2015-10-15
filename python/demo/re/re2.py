#-*- encoding:utf-8 -*-

import re

strs = "<title>xdd</title><div>11</div>"
print re.search("<.*>",strs).group()       #贪婪匹配，匹配整个字符串
print re.search("<.+>",strs).group()       #贪婪匹配，匹配整个字符串
print re.search("<.*?>",strs).group()      #非贪婪匹配，只匹配到<title>
print re.search("<title>.*?</title>",strs).group()      #非贪婪匹配，只匹配到<title>
print re.search("<.+?>",strs).group()      #非贪婪匹配，只匹配到<title>
print re.search("<.??>",strs)              #匹配结果为空

print re.findall("a{2,5}","aaaaaaaaaa")    #匹配2到5次，尽可能多的匹配
print re.findall("a{2,5}?","aaaaaaaaaa")   #匹配2到5次，尽可能少的匹配 
