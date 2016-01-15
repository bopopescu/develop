#-*- encoding:utf-8 -*-

import os
import time
import sys

#dirs_list = [r"D:\wget", r"D:\wget76",r"D:\wget"]
"""
   需要在命令行里面运行，接收不固定长度的参数(用到了魔法参数)，参数为路径，结果将路径下的所有子目录子文件全都打印出来 
"""

def list_dir(*dirs_list):
    while 1:
        #print len(sys.argv)
        if len(sys.argv) == 1:
            print u"请至少输入一个路径"
            break
        for each_dir in dirs_list:
            if os.path.exists(each_dir):
                if sys.argv[0] != each_dir:
                    print "*"*25 + each_dir + "*"*25
                    #print __file__
                    for roots, dirs, files in os.walk(each_dir):
                        for each_dir in dirs:
                            filename = os.path.join(roots, each_dir)
                            print filename
                        for each_file in files:
                            filename = os.path.join(roots, each_file)
                            print filename
                    print "\n"
            else:
                print "*"*25 + each_dir + " does not exist!!!" + "*"*25 + "\n"
        print u"请等待1分钟........................................"
        time.sleep(60)


if __name__ == "__main__":
    list_dir(*sys.argv)
    
