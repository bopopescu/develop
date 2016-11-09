#-*- encoding:utf-8 -*-

'''
Created on 2016-11-09

@author: dedong.xu

@description: log日志函数。
'''

import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

LOG_FILENAME = "d:/test/log.log"

def log_by_size(info, logfile = LOG_FILENAME, mode = "a", maxBytes = 50*1024*1024, backupCount = 10):
    """ 可以设定log文件的大小，当超过设定的值时，就将当前文件重命名，然后创建一个新的同名日志文件 """
    Rthandler = RotatingFileHandler(logfile, mode = mode, maxBytes = maxBytes, backupCount = backupCount)
    log_format = "%(asctime)s : %(levelname)s : %(message)s"
    formatter = logging.Formatter(log_format)
    Rthandler.setFormatter(formatter)
    log = logging.getLogger()
    log.setLevel(logging.NOTSET)
    log.addHandler(Rthandler)
    logging.info(info)
    log.removeHandler(Rthandler)
    
    
    
def log_by_day(info, logfile = LOG_FILENAME):
    """ 每天生成一个日志文件 """
    logHandler = TimedRotatingFileHandler(logfile, when="midnight")
    logFormatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)-s: %(message)s')
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.NOTSET)
    logging.info(info)
    logger.removeHandler(logHandler)
    
    
if __name__ == "__main__":    
    log_by_size("this is my info log")
    log_by_day("this is my info log")
    
    
    