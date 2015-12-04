#-*- encoding:utf-8 -*-

import urllib

print "\nurllib.quote(string[, safe])：对字符串进行编码。参数safe指定了不需要编码的字符\n"
astr = urllib.quote('this is "K"')
print urllib.quote('this is "K"','this is "K"')
print astr

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "\nurllib.unquote(string) ：对字符串进行解码\n"
bstr = urllib.unquote(astr)
print bstr


print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "\nurllib.quote_plus(string [ , safe ] ) ：与urllib.quote类似，但这个方法用'+'来替换' '，而quote用'%20'来代替' '\n"
cstr = urllib.quote_plus('this is "K"')
print cstr

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "\nurllib.unquote_plus(string ) ：对字符串进行解码\n"
dstr = urllib.unquote_plus(cstr)
print dstr

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "urllib.urlencode(query[, doseq])：将dict或者包含两个元素的元组列表转换成url参数。"
print "例如 字典{'name': 'wklken', 'pwd': '123'}将被转换为'name=wklken&pwd=123'"
params = {"a":"1","b":"2","c":"3"}
print urllib.urlencode(params)

params = [("a","1"),("b","2"),("c","3")]
print urllib.urlencode(params)

params = (("a","1"),("b","2"),("c","3"))
print urllib.urlencode(params)

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "urllib.pathname2url(path)：将本地路径转换成url路径\n"
l2u = urllib.pathname2url(r"d:\a\test.py")
print l2u
l2u = urllib.pathname2url("d:/a/test.py")
print l2u

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "urllib.url2pathname(path)：将url路径转换成本地路径"
print urllib.url2pathname(l2u)









