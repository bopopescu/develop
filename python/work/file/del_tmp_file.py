#-*- encoding:utf-8 
"""
    @author: dedong.xu
	@date: 2016-09-06
	@description: delete tmp files in C:\Users\username\AppData\Local\Temp folder
"""

import getpass
import os
import time

def get_user():
    """ get current login user """
    return getpass.getuser()
	
	
def get_tmp_folder(username):
    """ get tmp folder """
    tmp_folder = "C:\Users\%s\AppData\Local\Temp" % username
    return tmp_folder
	
	
def delete_file(filename):
    """ delete one file """
    os.remove(filename)
    
	
def delete_tmp_files(tmp_folder):
    """ delete tmp files in tmp folder """
    for each_file in os.listdir(tmp_folder):
        if each_file.startswith("Zip") and each_file.endswith(".tmp"):
            filename = os.path.join(tmp_folder, each_file)
            delete_file(filename)
            print "delete %s!" % filename
            time.sleep(0.1)
			
	
if __name__ == "__main__":
    username = get_user()
    tmp_folder = get_tmp_folder(username)
    print tmp_folder
    delete_tmp_files(tmp_folder)
