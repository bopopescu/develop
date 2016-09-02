#-*- encoding:utf-8 -*-

import subprocess
from SimpleXMLRPCServer import SimpleXMLRPCServer

def analyze():
    grep_cmd = "ps -ef | grep run_git_log.py"
    process = subprocess.Popen(grep_cmd, stdout = subprocess.PIPE, shell = True)
    all_lines = process.stdout.readlines()
    for each_line in all_lines:
        print each_line

    if len(all_lines) >= 5:
        print "Timing Fresh is working"
    else:
        cmd = "python " + os.getcwd() + "/run_git_log.py"
        subprocess.Popen(cmd, shell = True)
        print "I am working!"
    return "result"


if __name__ == "__main__":
    server = SimpleXMLRPCServer(("10.10.2.170", 9998))
    server.register_function(analyze)
    server.serve_forever()

