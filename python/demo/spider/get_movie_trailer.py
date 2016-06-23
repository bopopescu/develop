#-*- encoding:utf-8 -*-

'''
Created on 2016年6月21日

@author: dedong.xu
'''
"""
        指定一个主页面入口，然后去匹配并获得相应的url，如果是合法的新的url，然后再去进行解析，直到所有的合法的url被解析完
"""

import urllib, urllib2
import urlparse
import time
import os
import re
from bs4 import BeautifulSoup

library_url = r"http://www.hd-trailers.net/library/"
base_movie_url = r"http://www.hd-trailers.net"
base_movie_path = r"d:\test\hd_trailers"
library_list = ["0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

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
            url = url[:-1]
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
    
"""url解析器"""
class HtmlParser(object):   
    def parser(self, html_doc):
        if html_doc is None:
            return
        try:
            soup = BeautifulSoup(html_doc, "html.parser", from_encoding = "utf-8")
        except Exception as e:
            print "parser error: ", str(e)
            soup = None
        return soup
    
    def get_all_movie_link_urls(self, soup):
        movie_urls = set()
        links = soup.find("table", class_ = "libraryTextIndexList").find_all("a")
        for link in links: 
            try:
                movie_urls.add(link["href"])
            except Exception, e:
                print str(e)
        return movie_urls
        
    def get_movie_info(self, soup):
        movie_name_obj = soup.find("table", class_ = "mainTopTable").find("h1", class_ = "previewTitle", itemprop = "name")
        if movie_name_obj:
            movie_name = movie_name_obj.text
        else:
            movie_name = None
        other_info_soup = soup.find("table", class_ = "bottomTable")
        trailer_obj = other_info_soup.find("td", id = "Trailers").find("h2")
        if trailer_obj:
            trailer = trailer_obj.text
        else:
            trailer = None
        tr_obj = other_info_soup.find_all("tr", itemprop = "trailer")
        movie_other_info = []
        for each_tr_obj in tr_obj:
            each_movie_other_info = []
            td_obj = each_tr_obj.find_all("td")
            for each_td_obj in td_obj:
                if not each_td_obj.text.strip():
                    continue
                if each_td_obj.text in ("480p", "720p", "1080p"):
                    try:
                        movie_download_url = each_td_obj.find("a")["href"]
                    except Exception, e:
                        movie_download_url = None
                        print str(e)
                    cur_movie_path = self.create_movie_path(movie_name)
                    movie_local_url = self.download_movie(movie_download_url, cur_movie_path)
                    each_movie_other_info.append((each_td_obj.text, movie_local_url))
                else:
                    each_movie_other_info.append(each_td_obj.text)
            movie_other_info.append(each_movie_other_info)    
        return {"movie_name": movie_name, "movie_other_info": movie_other_info}
    
    def create_movie_path(self, movie_name):
        if movie_name is None:
            return   
        for each_str in ['\\','/',':','*','?','"','<','>','|']:
            if each_str in movie_name:
                movie_name = movie_name.replace(each_str, "-")
        cur_movie_path = os.path.join(base_movie_path, movie_name) 
        if not os.path.exists(cur_movie_path):
            os.mkdir(cur_movie_path)
        return cur_movie_path
    
    def download_movie(self, download_url, movie_path):
        if download_url is None or movie_path is None:
            return
        try:
            movie_local_url = os.path.join(movie_path,os.path.basename(download_url))
            if not os.path.exists(movie_local_url):
                urllib.urlretrieve(download_url, movie_local_url)#, Schedule)
        except Exception, e:
            movie_local_url = None
            print str(e)
        return movie_local_url
            

"""主程序"""
class SpiderMain(object):
    def __init__(self):
        self.urlmanager = UrlManager()
        self.urldownloader = UrlDownloader()
        self.htmlparser = HtmlParser()
        
    def craw(self, library_url, library_list):
        print "begin to craw!"
        for each_library in library_list:
            """对每一个字母开头的页面解析"""
            library_page = urlparse.urljoin(library_url, each_library)
            library_html_doc = self.urldownloader.url_download(library_page)
            library_parser_page = self.htmlparser.parser(library_html_doc)
            
            if library_parser_page is None:
                return
            print library_page
            movie_link_urls = self.htmlparser.get_all_movie_link_urls(library_parser_page)
            for each_movie_url in movie_link_urls:
                movie_url = urlparse.urljoin(base_movie_url,each_movie_url)
                print movie_url
                #movie url like: http://www.hd-trailers.net/movie/1/ 
                movie_html_doc = self.urldownloader.url_download(movie_url)
                movie_parser_page = self.htmlparser.parser(movie_html_doc)
                #get movie info
                movie_info = self.htmlparser.get_movie_info(movie_parser_page)
                print movie_info
            
            
def Schedule(a, b, c):
    '''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a *b / c
    if per > 100:
        per = 100
    print "%.2f%%" % per
    
    
if __name__ == "__main__":
    obj_spider = SpiderMain()
    obj_spider.craw(library_url, library_list)
    print "Game Over!!!"