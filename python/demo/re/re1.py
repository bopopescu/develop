#-*- encoding:utf-8 -*-
import re

print re.findall("a*","  ")

strs = "sdgetrndbsge"

pattern = r"^s[asdgeyitr]{1,}"

result = re.findall(pattern,strs)
print result
print type(result)
for i in result:
    print i,

if result:
    print 99999999

print "**************************"


#Python提供了两种不同的原始操作：match和search。match是从字符串的起点开始做匹配，而search（perl默认）是从字符串做任意匹配.
#注意：当正则表达式是' ^ '开头时，match与search是相同的。match只有当且仅当被匹配的字符串开头就能匹配 或 从pos参数的位置开始就能匹配 时才会成功。
#re.match(patterns, strs)
#re.search(patterns, strs)

print re.match("c","abcdef")
print re.match("c","cabdef")
print re.search("c","abcdef")
print re.search("c","abcdefccc").group()
print re.findall("c","abcdefccc")

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#re.compile(pattern, flags=0)
#编译正则表达式，返回RegexObject对象，然后可以通过RegexObject对象调用match()和search()方法。

prog = re.compile("a")
result1 = prog.match("asdc")
print result1

result2 = re.match("a","asdc")
print result2
print result1 == result2
print "*****************************************************************************************"

#re.compile返回regrexobject对象， 用来重复使用regrexobject；
pat = re.compile("c")

print "pat: ", pat
print pat.match("asdcvb")
print pat.match("asdcvb",1)
print pat.match("asdcvb",2)
print pat.match("asdcvb",3)  #这个3就是pos参数的值
print pat.match("asdcvb",3).group(),type(pat.match("asdcvb",3).group()), "   group,   返回被 RE 匹配的字符串"
print pat.match("asdcvb",3).start(),type(pat.match("asdcvb",3).start()), "   start,   返回匹配开始的位置"
print pat.match("asdcvb",3).end(),type(pat.match("asdcvb",3).end()),   "   end,     返回匹配结束的位置"
print pat.match("asdcvb",3).span(),type(pat.match("asdcvb",3).span()),  "   span     返回一个元组包含匹配 (开始,结束) 的位置"

#group()返回被 RE 匹配的字符串
#start()返回匹配开始的位置
#end()返回匹配结束的位置
#span()返回一个元组包含匹配 (开始,结束) 的位置

print "++++++++++++++++++++++++++++++++++++++++"


#re.split(pattern, string, maxsplit=0)
#通过正则表达式将字符串分离，如果用括号将正则表达式括起来，那么匹配的字符串也会被列入到list中返回。
#maxsplit是分离的次数，maxsplit=1分离一次，默认为0，不限制次数

print re.split("\W+","aa,sd,a,sda")

print re.split("\W+","aa,sd,a,sda",maxsplit = 2)

#如果用括号将正则表达式括起来，那么匹配的字符串也会被列入到list中返回
print re.split("(\W+)","aa,sd,a,sda")

print "aasdasda".split("aasdasda")


#re.sub(pattern, repl, string, count=0, flags=0)
#找到 RE 匹配的所有子串，并将其用一个不同的字符串替换。
#可选参数 count 是模式匹配後替换的最大次数；count 必须是非负整数。缺省值是 0 表示替换所有的匹配。
#如果无匹配，字符串将会无改变地返回。

src_str = "asd23asd"
print "原始串为： ", src_str
print re.sub("\d+","1",src_str), "   将尽可能多的数字替换为1"
print re.sub("[asd]+","1",src_str)
print re.sub("asd","1",src_str,count=0)
print re.sub("asd","1",src_str,count=-1)
print re.sub("asd","1",src_str,count=1)
print re.sub("asd","1",src_str,count=2)
print re.sub("asd","1",src_str,count=3)
print re.sub("asd","1",src_str,count=4)

#re.IGNORECASE用来在匹配时忽略大小写
print re.findall("[A-Z]+","asfas1231ada",re.IGNORECASE), "   不区分大小写，返回一个列表" #re.findall匹配的结果是一个列表
print re.search("[A-Z]+","asfas",re.IGNORECASE).group(), "   不区分大小写，返回一个字符串"  #re.search匹配的结果,如果匹配不成功，则返回none；否则返回matchobject，一个对象

print "************************************************************************"

#re.MULTILINE对$的影响
print re.findall("foo.$","foo1\nfoo2\nfoo3\nfoo4"), "   匹配最后一行的结果"
print re.findall("foo.$","foo1\nfoo2\nfoo3\nfoo4", re.MULTILINE), "   匹配所有行的结果"
print re.search("foo.$","foo1\nfoo2\nfoo3\nfoo4").group(), "   匹配最后一行的结果"
print re.search("foo.$","foo1\nfoo2\nfoo3\nfoo4", re.MULTILINE).group(), "   匹配第一行的结果"

print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

#没有$符号的情况下
print re.findall("foo.","foo1\nfoo2\nfoo3\nfoo4"), "   匹配所有行的结果"
print re.findall("foo.","foo1\nfoo2\nfoo3\nfoo4", re.MULTILINE), "   匹配所有行的结果"
print re.search("foo.","foo1\nfoo2\nfoo3\nfoo4").group(), "   匹配最后一行的结果"
print re.search("foo.","foo1\nfoo2\nfoo3\nfoo4", re.MULTILINE).group(), "   匹配第一行的结果"


#re.findall 分组

print re.findall("(cc)(aa)", "ccaadacciuccaaojccjjopaaccaa")
print re.search("(cc)(aa)", "ccaadacciuccaaojccjjopaaccaa").group()

#最后：如果能用字符串的方法，就不要选择正则表达式，因为字符串方法更简单快速。

#返回匹配到的所有命名子组的字典。Key是name值，value是匹配到的值
m=re.match("(?P<first>\w+) (?P<secode>\w+)","hello world")
print m.groupdict()
