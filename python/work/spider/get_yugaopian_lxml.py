#-*- encoding:utf-8 -*-
'''
Created on 2016-04-28

@author: dedong.xu
'''

#standard lib
import urllib, urllib2
import urlparse
import re
import os
import json
import logging

#3rd lib
from lxml import etree

#project
from get_movie_trailer import Mysql
from settings import SPECIAL_CHARS_LIST, log


"""
指定一个主页面入口，然后去匹配并获得相应的url，如果是合法的新的url，然后再去进行解析，直到所有的合法的url被解析完。
使用lxml来解析html文档
"""

base_main_url = r"http://www.yugaopian.com"
highlight_url = base_main_url + "/movlist"
base_download_url= "http://www.yugaopian.com/?view=api&mode=download-data&ttid="
base_movie_path = "Z:/other/download_movie/yugaopian"
LOG_FILENAME = os.path.join(os.getcwd(), "yugaopian.log")


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
        try:
            response = urllib2.urlopen(url)
            if response.code != 200:
                return
            return response.read()
        except Exception as e:
            return 
    


"""html解析器"""
class HtmlParser(object):            
    def get_movie_name(self, page):
        movie_name = None
        for record in page.xpath(u"//h1"):
            if "class" in record.attrib:
                if record.attrib["class"] == "movie-name":
                    #movie_name = record.text
                    try:
                        movie_name = record.attrib["title"]
                    except Exception as e:
                        print str(e)
                    break
        return movie_name
    
    def get_picture_download_url(self, page):
        try:
            picture_download_url = page.xpath(u"/html/body/div/div/div[@class='movie-title-mpic']/a/img")[0].attrib["src"]
        except Exception, e:
            picture_download_url = None
            #print "get_picture_download_url: ", str(e)
        return picture_download_url
    
    def get_movie_info(self, page):
        movie_info = {}
        movie_name = self.get_movie_name(page)
        if movie_name:
            log("movie_name is: %s" % movie_name)
        movie_info["movie_name"] = movie_name
        cur_movie_path = self.create_movie_path(movie_name)
        picture_download_url = self.get_picture_download_url(page)
        picture_path = self.download_movie_or_picture(picture_download_url, cur_movie_path, "picture")
        movie_info["picture_path"] = picture_path
        movie_info["movie_other_info"] = [["", "Trailer"]]
        return movie_info
            
    def add_link(self, p, href, key):
        new_full_url = ""
        if href.has_key(key):
            link = href[key]
            reg_result = re.match(p, link)
            if reg_result:
                new_full_url = urlparse.urljoin(base_main_url, reg_result.group())
        return new_full_url

    def get_download_url(self, base_main_url, page):
        hrefs = page.xpath(u"//a")
        p = r"/download/\d+"
        download_url_set = set()
        for href in hrefs:
            download_url = self.add_link(p, href.attrib, "href")
            if download_url:
                download_url_set.add(download_url)
        return download_url_set
    
    def download_movie_or_picture(self, download_url, cur_movie_path, category = None, isDownload = False):
        if isDownload:
            if download_url is "" or download_url is None or cur_movie_path is None:
                return
            try:
                local_path = os.path.join(cur_movie_path,os.path.basename(download_url)).replace("\\", "/")
                if not os.path.exists(local_path):
                    urllib.urlretrieve(download_url, local_path)#, Schedule)
            except Exception, e:
                local_path = ""
                print str(e)
                #log("download %s failed: %s" % (category, str(e)))
            return os.path.basename(download_url)
            return local_path
        return ""
    
    def download_movie(self, download_url, cur_movie_path):
        if download_url is None:
            return
        try:
            local_path = os.path.join(cur_movie_path,os.path.basename(download_url)).replace("\\", "/")
            urllib.urlretrieve(download_url, local_path)#, Schedule)
        except Exception as e:
            local_path = ""
            print str(e)
        #return local_path
        return os.path.basename(download_url)
    
    def create_movie_path(self, movie_name):
        if movie_name is None:
            return   
        for each_str in SPECIAL_CHARS_LIST:
            if each_str in movie_name:
                movie_name = movie_name.replace(each_str, "_")
        cur_movie_path = os.path.join(base_movie_path, movie_name).replace("\\","/")
        if not os.path.exists(cur_movie_path):
            os.mkdir(cur_movie_path)
        return cur_movie_path
    
    def get_all_movie_urls(self, page):
        new_highlight_urls = set()
        hrefs = page.xpath(u"//a")
        p = r"/movie/\d+"
        for href in hrefs:
            movie_url = self.add_link(p, href.attrib, "href")
            if movie_url:
                new_highlight_urls.add(movie_url)
        return new_highlight_urls
        
    def parser(self, html_doc):
        if html_doc is None:
            return
        try:
            page = etree.HTML(html_doc.decode('utf-8'))
        except Exception as e:
            print "parser error: ", str(e)
            page = None
        return page
    
    def get_final_download_url(self, download_url_content, cur_movie_path):
        download_url_dict = {}
        extend_name_list = [".flv", ".mov", ".mkv", ".mp4", ".swf", ".vob", ".bdmv",".f4v"]
        try:
            #download_url = json.loads(download_url_content)[0]["movurl"]    #这句代码解析json格式的数据并将电影下载链接获取到
            for record in json.loads(download_url_content):
                extend_name = os.path.splitext(record["movurl"])[1]
                if extend_name and extend_name in extend_name_list: 
                    if record["subtitle"] == u"高清晰版":
                        record["subtitle"] = u"high_definition"
                    movie_filename = self.download_movie_or_picture(record["movurl"], cur_movie_path)  
                    download_url_dict[record["subtitle"]] = movie_filename
                    download_url_dict["url_" + record["subtitle"]] = record["movurl"]
                #else:
                    #不是有效的下载链接的话，进一步进行分析，获取硕鼠官网的下载链接。
                    #print record["movurl"]
                    #html_doc = UrlDownloader().url_download(record["movurl"])
                    #soup = self.parser(html_doc)
                    #get_flvcd_download_url(soup)
        except Exception as e:
            print "get download url error. ", str(e)
        return download_url_dict


    #flvcd 在download页面获取不到下载链接时，进一步分析提供给的链接， 去获取硕鼠官网的下载链接		
    def get_flvcd_download_url(self, page):
        """not implement"""
    
    def get_adress(self, adress_dict, key):
        try:
            adress = adress_dict[key]
        except Exception, e:
            adress = ""
        return adress
    

"""数据库"""
class  Mysql_ZH(Mysql):       
    def insert_db_movie_name(self, movie_name, picture_path, language):
        if "'" in movie_name:
            insert_sql = '''insert into %s(%s,%s,%s) values ("%s","%s","%s")''' % ("movie_trailer_movie_name_zh", "name", "picture_path","language", movie_name, picture_path, language)
        else:
            insert_sql = "insert into %s(%s,%s,%s) values ('%s','%s','%s')" % ("movie_trailer_movie_name_zh", "name", "picture_path","language", movie_name, picture_path, language)
        #print insert_sql
        try:
            self.cursor.execute(insert_sql)
            current_id = self.conn.insert_id()
            self.conn.commit()
        except Exception as e:
            current_id = None
        return current_id
        """单线程的时候 self.conn.insert_id() 和 self.cursor.lastrowid的结果是一样的,最后一条记录肯定就是刚刚插入的记录；但是并发插入就不一样了，多线程的时候"""
        #return self.cursor.lastrowid
        
    def insert_db_movie_info(self, movie_name_id, movie_time, trailer_order, address_high_definition, address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p,download_url):
        if "'" in trailer_order:
            insert_sql = '''insert into %s (%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s) values ("%d","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' \
            % ("movie_trailer_movie_info_zh", "movie_name_id", "movie_time","trailer_order", "address_high_definition","address_480p", "address_720p", \
           "address_1080p","url_high_definition","url_480p", "url_720p","url_1080p", "download_url", movie_name_id, movie_time, trailer_order, address_high_definition,\
           address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p,download_url)
        else:
            insert_sql = "insert into %s (%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s) values ('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
        % ("movie_trailer_movie_info_zh", "movie_name_id", "movie_time","trailer_order", "address_high_definition","address_480p", "address_720p", \
           "address_1080p","url_high_definition","url_480p", "url_720p","url_1080p","download_url", movie_name_id, movie_time, trailer_order, address_high_definition,\
           address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p,download_url)
        #print insert_sql
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
            print "insert db successfully!!!"
        except Exception as e:
            print str(e)
  
    def has_record(self, tb_name, column_name, tb_column):
        select_sql = 'select * from %s where %s = "%s"' % (tb_name, column_name, tb_column)
        self.cursor.execute(select_sql)
        record = self.cursor.fetchone()
        if record is None:
            return False
        return len(record) != 0
    
    def get_movie_name_id(self, tb_name, column_name, movie_name):
        if movie_name is None:
            return
        if '"' in movie_name:
            select_sql = "select * from %s where %s = '%s'" % (tb_name, column_name, movie_name)
        else:
            select_sql = 'select * from %s where %s = "%s"' % (tb_name, column_name, movie_name)
        self.cursor.execute(select_sql)
        record = self.cursor.fetchone()
        if record is None:
            return
        movie_name_id = record[0]
        return movie_name_id



"""主程序"""
class SpiderMain(object):
    def __init__(self):
        self.urlmanager = UrlManager()
        self.urldownloader = UrlDownloader()
        self.htmlparser = HtmlParser()
        self.mysql = Mysql_ZH()
         
    def craw(self, highlight_url, base_download_url):
        page_count = 261    #这个变量表示当前的页数
        num = 0           #这个变量表示下载预告片的个数
        while 1:
            """连接数据库"""
            conn, _ = self.mysql.connect_db()
            if conn is None:
                continue
            #解析所有预告片信息
            highlight_url_cur_page = os.path.join(highlight_url, "____" + str(page_count)).replace("\\", "/")
            highlight_html_doc = self.urldownloader.url_download(highlight_url_cur_page)
            highlight_soup = self.htmlparser.parser(highlight_html_doc)
            if highlight_soup is None:
                return 
            new_movie_urls = self.htmlparser.get_all_movie_urls(highlight_soup)
            if not new_movie_urls:
                break
            print "+++++++++++++++++++++++++++++++++++++++第%d页电影下载!!!+++++++++++++++++++++++++++++++++++++++" % page_count
            page_count += 1
            self.urlmanager.add_urls(new_movie_urls)
            while self.urlmanager.has_url():
                movie_url = self.urlmanager.get_url()
                num += 1
                print "第 %d次下载!!!" % num
                #movie_url = "http://www.yugaopian.com/movie/19215"
                movie_html_doc = self.urldownloader.url_download(movie_url)
                movie_soup = self.htmlparser.parser(movie_html_doc)
                if movie_soup is None:
                    continue
                #print "movie_url: ", movie_url
                new_download_url_set = self.htmlparser.get_download_url(base_main_url, movie_soup)
                movie_info = self.htmlparser.get_movie_info(movie_soup)
                movie_name_id = self.mysql.get_movie_name_id("movie_trailer_movie_name_zh", "name", movie_info["movie_name"])
                if ("movie_name" in movie_info and movie_info["movie_name"] is None) or \
                (self.mysql.has_record("movie_trailer_movie_name_zh", "name", movie_info["movie_name"])):
                    print "movie info is already in database or movie_name is None"
                else:
                    movie_name_id = self.mysql.insert_db_movie_name(movie_info["movie_name"],movie_info["picture_path"].replace("Z:/other", "/mnt/nas/other"), "Chinese")
                for new_download_url in new_download_url_set:
                    download_data_url = base_download_url + os.path.basename(new_download_url)   #基url + movie id号
                    download_url_content = self.urldownloader.url_download(download_data_url)
                    cur_movie_path = self.htmlparser.create_movie_path(movie_info["movie_name"])
                    download_url_dict = self.htmlparser.get_final_download_url(download_url_content,cur_movie_path) 
                                   
                    movie_time, trailer_order = movie_info["movie_other_info"][0][0], movie_info["movie_other_info"][0][1]
                    address_high_definition = self.htmlparser.get_adress(download_url_dict, "high_definition")
                    address_480p = self.htmlparser.get_adress(download_url_dict, "480p")
                    address_720p = self.htmlparser.get_adress(download_url_dict, "720p")
                    address_1080p = self.htmlparser.get_adress(download_url_dict, "1080p") 
                    url_high_definition = self.htmlparser.get_adress(download_url_dict, "url_high_definition")
                    url_480p = self.htmlparser.get_adress(download_url_dict, "url_480p")
                    url_720p = self.htmlparser.get_adress(download_url_dict, "url_720p")
                    url_1080p = self.htmlparser.get_adress(download_url_dict, "url_1080p")
                    if not self.mysql.has_record("movie_trailer_movie_info_zh", "download_url", new_download_url):
                        self.mysql.insert_db_movie_info(movie_name_id, movie_time, trailer_order, address_high_definition, address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p,new_download_url)
            """关闭数据库"""
            self.mysql.close_db()


def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print '%.2f%%' % per

              
if __name__ == "__main__":
    obj_spider = SpiderMain()
    obj_spider.craw(highlight_url, base_download_url)
    print "Game Over!!!"



