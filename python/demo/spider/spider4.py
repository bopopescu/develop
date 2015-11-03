#-*- encoding:utf-8 -*-
import urllib
import urllib2
import re
content = urllib2.urlopen("http://www.letv.com/").read()
#fp = open("test.html","r")
#content = fp.read()

#print re.findall("<title.*?\/title>", content) == re.findall("<title>.*?</title>", content)


#for i in re.findall("[^(<!--.*-->)]<a.*?\/a>", content.split("TOP热播")[1].split("播放记录")[0]):
for i in re.findall("[^(<!--.*-->)]<a.*?\/a>", content.split("TOP热播")[1].split("播放记录")[0]):
    #print i
    print re.search("(?<=>).*(?=<)",i).group()



info = urllib2.urlopen("http://www.letv.com/").info()
print info

getcode = urllib2.urlopen("http://www.letv.com/").getcode()
print getcode

geturl = urllib2.urlopen("http://www.letv.com/").geturl()
print geturl

content = urllib2.urlopen("http://www.letv.com/").readlines()
print content
