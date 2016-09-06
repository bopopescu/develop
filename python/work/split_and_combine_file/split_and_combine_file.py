#-*- encoding:utf-8 -*-

'''
Created on 2016-09-05

@author: dedong.xu

@description: 将一个大文件分割成多个小文件，然后再将这些小文件重新组成一个新的大文件；这两个大文件完全相同
'''

import os

src_path = r"d:\zzz"                        #大文件所在路径
big_file = "111.gif"                        #大文件
new_big_file = "new_big_file"               #新的大文件的名字，但不包含扩展名
per_file_size = 100000                      #单位是字节


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


def split_file(filename, chunksize):
    """ 
        分割文件，将一个大文件按照指定的大小分割成若干个小文件 ;
        根据文件指针的变化判断文件是否读取完毕，当文件指针不再变化的时候就表明读取完毕.
    """
    fp = open(filename, "rb")
    last_position = 0
    n = 1
    while 1:
        each_size = fp.read(chunksize)
        cur_position = fp.tell()
        if cur_position > last_position:
            new_file = "%s.%d" % (filename, n)
            write_file(new_file, each_size)
            last_position = cur_position  
            n += 1 
        else:
            print "Game Over!"
            break


def get_sorted_file_list(src_path):
    """ 获得当前目录下的所有已经排好顺序的文件列表,使用冒泡排序 """
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


def get_extend_name(filename):
    """获取文件扩展名 """
    return os.path.splitext(filename)[1]


def get_combine_filename(src_path, basefilename, extend_name):
    """ 获得组合文件的名字 """
    return os.path.join(src_path, "%s%s" % (basefilename, extend_name))


def maopao(li):
    """ 冒泡排序 """
    for i in xrange(len(li) - 1):
        for j in xrange(i, len(li)):
            if li[i] > li[j]:
                li[i], li[j] = li[j], li[i]
    return li


def main(new_big_file):
    """主程序入口"""
    split_file(os.path.join(src_path, big_file), per_file_size)
    extend_name = get_extend_name(big_file)
    combine_filename = get_combine_filename(src_path, new_big_file, extend_name)
    sorted_file_list = get_sorted_file_list(src_path)
    combine_files(sorted_file_list, combine_filename)


if __name__ == "__main__":
    main(new_big_file)
    

    
    
    