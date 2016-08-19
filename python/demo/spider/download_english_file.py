#-*- encoding:utf-8 -*-

'''
Created on 2016-07-29

@author: dedong.xu
'''

#standard libs
import urllib#, urllib2
import os
import re
import urlparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#3rd
import MySQLdb

#project
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD,SPECIAL_CHARS_LIST, log

cur_path = os.getcwd()
filename = cur_path + "/movie_name.txt"
download_name = cur_path + "/download_name.txt"
not_found_name = cur_path + "/not_found_name.txt"
logfile_name = os.path.join(cur_path, "english_name.log")

def format_movie_name(movie_name):
    for each_str in SPECIAL_CHARS_LIST:
        if each_str in movie_name:
            movie_name = movie_name.replace(each_str, "_")
    return movie_name


def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)			
	
def download_movie(download_url, cur_movie_path, movie_name, length):
    if download_url is "" or download_url is None or cur_movie_path is None:
        return
    movie_name = u"%s"%format_movie_name(movie_name)
    extend_name = os.path.splitext(os.path.basename(download_url))[1]	
    cur_movie_path = os.path.join(cur_movie_path,movie_name)
    create_folder(u"%s"%cur_movie_path)
    try:  
        tmp_name = u"%s"%movie_name + u"-trailer-%d%s".encode("utf-8") % (length, extend_name)
    except Exception, e:
        tmp_name = os.path.basename(download_url)
    local_path_file = os.path.join(cur_movie_path, tmp_name)
    try:
        if not os.path.exists(local_path_file):
            urllib.urlretrieve(download_url, local_path_file)#, Schedule)
            log("download movie: %s" % movie_name, logfile_name)
    except Exception, e:
        os.rmdir(cur_movie_path)
        print "download failed: %s; remove dir: %s" % (str(e), cur_movie_path)
        
        
def read_file(filename):
    fp = open(filename, "r")
    all_lines = fp.readlines()
    fp.close()
    return all_lines
        
def get_movie_id(tb_name, movie_name):
    if not movie_name:
        return
    try:
        conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWD, db = DB_NAME, charset = "utf8")
        cursor = conn.cursor()
    except Exception, e:
        conn = None
        cursor = None
    else:
        if "'" in movie_name:
            select_sql = 'select id, name from %s where name like "%%%s%%"' % (tb_name, movie_name)
        else:
            select_sql = "select id, name from %s where name like '%%%s%%'" % (tb_name, movie_name)
        cursor.execute(select_sql)
        record = cursor.fetchall()
        cursor.close()
        conn.close()
        if record:
            return record
    return None

        
def get_url(tb_name, movie_id):
    try:
        conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWD, db = DB_NAME, charset = "utf8")
        cursor = conn.cursor()
    except Exception, e:
        print str(e)
        conn = None
        cursor = None
    else:
        #select_sql = 'select url_high_definition, url_480p,url_720p, url_1080p from %s where movie_name_id = %d' % (tb_name, movie_id)
        select_sql = 'select url_1080p from %s where movie_name_id = %d' % (tb_name, movie_id)
        cursor.execute(select_sql)
        record = cursor.fetchall()
        cursor.close()
        conn.close()
        if record:
            return record
    return None

def record_download_name(filename, content):
    fp = open(filename, "a+")
    fp.write(content + "\n")
    fp.close()


def main():
    count = 1
    all_lines = read_file(filename)
    for each_line in all_lines:
        print "*"*50
        try:
            chinese_name = re.split("###", each_line.strip())[0].strip()
            movie_name_list = [each_line.strip().split("###")[1]]
            movie_name_list = [re.split("###", each_line.strip())[1].strip()]
            for name in movie_name_list:
                movie_id_tuple = get_movie_id("movie_trailer_movie_name",name)
                if movie_id_tuple is not None:
                    for each_record in movie_id_tuple:
                        print "this is %d download, current movie name is %s, but real movie name is %s\n" % (count, name, each_record[1])
                        url_tuple_tuple = get_url("movie_trailer_movie_info", each_record[0])
                        log("current download filename is %s" % name, logfile_name)
                        record_download_name(download_name, each_record[1])
                        for url_tuple in url_tuple_tuple:
                            for url in url_tuple:
                                cur_index = url_tuple_tuple.index(url_tuple)
                                download_movie(url, r"Z:\other\users\xudedong\17\movie".replace("/", "\\"), chinese_name, cur_index)
                        count += 1
                else:
                    print "get movie name: %s; but not in database!" % name
        except Exception as e:
            print str(e)    
  
  
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
    main()
    print "Over!!!"
    
    
