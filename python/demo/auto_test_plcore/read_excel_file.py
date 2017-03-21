#-*- encoding:utf-8 -*-

'''
Created on 2016-12-7

@author: dedong.xu

@description: python读取excel文件中的内容
'''

#3rd lib
import xlrd

excel_file = r"plcore_auto_test.xls"

class Read_Excel(object):
    """ 使用python第三方库xlrd读取Excel文件的内容"""
    
    def __init__(self, filename):
        """ 初始化变量 """
        self.filename = filename
        self.__data = xlrd.open_workbook(self.filename)
        
    def get_sheet_names(self):
        """ 获取所有的sheet name """
        return self.__data.sheet_names()
    
    def get_data_by_name(self, sheet_name):
        """ 通过名称获取数据 ，返回一个Sheet对象"""
        try:
            table = self.__data.sheet_by_name(sheet_name)
            return [table.row_values(i) for i in xrange(table.nrows)]
        except Exception as e:
            print str(e)
            return []
    
    def get_all_data(self):
        """ 获取所有的数据 """
        data_dict = {}
        name_list = self.get_sheet_names()
        for name in name_list:
            data_dict[name] = self.get_data_by_name(name)
        return data_dict
    
    def get_cell_data(self, sheetname, row, col):
        """ 获取单元格数据
                             参数：sheetname:页面的名称
                row：单元格所在的行
                col：单元格所在的列
        """
        table = self.__data.sheet_by_name(sheetname)
        return table.row_values(row)[col].strip()
    
    def get_apk_version(self, sheetname, row):
        """ 获取apk的版本号 """
        return self.get_cell_data(sheetname, row, 1)
    
    def get_apk_update_conf_content(self, sheetname, row):
        """ 获取apk的升级配置文件 """
        return self.get_cell_data(sheetname, row, 2)
    
    def get_play_conf_content(self, sheetname, row):
        """ 获取apk的播放配置文件 """
        return self.get_cell_data(sheetname, row, 3)

        
        
        
if __name__ == "__main__":
    re = Read_Excel(excel_file)
    sheet_names =  re.get_sheet_names()
    for sheet_name in sheet_names:
        sheet_name = "Sheet3"
        print re.get_apk_version(sheet_name, 3)
        print "*"*100
        print re.get_apk_update_conf_content(sheet_name, 3)
        print "*"*100
        print re.get_play_conf_content(sheet_name, 3)
        break
        
        
        