#-*- encoding:utf-8 -*-

'''
Created on 2016-07-28

@author: dedong.xu
'''
import logging
import os

DB_HOST = "xxxxxxxx"
DB_NAME = "db_name"
DB_USER = "user"
DB_PASSWD = "password"
LOG_FILENAME = os.path.join(os.getcwd(), "log.txt")

"""这个列表的含义是所有的不能用于创建目录的特殊符号"""
SPECIAL_CHARS_LIST = ['\\','/',':','*','?','"','<','>','|', '+', ',', '.',' ']


def log(info, filename = LOG_FILENAME):
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = "a", format = "%(asctime)s : %(message)s")
    logging.info(info)    