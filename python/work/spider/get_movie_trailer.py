#-*- encoding:utf-8 -*-

'''
Created on 2016年6月21日

@author: dedong.xu
'''
"""
        指定一个主页面入口，然后去匹配并获得相应的url，如果是合法的新的url，然后再去进行解析，直到所有的合法的url被解析完
"""
#standard libs
import urllib, urllib2
import urlparse
import os
import logging

#3rd libs
from bs4 import BeautifulSoup
import MySQLdb

#project
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD,LOG_FILENAME, SPECIAL_CHARS_LIST, log

library_url = r"http://www.hd-trailers.net/library/"
base_movie_url = r"http://www.hd-trailers.net"
base_movie_path = r"Z:/other/download_movie/movie_trailers"
library_list = ["0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]


"""url管理器"""
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        
    def add_url(self, url):
        """ 将新的url添加到new_urls集合中 """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
            
    def add_urls(self, urls):
        """ 将新的url列表添加到new_urls集合中 """
        for url in urls:
            self.add_url(url)
            
    def has_url(self):
        """ 判断new_urls集合中是否还有url """
        return len(self.new_urls) != 0
    
    def get_url(self):
        """ 从new_urls集合中获得一个url """
        url = self.new_urls.pop()
        if url.endswith("/") or url.endswith("\\"):
            url = url[:-1]
        self.old_urls.add(url)
        return url
    
    
"""url下载器"""
class UrlDownloader(object):
    def url_download(self, url):
        """ 获取html字符串文档 """
        if url is None:
            return 
        try:
            response = urllib2.urlopen(url)
            if response.code != 200:
                return
        except Exception, e:
            print str(e)
            return
        return response.read()
    
"""url解析器"""
class HtmlParser(object):   
    def parser(self, html_doc):
        """ 使用BeautifulSoup解析html文档 """
        if html_doc is None:
            return
        try:
            soup = BeautifulSoup(html_doc, "html.parser", from_encoding = "utf-8")
        except Exception as e:
            log("parser error: %s" % str(e))
            soup = None
        return soup
    
    def get_all_movie_link_urls(self, soup):
        """ 获取所有的电影链接 """
        movie_urls = set()
        try:
            links = soup.find("table", class_ = "libraryTextIndexList").find_all("a")
        except Exception as e:
            links = []
        for link in links: 
            try:
                movie_urls.add(link["href"])
            except Exception, e:
                print str(e)
                log("get movie links failed: %s" % str(e))
        return movie_urls
    
    def get_movie_name(self, soup):
        """ 获取电影的名字 """
        try:
            movie_name_obj = soup.find("table", class_ = "mainTopTable").find("h1", class_ = "previewTitle", itemprop = "name")
        except Exception as e:
            print str(e)
            movie_name_obj = None
        movie_name = movie_name_obj.text if movie_name_obj else None
        return movie_name
    
    def get_picture_download_url(self, soup):
        """ 获取图片的下载链接 """
        try:
            movie_picture_obj = soup.find("table", class_ = "mainTopTable").find("span", class_ = "topTableImage").find("img")
        except Exception as e:
            movie_picture_obj = None
        if movie_picture_obj:
            #picture_download_url = movie_picture_obj["src"]
            picture_download_url = urlparse.urljoin("http:", picture_download_url)
        else:
            picture_download_url = None
        return picture_download_url
    
    def get_trailer(self, soup):   
        """ 获取电影预告片的标题 """
        try:
            trailer_obj = soup.find("table", class_ = "bottomTable").find("td", id = "Trailers").find("h2")
        except Exception as e:
            trailer_obj = None
        trailer = trailer_obj.text if trailer_obj else None
        return trailer
    
    def get_movie_other_info(self, soup, cur_movie_path):
        """ 获取电影的其他信息 """
        try:
            tr_obj = soup.find("table", class_ = "bottomTable").find_all("tr", itemprop = "trailer")
        except Exception as e:
            tr_obj = []
        movie_other_info = []
        for each_tr_obj in tr_obj:
            each_movie_other_info = []
            td_obj = each_tr_obj.find_all("td")
            movie_category_dict = {}
            for each_td_obj in td_obj:
                if not each_td_obj.text.strip():
                    continue
                if each_td_obj.text in ("480p", "720p", "1080p"):
                    try:
                        movie_download_url = each_td_obj.find("a")["href"]
                    except Exception, e:
                        movie_download_url = ""
                        print str(e)
                    movie_local_url = self.download_movie_or_picture(movie_download_url, cur_movie_path, "movie")
                    movie_category_dict[each_td_obj.text] = movie_local_url
                    movie_category_dict["url_" + each_td_obj.text] = movie_download_url
                else:
                    each_movie_other_info.append(each_td_obj.text)
            each_movie_other_info.append(movie_category_dict)
            movie_other_info.append(each_movie_other_info) 
        return movie_other_info


    def get_movie_info(self, soup):
        """ 获取电影的所有信息 """
        movie_name = self.get_movie_name(soup)
        picture_download_url = self.get_picture_download_url(soup)
        cur_movie_path = self.create_movie_path(movie_name)
        picture_path = self.download_movie_or_picture(picture_download_url, cur_movie_path, "picture")
        movie_other_info = self.get_movie_other_info(soup, cur_movie_path) 
        return {"movie_name": movie_name, "picture_path": picture_path, "movie_other_info": movie_other_info}
    
    
    def create_movie_path(self, movie_name):
        """ 在本地创建保存下载的电影的目录 """
        if movie_name is None:
            return   
        for each_str in SPECIAL_CHARS_LIST:
            if each_str in movie_name:
                movie_name = movie_name.replace(each_str, "_")
        cur_movie_path = os.path.join(base_movie_path, movie_name).replace("\\","/")
        if not os.path.exists(cur_movie_path):
            os.mkdir(cur_movie_path)
        return cur_movie_path
    
    def download_movie_or_picture(self, download_url, cur_movie_path, category = None, isDownload = False):
        """ 下载电影或者图片 """
        if isDownload:
            if download_url is "" or download_url is None or cur_movie_path is None:
                return
            try:
                local_path = os.path.join(cur_movie_path,os.path.basename(download_url)).replace("\\", "/")
                if not os.path.exists(local_path):
                    urllib.urlretrieve(download_url, local_path)#, Schedule)
            except Exception, e:
                local_path = ""
                log("download %s failed: %s" % (category, str(e)))
            return os.path.basename(download_url)   #modify at 2016-07-07
        return ""
    
    def get_adress(self, adress_dict, key):
        """ 获取地址 """
        try:
            adress = adress_dict[key]
        except Exception, e:
            adress = ""
        return adress
    
    
"""数据库"""
class  Mysql(object):
    def __init__(self):
        self.host = DB_HOST
        self.user = DB_USER
        self.passwd = DB_PASSWD
        self.db = DB_NAME
        
    def connect_db(self):
        """ 连接数据库 """
        try:
            self.conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWD, db = DB_NAME, charset = "utf8")
            self.cursor = self.conn.cursor()
        except Exception, e:
            print str(e)
            #sys.exit()
            self.conn = None
            self.cursor = None
        return self.conn, self.cursor
        
        
    def insert_db_movie_name(self, movie_name, picture_path, language):
        """ 将电影名字插入数据库 """
        if "'" in movie_name:
            insert_sql = '''insert into %s(%s,%s,%s) values ("%s","%s","%s")''' % ("movie_trailer_movie_name", "name", "picture_path","language", movie_name, picture_path, language)
        else:
            insert_sql = "insert into %s(%s,%s,%s) values ('%s','%s','%s')" % ("movie_trailer_movie_name", "name", "picture_path","language", movie_name, picture_path, language)
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
        
    def insert_db_movie_info(self, movie_name_id, movie_time, trailer_order, address_high_definition, address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p):
        """ 将电影其他信息插入数据库 """
        if "'" in trailer_order:
            insert_sql = '''insert into %s (%s,%s,%s,%s,%s,%s, %s, %s,%s,%s, %s) values ("%d","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' \
            % ("movie_trailer_movie_info", "movie_name_id", "movie_time","trailer_order", "address_high_definition","address_480p", "address_720p", \
           "address_1080p","url_high_definition","url_480p", "url_720p","url_1080p", movie_name_id, movie_time, trailer_order, address_high_definition,\
           address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p)
        else:
            insert_sql = "insert into %s (%s,%s,%s,%s,%s,%s, %s, %s,%s,%s, %s) values ('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
        % ("movie_trailer_movie_info", "movie_name_id", "movie_time","trailer_order", "address_high_definition","address_480p", "address_720p", \
           "address_1080p","url_high_definition","url_480p", "url_720p","url_1080p", movie_name_id, movie_time, trailer_order, address_high_definition,\
           address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p,url_1080p)
        #print insert_sql
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception as e:
            print str(e)
  
    def has_record(self, tb_name, column_id, tb_id, column_name, tb_column):
        """判断数据库是否有指定的记录"""
        if tb_id is None:
            if "'" in tb_column:
                select_sql = 'select * from %s where %s = "%s"' % (tb_name, column_name, tb_column)
            else:
                select_sql = "select * from %s where %s = '%s'" % (tb_name, column_name, tb_column)
        else:
            if "'" in tb_column:
                select_sql = 'select * from %s where %s = "%s" and %s = "%s"' % (tb_name, column_id, tb_id, column_name, tb_column)
            else:
                select_sql = "select * from %s where %s = '%s' and %s = '%s'" % (tb_name, column_id, tb_id, column_name, tb_column)
        self.cursor.execute(select_sql)
        record = self.cursor.fetchone()
        if record is None:
            return False
        return len(record) != 0
    
    def get_movie_name_id(self, tb_name, column_name, movie_name):
        """ 获取表中电影名字的id """
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
        
        
    def close_db(self):
        """ 关闭数据库 """
        self.cursor.close()
        self.conn.close()
		

"""主程序"""
class SpiderMain(object):
    def __init__(self):
        self.urlmanager = UrlManager()
        self.urldownloader = UrlDownloader()
        self.htmlparser = HtmlParser()
        self.mysql = Mysql()
        
    def craw(self, library_url, library_list):
        """ 开始爬取网站信息 """
        print "begin to craw!"
        log("*******************************begin to craw!*******************************")
        for each_library in library_list:
            """连接数据库"""
            conn, _ = self.mysql.connect_db()
            if conn is None:
                continue
            """对每一个字母开头的页面解析"""
            library_page = urlparse.urljoin(library_url, each_library)
            library_html_doc = self.urldownloader.url_download(library_page)
            library_parser_page = self.htmlparser.parser(library_html_doc)
            if library_parser_page is None:
                return
            movie_link_urls = self.htmlparser.get_all_movie_link_urls(library_parser_page)
            for each_movie_url in movie_link_urls:
                movie_url = urlparse.urljoin(base_movie_url,each_movie_url)   #movie url like: http://www.hd-trailers.net/movie/1/ 
                movie_html_doc = self.urldownloader.url_download(movie_url)
                movie_parser_page = self.htmlparser.parser(movie_html_doc)
                movie_info = self.htmlparser.get_movie_info(movie_parser_page)  #get movie info and download picture
                #print movie_info
                movie_name_id = self.mysql.get_movie_name_id("movie_trailer_movie_name", "name", movie_info["movie_name"])
                if ("movie_name" in movie_info and movie_info["movie_name"] is None) or \
                (self.mysql.has_record("movie_trailer_movie_name", "id", None, "name", movie_info["movie_name"])):
                    print "movie info is already in database or movie_name is None"
                else:
                    movie_name_id = self.mysql.insert_db_movie_name(movie_info["movie_name"],movie_info["picture_path"].replace("Z:/other", "/mnt/nas/other"), "English")
                if movie_name_id is None:
                    continue
                for each_record in movie_info["movie_other_info"]:
                    movie_time = each_record[0]
                    trailer_order = each_record[1]
                    address_high_definition = ""
                    address_480p = self.htmlparser.get_adress(each_record[2], "480p")
                    address_720p = self.htmlparser.get_adress(each_record[2], "720p")
                    address_1080p = self.htmlparser.get_adress(each_record[2], "1080p") 
                    url_high_definition = ""
                    url_480p = self.htmlparser.get_adress(each_record[2], "url_480p")
                    url_720p = self.htmlparser.get_adress(each_record[2], "url_720p")
                    url_1080p = self.htmlparser.get_adress(each_record[2], "url_1080p")
                    if not self.mysql.has_record("movie_trailer_movie_info", "movie_name_id", movie_name_id,  "movie_time", movie_time):
                        self.mysql.insert_db_movie_info(movie_name_id, movie_time, trailer_order, address_high_definition, address_480p, address_720p, address_1080p, url_high_definition, url_480p, url_720p, url_1080p)
            """关闭数据库"""
            self.mysql.close_db()
        
            
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