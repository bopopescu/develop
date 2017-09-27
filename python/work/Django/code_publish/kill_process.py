import os
import subprocess

process_list = ["nginx", "uwsgi"]
password = "613303"

def get_process_id(process_name):
    cmd = "ps -ef | pgrep %s" % process_name
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.readlines()
    return [i.strip() for i in out]

def kill_process(pid, password):
    cmd = 'echo "%s" | sudo -S kill -9 %s' % (password, pid)
    os.system(cmd)

def start_nginx(password):
    cmd = 'echo "%s" | sudo -S service nginx start' % password
    os.system(cmd)

def start_uwsgi():
    cmd = "uwsgi -x /home/goland/develop/code_publish/uwsgi_socket.xml"
    os.system(cmd)

def start_uwsgi_new():
    cmd = "uwsgi --ini /home/goland/develop/code_publish/uwsgi.ini --pidfile /tmp/uwsgi.pid --daemonize /tmp/uwsgi.log"
    os.system(cmd)

def main(process_list):
    for process in process_list:
        pid_list = get_process_id(process)
        print process, len(pid_list)
        for pid in pid_list:
            kill_process(pid, password)
    start_nginx(password)
    #start_uwsgi()
    start_uwsgi_new()


if __name__ == "__main__":
    main(process_list)
