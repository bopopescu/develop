#-*- encoding:utf-8 -*-

'''
Created on 2016-09-05

@author: dedong.xu

@description: 将一个大文件分割成多个小文件
'''

import os

src_path = r"d:\zzz"                        #大文件所在路径
big_file = "111.gif"                        #大文件
per_file_size = 100000                      #单位是字节


def write_file(filename, c):
    """ 写文件 """
    try:
        fp = open(filename, "wb")
        fp.write(c)
        fp.close()
    except Exception as e:
        print "write file exception; %s" % str(e)


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


def main():
    """主程序入口"""
    split_file(os.path.join(src_path, big_file), per_file_size)


if __name__ == "__main__":
    main()
    

    
    
    