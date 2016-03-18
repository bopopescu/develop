#-*- encoding:utf-8 -*-
'''
Created on 2016��3��18��

@author: dedong.xu
'''
from bs4 import BeautifulSoup
import urllib2
import urlparse
import re

"""
   一个简单的爬虫程序，主要分为主程序， url管理器， url下载器，解析器以及输出器(将爬取的内容输出到html文件里，方便查看)
"""

""" url管理器 """
class UrlManager(object):
    def __init__(self):
        self.new_urls = set() 
        self.old_urls = set()
    
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
        
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
            
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
            
    def has_new_url(self):
        if len(self.new_urls) != 0:
            return True
        else:
            return False
        
    def has_new_url_test(self):
        return len(self.new_url) != 0
        
""" url下载器 """
class HtmlDownloader(object):
    
    def download(self, url):
        if url is None:
            return None
        
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        
        return response.read()
        
        
"""解析器"""
class HtmlParser(object):
    
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        #/vies/123.htm
        links = soup.find_all("a", href = re.compile(r"/view/\d+\.htm"))
        for link in links:
            new_url = link["href"]
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
    
    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data["url"] = page_url
        
        title_node = soup.find("dd", class_ = "lemmaWgt-lemmaTitle-title").find("h1")
        
        if title_node:
            res_data["title"] = title_node.get_text()
        else:
            res_data["title"] = "empty"
            
        summary_node = soup.find("div", class_ = "lemma-summary")
        if summary_node:
            res_data["summary"] = summary_node.get_text()
        else:
            res_data["summary"] = "empty"
        
        return res_data
        
    def parser(self, page_url, html_doc):
        if page_url is None or html_doc is None:
            return
        soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
        
"""输出器"""
class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        
    
    def output_html(self):
        fp = open("output.html", "w")
        fp.write("<html>")
        fp.write("<body>")
        fp.write("<table>")
        for data in self.datas:
            fp.write("<tr>")
            fp.write("<td>%s</td>"%data["url"].encode("utf-8"))
            fp.write("<td>%s</td>"%data["title"].encode("utf-8"))
            fp.write("<td>%s</td>"%data["summary"].encode("utf-8"))
            fp.write("</tr>")
        fp.write("</table>")
        fp.write("</body>")
        fp.write("</html>")
        fp.close()

""" 主类  """
class SpiderMain(object):
    def __init__(self):
        self.urls = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()
    
    def craw(self, root_url):
        num = 1
        self.urls.add_new_url(root_url)
        print self.urls.new_urls
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print "count %d: %s" % (num, new_url)
                html_doc = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parser(new_url, html_doc)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                
                if num == 30:
                    break
                num += 1
            except Exception, e:
                print "crawed filed!!!", str(e)
            
        self.outputer.output_html()


if __name__ == "__main__":
    root_url = "http://baike.baidu.com/view/2107.htm"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
    print "Game Over!"
