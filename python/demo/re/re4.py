#-*- encoding:utf-8 -*-


import re
#只在字符串开头进行匹配
print re.search("\Aada", "adasdsd").group()

print re.search("\s+", "    !@#$%^&*()_<>?HJKL:OP{}|adasdsd").group()


#re.compile(pattern[, flags])
#把正则表达式的模式和标识转化成正则表达式对象，供 match() 和 search() 这两个函数使用。

#以下两种用法结果相同

compiled_pattern = re.compile("\w+") 
result = compiled_pattern.match("asdas").group()
print result
result = re.match("\w+", "asdas").group()
print result



pat = re.compile("a")
print pat.search("asdfg").group()
print pat.search("asdfg",0).group()
print pat.search("asdfg")
print pat.search("asdfg",0)
if pat.search("asdfg").group() == pat.search("asdfg",0).group():
    print 88

#re.split(pattern, string[, maxsplit=0, flags=0])
#此功能很常用，可以将将字符串匹配正则表达式的部分割开并返回一个列表。对 RegexObject，有函数：
print re.split("\d+", "qw1qw2qw")
print re.split("\d+", "qw1qw2qw",maxsplit=1)
#对于一个找不到匹配的字符串而言，split 不会对其作出分割
print re.split("aaa+", "qw1qw2qw")

print "************************************************************"

print re.split('\W+', 'test,test,test')

print re.split('(\W+)', 'test,test,test')

print re.split('\W+',' test, test, test.',1)

print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

#re.sub(pattern, repl, string[, count, flags])
#在字符串 string 中找到匹配正则表达式 pattern 的所有子串，用另一个字符串 repl 进行替换。如果没有找到匹配 pattern 的串，则返回未被修改的 string。Repl 既可以是字符串也可以是一个函数。对于 RegexObject 有
print "替换字符串，只替换一次： ",re.sub("\d","a","1q2w3e",count=1)
print "替换字符串，替换所有符合条件的串： ", re.sub("\d","a","1q2w3e")
p = re.compile("\d")
print "先将正则表达式编译，再进行替换：", p.sub("a", "0s9d")


#re.subn(pattern, repl, string[, count, flags])
#该函数的功能和 sub() 相同，但它还返回新的字符串以及替换的次数。同样 RegexObject 有：
#subn(repl, string[, count=0])
print "---------------------------------------------------------------------"
print "替换字符串，只替换一次： ",re.subn("\d","a","1q2w3e",count=1)
print "替换字符串，替换所有符合条件的串： ", re.subn("\d","a","1q2w3e")
p = re.compile("\d")
print "先将正则表达式编译，再进行替换：", p.subn("a", "0s9d")
















