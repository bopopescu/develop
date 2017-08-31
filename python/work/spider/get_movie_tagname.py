#-*- encoding:utf-8 -*-
'''
Created on 2017-04-21

@author: dedong.xu

@description: 爬取电影的标签
'''

#standard lib
import re
import json
import time
import urllib2
import logging
import random

#3rd lib
from lxml import etree
from poster.streaminghttp import register_openers

base_get_url = "http://10.10.3.196:8080/tool/vmdbid_relationid?count=1&start="
post_url = "http://10.10.3.196:8080/tool/vmdbidtag"
douban_id = "26260853"
base_url = "https://movie.douban.com/subject"
LOG_FILENAME = "log.txt"
time_list = [5, 10, 15, 20, 25, 30]
useragent_list = ["Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
                  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) ",
                  "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT) ",
                  "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1 ",
                  "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
                  "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12",
                 ]


def log(info):
    """ 记录log日志 """
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = "a", format = "%(asctime)s : %(message)s")
    logging.info(info)  
    
    
class PostAccessUrl(object):
    """ HTTP POST请求 """
    def access_url(self, url, params):
        """ 访问url """
        try:
            register_openers()
            params = json.dumps(params)
            req = urllib2.Request(url, data = params, headers = {"Content-Type": "application/json"})
            response = urllib2.urlopen(req)
            return response.read()
        except Exception, e:
            return str(e)
        

class GetAccessUrl(object):
    """ HTTP GET 请求"""
    def access_url(self, url, useragent):
        """ 访问url """
        if url is None:
            return
        try:
            print useragent
            request = urllib2.Request(url)
            request.add_header("User-Agent", useragent)
            res = urllib2.urlopen(request)
            if res.code != 200:
                return
        except Exception, e:
            return
        return res.read()
    
    
    def access_url2(self, url):
        """ 访问url """
        if url is None:
            return
        try:
            res = urllib2.urlopen(url)
            if res.code != 200:
                return
        except Exception, e:
            return
        return res.read()
    
    
class UrlDownloader(GetAccessUrl):
    """ url下载器 """  
    def __init__(self):  
        """ 将父类的方法改名 """
        self.download = super(self.__class__, self).access_url
    
    
class HtmlParser_By_Re(object):
    """ html解析器 """
    def get_tags(self, html_doc):
        """ 使用正则表达式解析 """
        p1 = r'<div class="tags-body">\s*(<a href="/tag/[\d\D]+?" class="">[\d\D]+?</a>\s*)+\s*</div>'
        res = re.search(p1, html_doc)
        if res:
            p2 = r'<a href="/tag/[\d\D]+?" class="">([\d\D]+?)</a>\s*'
            return re.findall(p2, res.group())
        return []
        
        
class HtmlParse_By_lxml(object):
    """ html解析器 """
    def parser(self, html_doc):
        """ 解析html文档 """
        if html_doc is None:
            return
        try:
            page = etree.HTML(html_doc.decode('utf-8'))
        except Exception as e:
            print "parser error: ", str(e)
            page = None
        return page
    
    def get_tags(self, page):
        """ 获取标签名字 """
        res = page.xpath(u'//div[@class="tags-body"]')
        """
        #这种方法也可以
        for record in res:
            for i in record.getchildren():
                print i.text,
        return [i.text for record in res for i in record.getchildren()]
        """       
        return [i.text for record in res for i in record.findall("a")]
                
                
class SpiderMain(object):
    """ 爬虫主程序 """
    def __init__(self):
        """ 初始化变量 """
        self.ud = UrlDownloader()
        self.hpbr = HtmlParser_By_Re()
        self.hpbl = HtmlParse_By_lxml()
        self.gau = GetAccessUrl()
        self.pau = PostAccessUrl()
        
    def crawl_test(self, url=None):
        n = 1
        while 1:
            useragent= random.choice(useragent_list)
            url = "https://movie.douban.com/subject/26260853"
            html_doc = self.ud.download(url, useragent)
            page = self.hpbl.parser(html_doc)
            tag_list = self.hpbl.get_tags(page)
            n += 1
        
    def crawl(self, url, base_get_url, post_url):
        """ 程序入口 """
        n = 10
        while 1:
            get_url = base_get_url + str(n)
            res = json.loads(self.gau.access_url2(get_url))
            if res["subjects"]:
                doubanid = res["subjects"][0]["doubanid"]
                vmdbid = res["subjects"][0]["vmdbid"]
                url = "%s/%s" % (base_url, doubanid)
                useragent= random.choice(useragent_list)
                html_doc = self.ud.download(url, useragent)
                page = self.hpbl.parser(html_doc)
                tag_list = self.hpbl.get_tags(page)
                params = {"subjects": []}
                di= {"vmdbid": vmdbid, "tags": tag_list}
                params["subjects"].append(di)
                res = self.pau.access_url(post_url, params)
                sleep_time = random.choice(time_list)
                time.sleep(sleep_time)
                n += 1                
            else:
                break
            
         
        
    
if __name__ == "__main__":
    spider = SpiderMain()
    spider.crawl(base_url, base_get_url, post_url)

    
    
    
