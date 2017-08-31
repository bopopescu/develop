#-*- encoding:utf-8 -*-
'''
Created on 2017-07-24

@author: dedong.xu

@description: python爬虫模拟豆瓣登录，然后下载豆瓣高清海报原图
'''
#standard lib
import os
import re
import time
import random
import urllib
import logging

#3rd lib
import requests 
import lxml.etree
import lxml.html
import xlrd


LOGIN_URL = "https://accounts.douban.com/login"
LOG_FILENAME = "douban_poster.log"
EXCEL_FILE = "douban_movieid.xlsx"
PICTURE_PATH = "picture"
SLEEP_TIME_LIST = [10, 20, 23, 15, 50]


def log(info = None, loglevel = logging.NOTSET, logfile=LOG_FILENAME):
    """ 日志函数 """
    logging.basicConfig(filename = logfile, 
                        level    = loglevel, 
                        filemode = "a", 
                        datefmt  = '%a, %d %b %Y %H:%M:%S',
                        format   = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    #return logging
    logging.info(info)
    
    
class Read_Excel(object):
    """ 使用python读取excel表格数据 """
    
    def __init__(self, filename):
        """ 初始化设置值 """
        self.filename = filename
        self.data = xlrd.open_workbook(self.filename)
        
    def get_sheet_names(self):
        """ 获取所有的sheet name """
        return self.data.sheet_names()

    def get_data(self):
        """ 通过索引顺序获取数据,数据以列表形式呈现 """
        table1 = self.data.sheets()
        print table1, type(table1), len(table1)
        
    def get_data_index(self):
        """ 通过索引顺序获取 ，返回一个对Sheet象"""
        table2 = self.data.sheet_by_index(0)
        print table2, type(table2)
        for i in xrange(table2.nrows):
            print type(table2.row_values(i)), table2.row_values(i)
        print table2.nrows, table2.ncols
        
    def get_data_by_name(self, sheet_name):
        """ 通过名称获取数据 ，返回一个对Sheet象"""
        table = self.data.sheet_by_name(sheet_name)
        return [table.row_values(i) for i in xrange(table.nrows)] 


class LoginDouban(object):
    def __init__(self):
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}

    def parse_form(self, tree):
        """ 解析form表单 """
        data = {}
        for e in tree.cssselect("form input"):
            if e.get("name"):
                data[e.get("name")] = e.get("value")
        return data
    
    def __get_form_data(self, html):
        """ 获得登陆的form表单 """
        """
        form表单类似下面所示
        formdata = {"redir": "https://www.douban.com/people/xudedong/",
                    "form_email": "xxxxxxxx", 
                    "form_password": "xxxxxxxx",
                    "remember": None,
                    "source": None,
                    "login": u"登录"
                    }
        """
        tree = lxml.html.fromstring(html)   
        data = self.parse_form(tree)
        try:
            captchaAddr = tree.cssselect("img#captcha_image")[0].get("src")
        except:
            captchaAddr = ""
        #利用正则表达式获取captcha的ID  
        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'  
        try:
            captchaID = re.findall(reCaptchaID, html)[0]
        except:
            captchaID = ""
        #保存到本地  ,然后打开图片输入其中的验证码
        try:
            urllib.urlretrieve(captchaAddr, "captcha.jpg")  
            captcha = raw_input('please input the captcha:') 
        except Exception, e:
            captcha = ""
            print str(e)
        data['captcha-solution'] = captcha  
        data['captcha-id'] = captchaID
        data["form_email"] = "13581722018"
        data["form_password"] = "xudedong1989"
        data["login"] = u"登录".encode("utf-8")
        data["redir"] = "https://www.douban.com/people/xudedong/"
        return data
    
    def login_douban(self, url):
        """ 登录豆瓣，返回一个带有登录信息的对象 """
        html = requests.get(url, headers = self.headers).content
        data = self.__get_form_data(html)
        session = requests.Session()
        session.headers.update(self.headers)
        session.post(url, data = data, headers = self.headers)
        return session


class Download(object):
    """ 网页下载器  """
    def download_html(self, url):
        """ 下载网页 """    
        res = requests.get(url)
        if res.ok is True:
            return res.content
        return
    
    def download_picture(self, url, filename = None):
        """ 下载图片 """
        print urllib.urlretrieve(url, filename)
    
    
class HtmlParser(object):
    """ html文档解析器 """            
    def parse(self, html_doc):
        """ 解析html文档 """
        tree = lxml.html.fromstring(html_doc)
        return tree
    
    def get_tree_list(self, tree):
        """ 获得解析树 """
        return tree.cssselect("div#content>div>div.article>ul>li")    
    
    def get_poster_display_link(self, ele):
        """ 获取海报的展示链接 """
        try:
            poster_link = ele.cssselect("div.cover>a")[0].get("href")
        except:
            poster_link = ""
        return poster_link
    
    def get_poster_link1(self, ele):
        """ 获取海报链接 """
        try:
            poster_link = ele.cssselect("div.cover>a>img")[0].get("src")
        except:
            poster_link = ""
        print "海报链接 ： ", poster_link
        return poster_link
    
    def get_response(self, ele):
        """ 获取响应数 """
        try:
            p = r"\d+"
            res = ele.cssselect("div.name>a")[0].text_content().strip()
            response = int(re.match(p, res).group())
        except:
            response = 0
        return response
            
    def get_dpi(self, ele):
        """ 获取分辨率 """
        try:
            dpi = ele.cssselect("div.prop")[0].text_content().strip()
        except:
            dpi = ""
        return dpi
    
    def get_dpi_num(self, dpi):
        """ 返回分辨率的数值 """
        return eval(dpi.lower().replace("x", "*"))
    
    def is_vertical_poster(self, dpi):
        """ 是否是竖向海报 """
        #landscape横向;  vertical竖向
        landscape, vertical = [i.strip() for i in dpi.lower().split("x")]
        if not (landscape.isdigit() and vertical.isdigit()):
            raise ValueError, "Invalid dpi value"
        if int(landscape) < int(vertical):
            return True
        return False
        
    def is_official_poster(self, des):
        """ 判断是否是正式海报 """
        if u"正式海报" in des:
            return True
        return False
    
    def is_chinese(self, des):
        """ 判断是否是中国大陆的海报 """
        if u"中国大陆" in des:
            return True
        return False
    
    
class Spider(object):
    def __init__(self):
        """ 实例化 """
        self.du = Download()
        self.hp = HtmlParser()  
        
    def __get_max_value_list(self, max_value, data_list):
        """ 获得最大值所在的字典，添加到列表然后返回 """
        max_value_list = []
        return [res for res in data_list if max_value in res.values()]
        for res in data_list:
            if max_value in res.values():
                max_value_list.append(res)
        return max_value_list  
    
    def __write_file(self, filename, content):
        """ 以二进制方式写文件 """
        try:
            with open(filename, "wb") as f:
                f.write(content)
        except:
            log("FAILED: %s" % filename)
        
    def craw(self, session, movie_id, movie_info_url, movie_photo_url, picture_path, sleep_time):
        """ 获取想要的数据,整理成列表形式返回"""
        data_list= []
        response_list= []
        movie_info_html_doc = self.du.download_html(movie_info_url)
        tree = self.hp.parse(movie_info_html_doc)  
        movie_name = tree.cssselect("div#content>h1>span")[0].text.strip()
        log("movie id is: %s, movie name is : %s" % (movie_id, movie_name))
        html_doc = self.du.download_html(movie_photo_url)
        tree = self.hp.parse(html_doc)  
        tree_list = self.hp.get_tree_list(tree)
        for ele in tree_list:
            if ele.cssselect("div.name"):
                #获得海报的描述，正式海报？中国大陆？
                content = ele.cssselect("div.name")[0].text_content()
                dpi = self.hp.get_dpi(ele)
                if self.hp.is_chinese(content) and self.hp.is_official_poster(content) and self.hp.is_vertical_poster(dpi):#是否是中国大陆，  是否是正式海报， 是否是竖向海报
                    poster_link = self.hp.get_poster_display_link(ele)
                    print "poster_link is : %s" % poster_link
                    #解析海报页面，获取海报高清原图的链接
                    poster_link_html_doc = session.get(poster_link).content
                    page = lxml.etree.HTML(poster_link_html_doc)
                    #for res in lxml.html.fromstring(poster_link_html_doc).cssselect("div#content>div>div.article>div.photo-show>div.photo-wp>a.photo-zoom"):
                    for res in page.xpath(u"//div[@id='content']/div/div[@class='article']/div[@class='clearfix']/span[@class='update magnifier']/a"):
                        releative_url = res.attrib["href"]
                    if "releative_url" not in dir():  #这句代码用来判断releative_url变量有没有定义, 也可以使用 "releative_url" in locals()
                        releative_url = "" 
                    response = self.hp.get_response(ele)
                    data_list.append({"poster_link": poster_link, "releative_url": releative_url, "response": response, "dpi": self.hp.get_dpi_num(dpi)})
                    response_list.append(response)
        if not data_list:
            return
        max_response = max(response_list) if response_list else 0
        max_response_list = self.__get_max_value_list(max_response, data_list)   
        dpi_list = [res["dpi"] for res in max_response_list]
        max_dpi = max(dpi_list)
        max_dpi_list = self.__get_max_value_list(max_dpi, max_response_list)
        final_data_list = max_dpi_list
        
        for data in final_data_list:
            poster_link = data["poster_link"]
            releative_url = data["releative_url"]
            print "这是最终的下载链接: %s" % releative_url
            log("这是最终的下载链接: %s" % releative_url)
            prompt_dict = {"#": "获取的地址不对,这是没有登录时的地址: #", "": "未能获取到海报的下载链接"}
            if releative_url in prompt_dict:
                continue
            session.headers["Referer"] = poster_link
            releative_res = session.get(releative_url, verify = False)
            picture_name = "%s_%s%s" % (movie_name, movie_id, os.path.splitext(releative_url)[1].strip())
            log("picture name is : %s" % picture_name)
            if not os.path.exists(os.path.join(picture_path, picture_name)):
                self.__write_file(os.path.join(picture_path, picture_name), releative_res.content)
                print "休眠 %ds" % sleep_time
                time.sleep(sleep_time)

def get_movie_id_list():
    """ 获得电影的id列表 """
    rel = Read_Excel(EXCEL_FILE)
    sheet_names_list = rel.get_sheet_names()
    movie_id_list = []
    for sheet_name in sheet_names_list:
        print sheet_name
        data_list = rel.get_data_by_name(sheet_name)
        for res in data_list:
            if type(res[-1]) is type(1.0) and int(res[-1]) not in movie_id_list:
                movie_id_list.append(int(res[-1]))
    return movie_id_list

if __name__ == "__main__":
    movie_id_list = get_movie_id_list()
    ld = LoginDouban()
    session = ld.login_douban(LOGIN_URL)
    s = Spider()
    for movie_id in movie_id_list:
        log("\n%s begin movie id is %s %s" % ("*"*50, movie_id, "*"*50))
        movie_info_url = "https://movie.douban.com/subject/%s" % movie_id
        movie_photo_url = "%s/photos?type=R" % movie_info_url
        sleep_time = random.choice(SLEEP_TIME_LIST)
        s.craw(session, movie_id, movie_info_url, movie_photo_url, PICTURE_PATH, sleep_time)
        






