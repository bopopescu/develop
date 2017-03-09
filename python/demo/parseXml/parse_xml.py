#-*- encoding:utf-8 -*-

'''
Created on 2016-3-6

@author: dedong.xu

@description: 使用python的xml.dom.minidom 模块解析xml文件
'''

#standard lib
from xml.dom import minidom

xml_file = "DVDFab10.jzp"
date = "2021-05-26"
version = "78.9.6.3"
version_type = "official"
info_dict = {"date": date, "version": version, "version2": version_type}

class Parse_Xml(object):
    """ 解析xml文件内容 """
        
    def parse(self, xml_content):
        """ 解析xml字符串为xml对象 """
        try:
            doc = minidom.parseString(xml_content)
            root = doc.documentElement
            return root
        except Exception, e:
            raise NameError, str(e)
    
    def parse_xmlfile(self, xml_file):
        """ 解析xml文档为xml对象 """
        try:
            doc = minidom.parse(xml_file)
            root = doc.documentElement
            return root
        except Exception, e:
            raise NameError, str(e)
        
    def get_xmlnode_list(self, node, name):
        """ 获取xml的节点 """
        return node.getElementsByTagName(name) if node else []
    
    def get_attrvalue(self, node, attrname):
        """ 获取节点的给定的属性值 """
        return node.getAttribute(attrname) if node else ""
    
    def update_node(self, node, key, value):
        """ 修改节点的属性值 """
        node.setAttribute(key, value)
        
    def to_xml(self, root):
        """ 对象转换为xml字符串 """
        return root.toxml()
        
    def write_xml(self, xml_file, root):
        """ 写xml文件 """
        fp = open(xml_file, "w")
        root.writexml(fp)
        fp.close()
        
     
if __name__ == "__main__":
    px = Parse_Xml()
    #root = px.parse(xml)                      #解析xml字符串
    root = px.parse_xmlfile(xml_file)          #解析xml文档
    node_list = px.get_xmlnode_list(px.get_xmlnode_list(root, "config")[0], "item")
    for node in node_list:
        key = px.get_attrvalue(node, "key").lower()
        if key in info_dict:
            node.setAttribute("data", info_dict[key])
    px.write_xml(xml_file, root)



     
        
        
        
