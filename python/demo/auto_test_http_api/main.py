#-*- encoding:utf-8 -*-
'''
Created on 2016-09-29

@author: dedong.xu

@description: 自动化测试http POST请求主程序入口。
'''

#standard lib
import sys
import time
import os

#local lib
from auto_test_http_api import Auto_Test_Http_Api
from read_excel_file import Read_Excel
from settings import excel_file, HTML_FILE_PATH, RESULT_LIST, FLAG , URL


def clear_list(the_list):
    """ 清空列表元素 """
    while the_list:
        the_list.pop()
        

def write_file(filename, c):
    """ 写文件 """
    with open(filename, "w") as f:
        f.write(c)
        
def create_path(folder):
    """ 创建目录 """
    if not os.path.exists(folder):
        os.makedirs(folder, mode = 0777)
        
        
def get_year_month_cur_time():
    """ 获取年，月，当前时间 """
    cur_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    year = cur_time.split("_", 1)[0]
    month = cur_time.split("_", 2)[1]
    return cur_time, year, month
  
"""
def get_keys_list(result_dict):
    " 给定的参数是期望结果，字典类型的数据，返回值是去重后的由字典的键组成的列表 "
    for key in xrange(len(result_dict)):
        if isinstance(result_dict, dict):
            key = result_dict.keys()[key]
            KEYS_LIST.append(key)
        if isinstance(result_dict[key], (dict, list, tuple)):
            get_keys_list(result_dict[key])
    return [i for i in set(KEYS_LIST)]
"""

def create_case_table(title_list, content_list):
    """ 将每一条case的内容以及所对应的标题放到table表格里面 """
    td0_strs = "".join(["<td>%s</td>\n" % i for i in title_list])
    td_strs = "".join(["<td>%s</td>\n" % i for i in content_list])
    content = "<table style='background-color:#E0EEEE; ' width='100%%' border='solid 3px'>\n\
    <tr align='center'>\n%s</tr>\n<tr align = 'center'>\n%s</tr>\n</table>\n<br />\n" % (td0_strs, td_strs)
    return content


def create_compare_result_table(color, actual_result, expected_result):
    """ 将预期结果和实际结果的对比放到table表格里面 """
    content = "<table style='background-color:%s; table-layout:fixed;word-break: break-word;' width='100%%' border='solid 3px red'>\n\
    <tr align = 'center' width = '50%%'>\n<td>%s</td>\n<td>%s</td>\n</tr>\n<tr align = 'center' width = '50%%'>\n\
    <td>%s</td><td>%s</td>\n</tr>\n</table>\n<br />\n" % (color, u"实际结果", u"预期结果", actual_result, expected_result)
    return content


def main(excel_file, FLAG):
    """ 主程序入口 """
    n = 1
    rel = Read_Excel(excel_file)
    data_dict = rel.get_all_data()
    cur_time, year, month = get_year_month_cur_time()
    final_path = os.path.join(os.path.join(HTML_FILE_PATH, year), month)
    create_path(final_path)
    content = "<html>\n<title>Auto Test Build Info</title>\n<body style= 'word-break: break-word; width:100%%'>\n<h1 align = 'center'>Auto Test Build Info</h1>\n"
    for key in data_dict:
        for index in xrange(1, len(data_dict[key])):
            api_name = rel.get_api_name(key, index)
            timeout = rel.get_timeout(key, index)
            url = rel.get_url(key, index)
            params = rel.get_params(key, index)
            category = rel.get_category(key, index)
            expected_result = rel.get_expected_result(key, index)
            content += "<h2 align = 'center'>Current Case number is %d, API name is: %s</h2>\n" % (n, api_name)
            data_dict[key][index][9] = u"预期结果见下方"
            content += create_case_table(data_dict[key][0], data_dict[key][index])
            atha = Auto_Test_Http_Api(url, params,  expected_result, timeout = float(timeout)/1000)
            is_timedout = atha.get_post_data()
            if not is_timedout:
                atha.convert_result_json_to_dict()
                if category.upper() == "A":
                    atha.convert_expected_result_json_to_dict()
                    atha.get_new_result()
                    atha.compare_result_by_structure()
                    actual_result = atha.new_result
                elif category.upper() == "B":
                    atha.convert_expected_result_json_to_dict()
                    atha.compare_result_by_all_str()
                    actual_result = atha.result
                elif category.upper() == "C":
                    atha.compare_result_by_field()
                    actual_result = atha.new_result
                else:
                    continue
                if RESULT_LIST:
                    color = "#CD5555"
                    FLAG = False
                else:
                    color = "#7CFC00"
            else:
                color = "#CD5555"
                FLAG = False
                actual_result = "timeout"
            content += create_compare_result_table(color, actual_result, expected_result)
            clear_list(RESULT_LIST)
            n += 1 
    content += "</body>\n</html>"
    write_file(os.path.join(final_path, "%s.html" % cur_time), content.encode("utf-8", "ignore"))
    print "\n%s/%s/%s/%s.html\n" % (URL, year, month, cur_time)
    if FLAG is False:
        print "测试结果有错误，请打开上面的链接进入详情页面\n"
        sys.exit(1)
        
    
if __name__ == "__main__":
    main(excel_file, FLAG)



