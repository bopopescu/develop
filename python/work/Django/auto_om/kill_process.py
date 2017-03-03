import os
import subprocess

process_list = ["nginx", "uwsgi"]

def get_process_id(process_name):
    cmd = "ps -ef | pgrep %s" % process_name
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.readlines()
    return [i.strip() for i in out]

def kill_process(pid):
    cmd = 'echo "123456" | sudo -S kill -9 %s' % pid
    os.system(cmd)

def start_nginx():
    cmd = 'echo "123456" | sudo -S service nginx start'
    os.system(cmd)

def start_uwsgi():
    cmd = "uwsgi -x uwsgi_socket.xml"
    os.system(cmd)

def start_uwsgi_new():
    cmd = "uwsgi --ini uwsgi.ini --pidfile uwsgi.pid --daemonize uwsgi.log"
    os.system(cmd)

def main(process_list):
    for process in process_list:
        pid_list = get_process_id(process)
        print process, len(pid_list)
        for pid in pid_list:
            kill_process(pid)
    start_nginx()
    #start_uwsgi()
    start_uwsgi_new()


if __name__ == "__main__":
    main(process_list)
