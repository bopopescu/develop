#-*- encoding:utf-8 -*-

'''
Created on 2016-09-28

@author: dedong.xu

@description: 使用urllib2模块发送http POST请求，获取返回结果，并与预期结果比较。
'''

#standard lib
import urllib2
import json

#local lib
from settings import RESULT_LIST


def ehco_result(*args):
    """ 根据给定的参数，打印输出到屏幕 """
    for record in args:
        print record
        
    
def traversal_result(result, expected_result):
    """ 递归循环遍历字典或者元组或者列表中的键值是否相等 """
    assert type(result) is type(expected_result)
    for key in xrange(len(result)):
        if isinstance(result, dict):
            key = result.keys()[key]
        if isinstance(result[key], dict) and isinstance(expected_result[key], dict):
            if sorted(result[key].keys()) == sorted(expected_result[key].keys()):
                traversal_result(result[key], expected_result[key])
            else:
                error = "2:内部字典的键不一样"
                RESULT_LIST.append(error)
                return False
        elif isinstance(result[key], list) and isinstance(expected_result[key], list):
            if len(result[key]) == len(expected_result[key]):
                traversal_result(sorted(result[key]), sorted(expected_result[key]))
            else:
                error = "3:内部列表长度不一样"
                RESULT_LIST.append(error)
                return False
        elif isinstance(result[key], tuple) and isinstance(expected_result[key], tuple):
            if len(result[key]) == len(expected_result[key]):
                traversal_result(sorted(result[key]), sorted(expected_result[key]))
            else:
                error = "4:内部元组长度不一样"
                RESULT_LIST.append(error)
                return False
        else:
            if result[key] != expected_result[key]:
                error = "5:元素值不相等"
                RESULT_LIST.append(error)
                return False

"""              
def get_specified_key(result):
    " 递归循环遍历字典或者元组或者列表中的键,并将键值对放入自己的数据结构里 ,一个键对应多个值的话，则以列表的形式将值保存起来与键对应"
    for key in xrange(len(result)):
        if isinstance(result, dict):
            key = result.keys()[key]
        if isinstance(result[key], (dict, list, tuple)):
            get_specified_key(result[key])
        else:
            if key in KEYS_LIST: 
                if key in RESULT_DICT:
                    RESULT_DICT[key].append(result[key])
                else:
                    RESULT_DICT[key] = [result[key]]
"""
       
                    
def clear_dict(the_dict):
    """ 清空字典 """
    for i in the_dict.keys():
        the_dict.pop(i)
            

class Auto_Test_Http_Api(object):
    """ 对http接口POST请求的自动化测试 """

    def __init__(self, url, params, expected_result, timeout= 50):
        """ 初始化设置值 ,其中expected_result的类型是字符串"""
        self.url = url
        self.params = params
        self.expected_result = expected_result
        self.timeout = timeout
        self.new_result = {}
        
        
    def get_post_data(self):
        """ 获取http请求的返回值 """
        try:
            #data = urllib.urlencode(self.params)
            request = urllib2.Request(self.url, self.params)
            request.add_header('Content-Type', 'application/json; charset=utf-8')
            #request.add_header('Content-Length', len(self.params))
            response = urllib2.urlopen(request, timeout = self.timeout)
            self.result = response.read()
            is_timedout = False
        except Exception as e:
            print str(e)
            self.result = "{}"
            is_timedout = True
        return is_timedout

    
    def convert_result_json_to_dict(self):
        """ 将json格式的数据转换成python字典 """
        try:
            self.result = json.loads(self.result)
        except Exception as e:
            print "convert json data to dict failed: ", str(e)
            self.result = {}
            
            
    def convert_expected_result_json_to_dict(self):
        """ 将json格式的数据转换成python字典 """
        try:
            self.expected_result = json.loads(self.expected_result)
        except Exception as e:
            print "convert json data to dict failed: ", str(e)
            self.expected_result = {}
    
    
    def output_result(self):
        """ 输入实际结果与预期结果 """
        print "actual results: ", type(self.result), self.result
        print "expected results: ", type(self.expected_result), self.expected_result
        
        
    def get_new_result(self):
        """ 根据预期结果的键值从实际结果里生成新的结果集  """
        assert(isinstance(self.expected_result, dict))
        for key in self.expected_result:
            try:
                self.new_result[key] = self.result[key]
            except KeyError as e:
                print str(e)
                pass
        """
        get_specified_key(self.expected_result)
        self.expected_result_dict = RESULT_DICT.copy()
        clear_dict(RESULT_DICT)
        get_specified_key(self.result)
        self.result_dict = RESULT_DICT.copy()
        clear_dict(RESULT_DICT)
        """
        
        
    def compare_result_key(self, key):
        """ 比较实际结果与预期的结果 """
        assert(isinstance(self.expected_result_dict, dict))
        assert(isinstance(self.result_dict, dict))
        if key in self.expected_result_dict and key in self.result_dict:
            if sorted(self.expected_result_dict[key]) == sorted(self.result_dict[key]):
                test_result = "%s OK..........................." % key
                test_flag = 1
            else:
                test_result = "%s ERROR..................." % key
                test_flag = 0
        else:
            test_result = "ERROR, can not find key: %s....................." % key
            test_flag = 0
        return test_flag, test_result
        
        
    def compare_result_by_structure(self):
        """ 结构化比较，比较实际结果与预期的结果 """
        assert(isinstance(self.expected_result, dict))
        assert(isinstance(self.new_result, dict))
        if sorted(self.new_result.keys()) == sorted(self.expected_result.keys()):
            """如果键都一样，那就对比字典的value值"""
            traversal_result(self.new_result, self.expected_result)          
        else:
            error = "1:字典的键不一样"
            RESULT_LIST.append(error)
            return False
        
    def compare_result_by_all_str(self):
        """ 全字符串比较，比较实际结果与预期的结果 """
        assert(isinstance(self.expected_result, dict))
        assert(isinstance(self.result, dict))
        if sorted(self.result.keys()) == sorted(self.expected_result.keys()):
            """如果键都一样，那就对比字典的value值"""
            traversal_result(self.result, self.expected_result)          
        else:
            error = "1:字典的键不一样"
            RESULT_LIST.append(error)
            return False
        
    def compare_result_by_field(self):
        """ 字段比较 """
        assert(isinstance(self.result, dict))
        field_dict = dict([i.split("=") for i in self.expected_result.split("&")])
        traversal_dict(self.result, field_dict, self.new_result)
        if self.new_result != field_dict:
            RESULT_LIST.append("字段不一样")
  

"""
expected_result = {"fileamounts":10, "movies":2}            
new_result = {}
"""
def traversal_dict(result, expected_result, new_result):
    """ 根据预期结果的键值从实际结果里生成新的结果集  """
    for key in xrange(len(result)):
        if isinstance(result, dict):
            key = result.keys()[key]
            if key in expected_result.keys():
                new_result[key] = result[key]
        if isinstance(result[key], (dict, list, tuple)):
            traversal_dict(result[key], expected_result, new_result)

                
                 

