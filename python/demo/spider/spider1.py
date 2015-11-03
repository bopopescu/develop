#-*- encoding:utf-8 -*-
import urllib2
url = "http://www.baidu.com"
page = urllib2.urlopen(url)

print "读取页面的内容"
print page.read()[:100]
print "*******************************************"
page = urllib2.urlopen(url)
print page.readline()
print "*******************************************"
print page.readlines()[:5]
print "*******************************************"
print "返回一个httpllib.HTTPMessage对象，表示远程服务器返回的头信息"
print page.info()
print "返回Http状态码。如果是http请求，成功则返回200,网址未找到则返回404"
print page.getcode()
print type(page.getcode())
if page.getcode() == 200:
    print 11111111111111111111111
print "返回请求的 url"
print page.geturl()
