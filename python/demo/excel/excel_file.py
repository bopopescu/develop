#-*- encoding:utf-8 -*-

'''
Created on 2016-09-21

@author: dedong.xu

@description: 使用python的第三方库读写Excel表格数据
'''

#3rd library
import xlrd
import xlwt
import pyExcelerator
import xlsxwriter.workbook

excel_file = r"d:\build_server.xlsx"
write_excel_file = r"d:\zzz.xlsx"
write_excel_file1 = r"d:\zzz.xls"


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
        table3 = self.data.sheet_by_name(sheet_name)
        return table3
        for i in xrange(table3.nrows):
            print table3.row_values(i)
        print table3.nrows, table3.ncols
        
        
    def get_cell_data(self, sheetname):
        """ 获取单元格数据 """
        table1 = self.data.sheet_by_index(0)
        cell1 = table1.cell(2, 1).value
        print cell1, type(table1)
        
        table2 = self.data.sheet_by_name(sheetname)
        cell2 = table2.cell(9, 2).value
        return cell2, type(table1)
        
        
    def get_cell_data_by_index(self):
        """ 通过索引获取单元格数据  """
        table1 = self.data.sheet_by_index(0)
        cell1 = table1.row(0)[0].value
        return cell1
        

class Write_Excel(object):
    """ 使用pyExcelerator库来向excel表格写入数据  """
    
    def __init__(self, filename):
        """ 初始化设置值 """
        self.filename = filename
        self.w = pyExcelerator.Workbook()
        
    def add_sheet_name(self, sheetname):
        """ 设置sheet name """
        self.ws = self.w.add_sheet(sheetname)
        
    def write_data(self, row, col, value):
        """ 写数据 """
        self.ws.write(row, col, value)
        self.w.save(self.filename)
        

class Write_Excel_By_Xlwt(object):
    """ 使用xlwt库来向excel表格写入数据 """
    
    def __init__(self, filename):
        """ 初始化设置值 """
        self.filename = filename
        self.w = xlwt.Workbook()
        
    def add_sheet_name(self, sheetname):
        """ 设置sheet name """
        self.ws = self.w.add_sheet(sheetname, cell_overwrite_ok = True)
        
    def write_data(self, row, col, value):
        """ 写入数据 """
        self.ws.write(row, col, value)
        self.w.save(self.filename)
        
        
class Write_Excel_By_XlsxWriter(object):
    """ 使用 XlsxWriter库来向excel表格写入数据 """
    
    def __init__(self, filename):
        self.filename = filename
        self.w = xlsxwriter.workbook.Workbook(self.filename)
        
    def set_excel(self):
        """ 设置表格大小以及字体 """
        self.worksheet = self.w.add_worksheet()      #增加一个worksheet
        self.bold = self.w.add_format({"bold" : 1})  #黑体格式，突出单元格文本
        self.worksheet.set_column("A:E", 20)         #加宽第A列到第E列，使文字更清晰
    
    def write_data(self):
        """ 向excel写数据 """
        self.worksheet.write("A1", "hello")
        self.worksheet.write("A2", "hello")
        self.worksheet.write("A3", "hello")
        self.worksheet.write("A4", "hello")
        self.worksheet.write("A5", "World", self.bold)
        self.worksheet.write(2, 1, 123)
        self.worksheet.write(3, 2, 123.456)
        self.worksheet.write("B4", "hello")
        
    
    def close(self):
        """ 关闭excel文件 """
        self.w.close()


class A(object):
    def __init__(self):
        self.name = "xdd"
        
    def test1(self):
        self.age = 89
        print self.name
        
    def test2(self):
        print self.age
        
        
def main(excel_file, write_excel_file):
    """ 从一个excel表中读取数据，然后再写入到另一个excel表中 """
    re = Read_Excel(excel_file)
    #re.get_data()
    #re.get_data_index()
    #re.get_cell_data("Sheet1")
    we = Write_Excel(write_excel_file)
    webx = Write_Excel_By_Xlwt(write_excel_file1)
    sheet_names = re.get_sheet_names()
    for sheet_name in sheet_names:
        table = re.get_data_by_name(sheet_name)
        webx.add_sheet_name(sheet_name)
        for i in xrange(table.nrows):
            for j in xrange(len(table.row_values(i))):
                webx.write_data(i, j, table.row_values(i)[j])
   
    
def main_test(write_excel_file):
    webx = Write_Excel_By_XlsxWriter(write_excel_file)
    webx.set_excel()
    webx.write_data()
    webx.close()
    
    
        
if __name__ == "__main__":
    main_test(write_excel_file)
    main(excel_file, write_excel_file)

    
    
    