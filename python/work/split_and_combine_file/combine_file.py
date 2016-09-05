#-*- encoding:utf-8 -*-

'''
Created on 2016-09-05

@author: dedong.xu

@description: 将指定目录下的小文件组成一个的大文件
'''

import os

src_path = r"d:\zzz"                        #小文件的目的路径以及新生成的大文件的所在路径
new_big_file = "new_big_file.gif"           #新的大文件的名字


def write_file(filename, c):
    """ 写文件 """
    try:
        fp = open(filename, "wb")
        fp.write(c)
        fp.close()
    except Exception as e:
        print "write file exception; %s" % str(e)


def read_file(filename):
    """ 读文件 """
    try:
        fp = open(filename, "rb")
        c = fp.read()
        fp.close()
    except Exception as e:
        c = ""
        print "read file exception; %s" % str(e)
    return c


def get_sorted_file_list(src_path):
    """ 获得当前目录下的所有已经排好序的以数字结尾的文件名字的列表,使用冒泡算法排序 """
    file_list = [os.path.join(src_path, each_file) for each_file in os.listdir(src_path) if each_file[-1].isdigit()]
    for i in xrange(len(file_list)-1):
        for j in xrange(i, len(file_list)):
            if len(file_list[i]) == len(file_list[j]):
                if file_list[i] > file_list[j]:
                    file_list[i], file_list[j] = file_list[j], file_list[i]
            elif len(file_list[i]) > len(file_list[j]):
                file_list[i], file_list[j] = file_list[j], file_list[i]
    return file_list
            

def combine_files(file_list, combine_filename):
    """ 从一个大文件分割好的一些小的文件再重新组合成一个新的大文件 """
    t = ""
    for each_file in file_list:
        c = read_file(each_file)
        t += c
    write_file(combine_filename, t)
    return


def get_combine_filename(src_path, basefilename):
    """ 获得组合文件的名字 """
    combine_filename = os.path.join(src_path, basefilename)
    return combine_filename


def main(src_path, new_big_file):
    """主程序入口"""
    combine_filename = get_combine_filename(src_path, new_big_file)
    sorted_file_list = get_sorted_file_list(src_path)
    combine_files(sorted_file_list, combine_filename)

if __name__ == "__main__":
    main(src_path, new_big_file)
    print "Combine file Successfully!"
    

    
    
    