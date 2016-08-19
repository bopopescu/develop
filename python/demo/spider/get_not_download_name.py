#-*- encoding:utf-8 -*-

import os

movie_name = "movie_name.txt"
src_path = r"Z:\other\users\xudedong\17\movie"
download_name = "download_name.txt"
not_download_name = "not_download_name.txt"

def read_file(filename):
    fp = open(filename, "r")
    all_lines = fp.readlines()
    fp.close()
    return all_lines
	
	
def get_all_name(all_lines):
    return [i.split("###")[0].strip() for i in all_lines if i.strip()]
	
	
def get_download_name(src_path):
    return [i.strip() for i in os.listdir(src_path)]
	
	
def get_not_download_name(all_name_list, download_name_list):
    not_download_name_list = []
    for i in all_name_list:
        if i not in download_name_list:
            not_download_name_list.append(i)
    return not_download_name_list
    return [i for i in all_name_list if i not in download_name_list]
	
	
def write_file(filename, c_list):
    fp = open(filename, "w")
    for c in c_list:
        fp.write(c + "\n")
    fp.close()
	
	
def main():
    all_lines = read_file(movie_name)
    all_name_list = get_all_name(all_lines)
    b = [i for i in all_lines if i.strip().endswith("###")]
    print b
    print len(b)
    return
    download_name_list = get_download_name(src_path)
    not_download_name_list = get_not_download_name(all_name_list, download_name_list)
    write_file(download_name, download_name_list)
    write_file(not_download_name, not_download_name_list)
	
def to_unicode(mylist):
    new_list = []
    for i in mylist:
        i = u"%s" % i.decode("gbk").encode("utf-8")
        new_list.append(i)
	
	
def test():
    download_name_list = read_file(download_name)
    not_download_name_list = read_file(not_download_name)
    #download_name_list = to_unicode(download_name_list)
    #not_download_name_list = to_unicode(not_download_name_list)
    write_file("real_not_download_name.txt", [i.strip() for i in not_download_name_list if i not in download_name_list])
    return [i.strip() for i in not_download_name_list if i not in download_name_list]
	
if __name__ == "__main__":
    main()
    #aa = test()
    #print len(aa)
	
	
	
	
	
	
	
	