#-*- encoding:utf-8 -*-

import urllib
url = "http://www.baidu.com"
print urllib.urlretrieve(url, "d:/test/baidu.txt")
