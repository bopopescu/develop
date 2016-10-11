#-*- encoding:utf-8 -*-
'''
Created on 2016-09-29

@author: dedong.xu

@description: 全局变量以及常量的设置。
'''

excel_file = r"d:\auto_test_result.xlsx"

""" 结果不一致时将自定义信息保存起来 """
#FLAG_LIST = []

""" 结果不一致时将具体位置保存起来 """
RESULT_LIST = []

""" 将指定的key保存到新的字典里面 """
RESULT_DICT = {}

""" 待测试的key列表 """
#KEYS_LIST = ["total", "title", "name", "director", "backdrop", "thumbnail"]
#KEYS_LIST = []

"""错误结果的提示"""
ERROR_MESSAGE = "Actual results are not consistent with expected results!"

"""正确结果的提示"""
SUCCESS_MESSAGE = "The result is success!"

""" html文件的存放路径 """
HTML_FILE_PATH = r"\\10.10.2.72\nas\other\users\vidon_auto_test_result"

""" 展示log信息的根路径 """
URL = "http://10.10.2.72:9008"

""" 判断是否错误的标志量，默认为True，如果设置为 False，那么结果无论如何都是错误的 """
FLAG = True


