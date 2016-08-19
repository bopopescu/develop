#-*- encoding:utf-8 -*-

'''
Created on 2016-08-02

@author: dedong.xu
'''


#standard libs
import urllib#, urllib2
import os
import re

#3rd
import MySQLdb

#project
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD,SPECIAL_CHARS_LIST, log
cur_path = os.getcwd()
filename = cur_path + "/English_name.txt"
download_name = cur_path + "/download_name.txt"
download_chinese_name = cur_path + "/download_chinese_name.txt"
not_found_name = cur_path + "/not_found_name.txt"

def download_movie(download_url, cur_movie_path, movie_name):
    if download_url is "" or download_url is None or cur_movie_path is None:
        return
    try:
        for each_str in SPECIAL_CHARS_LIST:
            if each_str in movie_name:
                movie_name = movie_name.replace(each_str, "_")
        cur_movie_path = os.path.join(cur_movie_path,movie_name)
        if not os.path.exists(cur_movie_path):
            os.mkdir(cur_movie_path)
        local_path = os.path.join(cur_movie_path,os.path.basename(download_url)).replace("\\", "/")
        if not os.path.exists(local_path):
            urllib.urlretrieve(download_url, local_path)#, Schedule)
    except Exception, e:
        local_path = ""
        
        
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
        print str(e)
        conn = None
        cursor = None
    else:
        if "'" in movie_name:
            select_sql = 'select id, name from %s where name like "%%%s%%"' % (tb_name, movie_name)
        else:
            select_sql = "select id, name from %s where name like '%%%s%%'" % (tb_name, movie_name)
        print select_sql
        cursor.execute(select_sql)
        record = cursor.fetchall()
        cursor.close()
        conn.close()
        if record:
            return record
        #return None
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
        select_sql = 'select url_high_definition, url_480p,url_720p, url_1080p from %s where movie_name_id = %d' % (tb_name, movie_id)
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


def has_url(records, tb_name, flag):
    if records:
        for record in records:
            movie_url = get_url(tb_name, record[0])
            if movie_url:
                flag =False
                break
    return flag
    
def main():
    count = 1
    all_lines = read_file(filename)  
    p = r"(([0-9]{0,}[a-zA-Z\_\-\!\.\:]+[0-9]{0,}\s?)+[;\s]?)+"
    res_com = re.compile(p)
    
    for each_line in all_lines:
        result = res_com.search(each_line)
        if result:
            movie_names = result.group()
            movie_name_list = [i.strip() for i in movie_names.split(";") if i.strip()]
        else:
            log("not find movie name")
            movie_name_list = []
        chinese_name = re.split(r"\s\d+", each_line.strip())[0].strip().strip()
        record2 = get_movie_id("movie_trailer_movie_name_zh", chinese_name)
        for name in movie_name_list:
            record1 = get_movie_id("movie_trailer_movie_name", name)
            flag = True
            if record1 or record2:
                flag = has_url(record1, "movie_trailer_movie_info", flag)
                if flag:
                    flag = has_url(record2, "movie_trailer_movie_info_zh", flag)
                if flag:
                    if chinese_name:
                        print chinese_name
                        record_download_name(not_found_name, name)
            else:
                if chinese_name:
                    print chinese_name
                    record_download_name(not_found_name, name)
            del chinese_name
            del name        

if __name__ == "__main__":
    main()
    print "Over!!!"
    
    