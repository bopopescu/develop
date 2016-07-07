#-*- encoding:utf-8-*-

'''
Created on 2016Äê6ÔÂ27ÈÕ

@author: dedong.xu
'''

class Write_File(object):
    #fp = ""
    
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
        
    def open_file(self):
        self.fp = open(self.filename, "w")
        
    def write_file(self):
        self.fp.write(self.content)
        
    def close_file(self):
        self.fp.close()
        
        
if __name__ == "__main__":
    wf = Write_File("d:/test/xudedong.txt", "qweqweqweqweqwe")
    wf.open_file()
    wf.write_file()
    wf.close_file()