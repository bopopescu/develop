#-*- encoding:utf-8 -*-

'''
Created on 2016-12-7

@author: dedong.xu

@description: 使用python的xml.dom.minidom 模块解析xml文件
'''

#standard lib
import re
import os
from xml.dom import minidom


class Parse_Xml(object):
    """ 解析xml文件内容 """
    
    def __init__(self):
        """ 初始化变量 """
        
    def get_xmlnode(self, node, name):
        """ 获取xml的节点 """
        return node.getElementsByTagName(name) if node else []
    
    def get_attrvalue(self, node, attrname):
        """ 获取节点的给定的属性值 """
        return node.getAttribute(attrname) if node else ""
        
    def parse(self, xml_content):
        """ 解析xml字符串为xml对象 """
        doc = minidom.parseString(xml_content)
        root = doc.documentElement
        return root
    
    def parse_xmlfile(self, xml_file):
        """ 解析xml文档为xml对象 """
        doc = minidom.parse(xml_file)
        root = doc.documentElement
        return root
    
    def test(self, root):
        node = self.get_xmlnode(root, "section")[0]
        print self.get_attrvalue(node, "id")
        print self.get_attrvalue(self.get_xmlnode(node, "apk")[0], "path")
        print self.get_attrvalue(self.get_xmlnode(node, "ip")[0], "group")
        
    def get_apk_path(self, node):
        """ 获取apk包的路径 """
        return self.get_attrvalue(self.get_xmlnode(node, "apk")[0], "path")
    
    def get_ip_list(self, node):
        """ 获取盒子的ip """
        return self.get_attrvalue(self.get_xmlnode(node, "ip")[0], "group").split("#")
    
    def get_xml_file(self, node):
        """ 获得拉取的xml文件 """
        return self.get_attrvalue(self.get_xmlnode(node, "outputxml")[0], "path")
    
    def get_xml_path(self, node):
        """ 获得推送的xml文件的路径 """
        return os.path.dirname(self.get_xml_file(node))
		
    def update_xml(self, xml, new_str):
        """ 先用正则和字符串替换的方式来修改xml，以后再替换为使用xml方法来修改 """
        p = r'<filepath path=(.*?)/>'
        return xml.replace(re.search(p, xml).group(1), '"%s"'% new_str)
    
        
     
if __name__ == "__main__":
    px = Parse_Xml()
    root = px.parse_xmlfile("info.xml.2014")
    node = px.get_xmlnode(root, "version")[0]
    print node
    #print px.get_apk_path(node)
    #print px.get_ip_list(node)
    #print px.get_xml_path(node)   
        
        
        
