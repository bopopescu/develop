#-*- encoding:utf-8

import subprocess
import time
import os

time_list = ["09", "10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

def run_git_log():
    while 1:
        cur_hour = time.strftime("%H")
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if cur_hour in time_list:
            print "current time is: ", time.strftime("%Y-%m-%d %H:%M:%S")
            process = subprocess.Popen("ps -ef | grep run_git_log.py", stdout = subprocess.PIPE, shell= True)
            all_lines = process.stdout.readlines()
            print "length is: ", len(all_lines)
            for each_line in all_lines:
                print each_line
            if len(all_lines) >= 5:
                print "Manual Fresh is working!"
                time.sleep(10)
            else:
                print "I am working"
                cmd = "python " + os.getcwd() + "/run_git_log.py"
                subprocess.call(cmd, shell = True)
                time.sleep(60*60)
        else:
            print "current time is: %s, not in working time" % cur_time
            time.sleep(30*60)



if __name__ == "__main__":
    run_git_log()
