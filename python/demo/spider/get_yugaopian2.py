#-*- encoding:utf-8 -*-
'''
Created on 2016��4��28��

@author: dedong.xu
'''

import urllib, urllib2
import urlparse
from bs4 import BeautifulSoup
import time
import re
import os
import json



"""
指定一个主页面入口，然后去匹配并获得相应的url，如果是合法的新的url，然后再去进行解析，直到所有的合法的url被解析完。
使用BeautifulSoup来解析html文档
"""

base_main_url = r"http://www.yugaopian.com"
highlight_url = base_main_url + "/highlight"
base_download_url= "http://www.yugaopian.com/?view=api&mode=download-data&ttid="
movie_path = "d:/test/movie/soup"


"""url管理器"""
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        
    def add_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    
    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)
    
    def has_url(self):
        return len(self.new_urls) != 0
    
    def get_url(self):
        url = self.new_urls.pop()
        if url.endswith("/") or url.endswith("\\"):
            url = url [:-1]
        self.old_urls.add(url)
        return url

"""url下载器"""
class UrlDownloader(object):
    def url_download(self, url):
        if url is None:
            return 
        response = urllib2.urlopen(url)
        if response.code != 200:
            return
        return response.read()


"""html解析器"""
class HtmlParser(object):
    def get_movie(self, download_url):
        if download_url is None:
            return
        try:
            urllib.urlretrieve(download_url, os.path.join(movie_path,os.path.basename(download_url)))#, Schedule)
        except Exception as e:
            print str(e)

    def get_download_url(self, base_main_url, soup):
        link = soup.find("a", href=re.compile(r"/download/\d+"))
        #try:
        if link is not None:
            print "link is: ", link
            print "title is: ", link["title"]
            new_url = link["href"]
            new_full_url = urlparse.urljoin(base_main_url, new_url)
            #except Exception as e:
            #    new_full_url = None
        else:
            new_full_url = ""
        return new_full_url
    
    def get_all_movie_urls(self, soup):
        new_highlight_urls = set()
        links = soup.find_all("a", href = re.compile(r"/movie/\d+"))
        for link in links:
            new_full_url = urlparse.urljoin(base_main_url, link["href"])
            new_highlight_urls.add(new_full_url)
        return new_highlight_urls
        
    def parser(self, html_doc):
        if html_doc is None:
            return
        try:
            soup = BeautifulSoup(html_doc, "html.parser", from_encoding = "utf-8")
        except Exception as e:
            print "parser error: ", str(e)
            soup = None
        return soup


"""主程序"""
class SpiderMain(object):
    def __init__(self):
        self.urlmanager = UrlManager()
        self.urldownloader = UrlDownloader()
        self.htmlparser = HtmlParser()
        
        
    def craw(self, highlight_url, base_download_url):
        num = 1
        self.urlmanager.new_urls.add(highlight_url)
        while self.urlmanager.has_url():
            #try:
                url = self.urlmanager.get_url()
                #解析预告片首页的所有预告片信息
                highlight_html_doc = self.urldownloader.url_download(url)
                highlight_soup = self.htmlparser.parser(highlight_html_doc)
                if highlight_soup is None:
                    return 
                new_movie_urls = self.htmlparser.get_all_movie_urls(highlight_soup)
                for movie_url in new_movie_urls:
                    print "*"*100
                    print "第 %d次下载!!!" % num
                    movie_html_doc = self.urldownloader.url_download(movie_url)
                    movie_soup = self.htmlparser.parser(movie_html_doc)
                    if movie_soup is None:
                        return
                    print "movie_url: ", movie_url
                    new_download_url = self.htmlparser.get_download_url(base_main_url, movie_soup)
                    print "new_download_url is : ", new_download_url
                    download_data_url = base_download_url + os.path.basename(new_download_url)   #基url + movie id号
                    download_url_content = self.urldownloader.url_download(download_data_url)
                    try:
                        download_url = None
                        #download_url = json.loads(download_url_content)[0]["movurl"]    #这句代码解析json格式的数据并将电影下载链接获取到
                        for record in json.loads(download_url_content):
                            if record["movurl"].endswith(".flv"):
                                download_url = record["movurl"]
                                break
                    except Exception as e:
                        download_url = None
                        print str(e)
                    print download_url
                    print movie_url
                    self.htmlparser.get_movie(download_url)
                    
                    
                    if num == 30:
                        break
                    num += 1
            #except Exception as e:
            #    print str(e), "  crawed failed!!!"


def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    #time.sleep(2)
    if per > 100 :
        per = 100
    print '%.2f%%' % per

              
if __name__ == "__main__":
    obj_spider = SpiderMain()
    obj_spider.craw(highlight_url, base_download_url)



