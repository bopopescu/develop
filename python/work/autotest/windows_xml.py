#-*- encoding:utf-8 -*-
from xml.etree.ElementTree import ElementTree
import getpass, os
import platform

user_name = getpass.getuser()


#XML_FILE_PATH = 'C:\\Users\\' + user_name + '\\AppData\\Roaming\\DVDFab9\\fab_config.xml'
SYSTEM_NAME = platform.platform()
if "XP" in SYSTEM_NAME.upper():
    XML_FILE_PATH = 'C:\\Documents and Settings\\' + user_name + '\\Application Data\\DVDFab9\\'
    xml_temp = XML_FILE_PATH + "temp.xml"
else:
    XML_FILE_PATH = 'C:\\Users\\' + user_name + '\\AppData\\Roaming\\DVDFab9\\'
    xml_temp = XML_FILE_PATH + "temp.xml"
    
def read_xml(xml_path, path,xml_temp):
    #print xml_path
    #delete(xml_path, xml_temp)
    nodes = []
    tree = ElementTree()
    try:
        tree.parse(xml_path)
        root = tree.getroot()
        nodes = root.findall(path)
    except Exception,e:
        pass
    return tree, nodes

def update_xml(nodes, key, value):
    for node in nodes:
        node.attrib[key] = value
       
def write_xml(tree, out_xml_path):  
    tree.write(out_xml_path, encoding="utf-8")
    

def delete(xml_path, xml_temp):

    fp = open(xml_path, "r")
    all_lines = fp.readlines()
    fp.close()
    fp = open(xml_temp, "w")
    for each_line in all_lines:
        if '<item_' in each_line:
            index = all_lines.index(each_line)
            each_line = ""
            all_lines[index+1] = ""
            all_lines[index+2] = ""
        fp.write(each_line)

    fp.close()
    os.remove(xml_path)
    os.rename(xml_temp, xml_path)




#if __name__ == '__main__':
#    read_xml(XML_FILE_PATH, 'common_setting/Generic',xml_temp)
