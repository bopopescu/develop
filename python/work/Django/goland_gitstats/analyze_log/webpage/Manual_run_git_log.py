#-*- encoding:utf-8

import subprocess
import time
import os
import sys

def run_git_log(param):
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print "current time is: ", time.strftime("%Y-%m-%d %H:%M:%S")
        process = subprocess.Popen("ps -ef | grep run_git_log.py", stdout = subprocess.PIPE, shell= True)
        all_lines = process.stdout.readlines()
        print "length is: ", len(all_lines)
        for each_line in all_lines:
            print each_line
        if len(all_lines) >= 6:
            print "Timing Fresh is working!"
        else:
            print "I am working"
            cmd = "python " + os.getcwd() + "/run_git_log.py " + param
            subprocess.call(cmd, shell = True)



if __name__ == "__main__":
    run_git_log(sys.argv[1])
