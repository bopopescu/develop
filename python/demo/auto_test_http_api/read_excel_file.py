#-*- encoding:utf-8 -*-
'''
Created on 2016-09-28

@author: dedong.xu

@description: python读取excel文件中的内容
'''
#standard lib
import json

#3rd library
import xlrd


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
    
    
    def get_data_by_index(self):
        """ 通过索引顺序获取 ，返回一个对Sheet象"""
        table2 = self.data.sheet_by_index(0)
        print table2, type(table2)
        for i in xrange(table2.nrows):
            print type(table2.row_values(i)), table2.row_values(i)
        print table2.nrows, table2.ncols
        
        
    def get_data_by_name(self, sheet_name):
        """ 通过名称获取数据 ，返回一个对Sheet象"""
        try:
            table = self.data.sheet_by_name(sheet_name)
            return [table.row_values(i) for i in xrange(table.nrows)]
            #print table3.nrows, table3.ncols
        except Exception as e:
            print str(e)
            return []
        
        
    def get_cell_data_by_name(self, sheetname):
        """ 获取单元格数据 """
        table2 = self.data.sheet_by_name(sheetname)
        cell1 = table2.col(6)[1].value
        cell2 = table2.cell(0, 4).value
        print table2.ncols
        print cell1, len(table2.col(8))
        print cell2, type(table2)
        
        
    def get_all_col_title(self, sheetname):
        """ 获取所有列的表头 """
        table = self.data.sheet_by_name(sheetname)
        print table.ncols, table.nrows
        data_dict = {}
        for i in xrange(table.ncols):
            key = table.col(i)[0].value
            value_list = []
            for j in xrange(1, table.nrows):
                value = table.col(i)[j].value
                value_list.append(value)
            data_dict[key] = value_list
        return data_dict
                
        
    def get_cell_data_by_index(self):
        """ 通过索引获取单元格数据  """
        table1 = self.data.sheet_by_index(2)
        cell1 = table1.cell(2, 1).value
        print cell1, type(table1)
        table1 = self.data.sheet_by_index(0)
        cell1 = table1.col(6)[0].value
        print cell1
        
    def get_all_data(self):
        """ 获取所有的数据 """
        data_dict = {}
        name_list = self.get_sheet_names()
        for name in name_list:
            data_dict[name] = self.get_data_by_name(name)
        return data_dict
        
    def get_api_name(self, sheetname, index):
        """ 获取接口名 """
        table = self.data.sheet_by_name(sheetname)
        return table.row_values(index)[4].strip()
        
    def get_params(self, sheetname, index):
        """ 获取请求的参数"""
        table = self.data.sheet_by_name(sheetname)
        return table.row_values(index)[5].strip()
    
    
    def get_url(self, sheetname, index):
        """ 获取url"""
        table = self.data.sheet_by_name(sheetname)
        return table.row_values(index)[6].strip()
    
        
    def get_category(self, sheetname, index):
        """ 获取类型 """
        table = self.data.sheet_by_name(sheetname)
        return table.row_values(index)[8].strip()
    
    def get_expected_result(self, sheetname, index):
        """ 获取预期的结果 """
        table = self.data.sheet_by_name(sheetname)
        return table.row_values(index)[9].strip()
    
    def get_timeout(self, sheetname, index):
        """ 获取超时时间 """
        table = self.data.sheet_by_name(sheetname)
        return table.row_values(index)[10]
    
        
    def convert_json_to_dict(self, json_data):
        """ 将json数据转换成python字典 """
        try:
            return json.loads(json_data)
        except Exception as e:
            print "convert json to dict failed", str(e)
            return {}
         
        
def main(excel_file):
    """ 主程序入口 """
    rel = Read_Excel(excel_file)
    data_dict = rel.get_all_data()
    print rel.get_params("Sheet1", 1)
    print json.loads(rel.get_params("Sheet1", 1))
    return data_dict
      
        
if __name__ == "__main__":
    excel_file = r"d:\auto_test_result.xlsx"
    main(excel_file)
    #for i in main(excel_file)["Sheet1"]:
    #    print i
    #print main(excel_file)