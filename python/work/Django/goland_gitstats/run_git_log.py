#-*- encoding:utf-8 -*-
import MySQLdb
import os
import subprocess
import time
import logging
import platform
import chardet

DB_NAME = "goland_gitstats"
GIT_BASE_URL = "git@10.10.2.31:"
TEMPFILE = os.getcwd() + "/temp_log.txt"
BRANCHES_FILE = os.getcwd() + "/all_branches.txt"
GIT_PROJECT_LOCAL_PATH = "/Volumes/Backup/goland"
DB_HOST = "10.10.2.170"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "123456"


#该函数可以获取不同系统平台下的文档的路径
def get_documents_path():
    if os.name == 'nt':
        SYSTEM_NAME = platform.platform()
        if "XP" in SYSTEM_NAME.upper():
            documents_path = os.path.expanduser("~") + "\\My Documents"
        else:
            documents_path = os.path.expanduser('~') + '\\Documents'
    else:
        documents_path = os.path.expanduser('~') + '/Documents'
    return documents_path

documents_path = get_documents_path()
LOG_FILENAME = documents_path + '/run_git_log.log'
LOG_FILENAME = os.path.dirname(__file__) + '/run_git_log.log'
LOG_FILENAME = os.getcwd() + '/run_git_log.log'

print LOG_FILENAME


#记录log的函数，参数是log信息
def log(info):     
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 


#从gitstats_project工程表里获取到所有的工程，没有参数，返回值一个列表，包括所有工程的名字
def get_all_projects():
    all_projects = []
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD, charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    select_sql = "select name from gitstats_project"
    cursor.execute(select_sql)
    conn.commit()
    res = cursor.fetchall() 
    cursor.close()   
    conn.close()

    for record in res:
        if record[0].strip():
            #git_url = os.path.join(GIT_BASE_URL, record[0].strip()) + ".git"
            all_projects.append(record[0].strip())
    return all_projects


#联表查询，从记录表里查询到指定工程最后一次提交的时间。接收的参数是each_project，表示工程名；返回值是最后一次提交的时间
def get_last_commit_time_and_branch_name(each_project):
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset="utf8")   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    select_sql = "select gcr.commit_time from gitstats_commit_record as gcr INNER JOIN gitstats_project as gp ON (gcr.project_id = gp.id) where gp.name = '%s' order by gcr.commit_time desc" % each_project 
    cursor.execute(select_sql)
    conn.commit()
    res = cursor.fetchone()
    #log("commit record: %s" % str(res))
    cursor.close()   
    conn.close()
    if res:
        last_commit_time = res[0]
        #last_commit_time = "2016-01-15 00:00:00"
    else:
        last_commit_time = "2015-12-01 00:00:00"
        #last_commit_time = time.strftime("%Y-%m-%d") + " 00:00:00"
        #last_commit_time = time.strftime("%Y-%m-%d %H:%M:%S")
    #log("last_commit_time is: %s" % last_commit_time)
    return last_commit_time


#这个函数获得指定工程与其所有的分支名字；接收的参数是工程的在本地的路径；返回值是一个列表，包括该工程的所有分支名字
def get_all_branches(dest_path):
    all_branches_list = []
    all_branches_txt = BRANCHES_FILE
    cmd = "git branch -a > " + all_branches_txt
    subprocess.call(cmd, cwd = dest_path, shell = True)
    fp = open(all_branches_txt, "r")
    all_lines = fp.readlines()
    fp.close()
    #all_branches_list.append(dest_path)
    for each_line in all_lines:
        if each_line.strip().startswith("remotes/origin") and each_line.count("origin") == 1:
            branch_name = each_line.split("origin/")[1].strip()
            all_branches_list.append(branch_name)
    print "all_branches_list: ", all_branches_list
    return all_branches_list
    #return all_branches_list[1:]


#该函数功能是将服务器上的工程clone到本地
def git_clone_project(project_name):
    folder_name = project_name.split(":")[1].strip().split(".")[0].strip().replace("/", "_")
    git_clone_cmd = "git clone " + project_name + " " + folder_name
    subprocess.call(git_clone_cmd, cwd = GIT_PROJECT_LOCAL_PATH, shell = True)


#这个函数的作用是，查看指定工程，指定分支，指定时间的log，然后把log保存到一个临时文件里
#接受的参数依次是each_project, project_local_path, branch_name,last_commit_time, end_time,tempfile
def run_git_log(each_project, project_local_path, branch_name,last_commit_time, end_time,tempfile):
    git_reset_cmd = "git reset --hard"
    subprocess.call(git_reset_cmd, cwd = project_local_path, shell = True)
    git_checkout_cmd = "git checkout " + branch_name
    subprocess.call(git_checkout_cmd, cwd = project_local_path, shell = True)
    git_pull_cmd = "git pull"
    subprocess.call(git_pull_cmd, cwd = project_local_path, shell = True)
    #git_log_cmd = 'git log --branches="%s" --after="%s" --before="%s" > %s' % (branch_name,last_commit_time, end_time,TEMPFILE)
    git_log_cmd = 'git log --after="%s" --before="%s" > %s' % (last_commit_time, end_time,TEMPFILE)
    print "git_log_cmd: ", git_log_cmd
    log("git log cmd is: %s" % git_log_cmd)
    #log("execute git cmd path is: %s" % project_local_path)
    p = subprocess.Popen(git_log_cmd, cwd = project_local_path, stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell=True)
    if p.stdout.read():
        print "out: ", p.stdout.read()
        log("project_name is : %s" % each_project)
        log("out: %s" % p.stdout.read())
    if p.stderr.read():
        print "err: ", p.stderr.read()
        log("project_name is : %s" % each_project)
        log("err: %s" % p.stderr.read())


#这个函数按行读取文件所有内容，接收的参数是一个带有路径的文件名字； 返回一个列表
def read_file_lines(filename):
    fp = open(filename, "r")
    all_lines = fp.readlines()
    fp.close()
    return all_lines


def format_date_time(src_date):
    from_list_time = src_date.strip().split(" ")[0].split("-")  
    if len(from_list_time[1]) == 1:
        month = "0" + from_list_time[1]
    else:
        month = from_list_time[1]
    if len(from_list_time[2]) == 1:
        day = "0" + from_list_time[2]
    else:
        day = from_list_time[2]
    format_date = from_list_time[0] + "-" + month + "-" + day + " " + src_date.strip().split(" ")[1]
    return format_date


#这个函数专门分析log的内容，将作者，提交时间，提交信息以及版本号提取出来。接收的参数是一个带有路径的文件名字
def analysis_log(temp_file):
    commit_version = ""
    author = ""
    commit_time = ""
    commit_message = ""
    each_result = []
    analyzed_log_result = []
    month_dict = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12",}
    
    all_lines = read_file_lines(temp_file)
    num = 0
    for each_line in all_lines:
        if each_line.strip():
            if num % 3 == 0:
                each_result = []
            if each_line.startswith("commit"):
                num += 1
                commit_version = each_line.split(" ")[1].strip()
                each_result.append(commit_version)
            
            elif each_line.startswith("Author:"):
                num += 1
                author = each_line.split(" ")[1].strip()
                each_result.append(author)
            
            elif each_line.startswith("Date:"):
                num += 1
                try:
                    temp_time = each_line.replace("Date:", "").strip()[4:].split("+")[0].strip()
                    month = month_dict[temp_time.split(" ")[0]]
                    day = temp_time.split(" ")[1]
                    cur_time = temp_time.split(" ")[2]
                    year = temp_time.split(" ")[3]
                    commit_time = year + "-" + month + "-" + day + " " + cur_time
                    commit_time = format_date_time(commit_time)
                except Exception, e:
                    commit_time = ""
                    log(str(e))
                each_result.append(commit_time)

                #获得commit信息
                commit_message = ""
                date_index = all_lines.index(each_line)
                flag = 1
                while flag:
                    commit_message += all_lines[date_index + 2].strip()
                    #if date_index + 3 > len(all_lines) - 1 or all_lines[date_index + 3].strip() == "":
                    if date_index + 3 > len(all_lines) - 1 or all_lines[date_index + 3].strip() == "" or all_lines[date_index + 1].strip().startswith("commit "):
                        flag = 0
                    else:
                        date_index += 1
                        flag = 1
                each_result.append(commit_message)
            #if each_line.startswith("commit") or each_line.startswith("Author") or each_line.startswith("Date:"):
            #    print num
            if each_result and num % 3 == 0:
                analyzed_log_result.append(each_result)
    #print analyzed_log_result
    return analyzed_log_result

                
        
        

#表Author， Porject， 以及Package都可以调用这个函数来完成查询功能。接收的参数是是表的名字，返回查询到的一条记录的第一个值
def select_table(tb_name, column_name):
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    select_sql = 'select id from %s where name = "%s"' % (tb_name, column_name)
    cursor.execute(select_sql)
    conn.commit()
    res = cursor.fetchone()
    cursor.close()   
    conn.close()
    return res
    


#表Author， Porject， 以及Package都可以调用这个函数来完成插入功能。 接收的参数是是表的名字，没有返回值。
def insert_table(tb_name, column_name):
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    insert_sql = 'insert into %s (name) values("%s")' % (tb_name, column_name)
    cursor.execute(insert_sql)
    conn.commit()
    cursor.close()   
    conn.close()


#函数功能是根据commit_record表中的commit_version字段是否有当前的值，有的话不在保存；否则保存到表中。
def ifsaved_currentrecord(project_name, branch_name, commit_version):
    flag = True
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()    
    select_sql = 'select id from %s where commit_version = "%s"' % ("gitstats_commit_record", commit_version)
    cursor.execute(select_sql)
    conn.commit()
    res = cursor.fetchone()
    cursor.close()   
    conn.close()
    if res:
        flag = False
    return flag


#函数功能是将git log 信息插入到数据库里,
#参数依次是author_id, project_id, branch_name, commit_version, commit_message, commit_time, package_path, flag
#返回值是当前插入的记录的id
def insert_commit_record(author_id, project_id, branch_name, commit_version, commit_message, commit_time, package_path, flag):
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    if "'" in commit_message:
        insert_sql = 'insert into %s (author_id,project_id, branch_name, commit_version, commit_message, commit_time, package_path, flag) values("%s","%s","%s","%s","%s","%s","%s","%s")' % \
                 ("gitstats_commit_record", author_id, project_id, branch_name, commit_version, commit_message, commit_time, package_path, flag)
    else:
        insert_sql = "insert into %s (author_id,project_id, branch_name, commit_version, commit_message, commit_time, package_path, flag) values('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                 ("gitstats_commit_record", author_id, project_id, branch_name, commit_version, commit_message, commit_time, package_path, flag)
    print "insert sql is: %s" % insert_sql
    cursor.execute(insert_sql)
    conn.commit()
    
    select_sql = 'select id from %s where commit_version = "%s"' % ("gitstats_commit_record", commit_version)
    print "select sql is: %s" % select_sql
    cursor.execute(select_sql)
    conn.commit()
    res = cursor.fetchone()
    cur_id = int(res[0])
    cursor.close()   
    conn.close()
    return cur_id


#将记录id与对应的产品id插入到数据库中
def insert_product_commit_record(product_id, commit_record_id):
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    insert_sql = 'insert into %s (product_id, commit_record_id) values(%d, %d)' % ("gitstats_product_commit_record", product_id, commit_record_id)
    cursor.execute(insert_sql)
    conn.commit()
    cursor.close()   
    conn.close()


def ifexistsselect_elseinsert_thenselect(tb_name, column_name):
    #判断当前工程是否在数据库，如果在取出对应id；如果不在，则先存入数据库中，然后再取出id
    data_id = select_table(tb_name, column_name)
    #print "data_id: ", data_id
    if not data_id:
        log("%s does not exist!" % column_name)
        insert_table(tb_name, column_name)
        data_id = select_table(tb_name, column_name)
    data_id = int(data_id[0])
    return data_id


#根据工程名字获取所有的对应的产品id
def get_product_id_from_project(project_name):
    all_product_id_list = []
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD,charset='utf8')   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    #select_sql = 'select name from %s where project_name like "%%s%"' % ("gitstats_product", project_name)
    select_sql = 'select id from gitstats_product where project_name like "%' + project_name + '%"'
    cursor.execute(select_sql)
    conn.commit()
    res = cursor.fetchall()
    cursor.close()   
    conn.close()
    for each_product_id in res:
        all_product_id_list.append(int(each_product_id[0]))
    print all_product_id_list
    return all_product_id_list


#check code
def detect_code(check_strs):
    dict_result = chardet.detect(check_strs)
    print dict_result
    bianma = dict_result["encoding"]
    print bianma
    if bianma == None:
        checked_strs = check_strs 
    elif bianma.upper() == "UTF-8":
        checked_strs = check_strs 
    else:
        checked_strs = check_strs.decode("gb2312","ignore").encode("utf-8")
    return checked_strs


#程序主函数入口
def main():
    log("\n\n\n-----------------------------------  begin  -------------------------------------------")
    end_time = time.strftime("%Y-%m-%d %H:%M:%S")
    all_projects = get_all_projects()
    for each_project in all_projects:
        print "each_project: ", each_project
        if "@" not in each_project or ":" not in each_project or "/" not in each_project or not each_project.strip().endswith(".git"):
            log("\n\n\n-------------------------invalid project name: %s----------------------------\n" % each_project)
            continue
        log("\n\n\n------------------------------project name is: %s---------------------------------" % each_project)
        #project_local_path = r"D:\develop\work_python\goland_gitstats\buildsystem"
        try:
            folder_name = each_project.split(":")[1].strip().split(".")[0].strip().replace("/", "_")
        except Exception as e:
            print str(e)      
            log("1111 " + str(e))
        project_local_path = os.path.join(GIT_PROJECT_LOCAL_PATH, folder_name)
        if not os.path.exists(project_local_path):
            git_clone_project(each_project)

        if (not os.path.exists(project_local_path)) or (os.path.exists(project_local_path) and ".git" not in os.listdir(project_local_path)):
            log("\n-----------------could not read from remote repostroy, maybe the git url: %s is invalid---------------\n" % each_project) 
            continue
        all_branches_list = get_all_branches(project_local_path)
        for branch_name in all_branches_list:
            log("\n\n---------------------------current branch name is :%s-------------------------------" % branch_name)
            package_path = ""
            flag = 0
            last_commit_time = get_last_commit_time_and_branch_name(each_project)
            print "last_commit_time: ", last_commit_time
            print "branch_name: ", branch_name
            run_git_log(each_project, project_local_path, branch_name, last_commit_time, end_time, TEMPFILE)
            analyzed_log_result = analysis_log(TEMPFILE)
            #判断当前工程是否在数据库，如果在取出对应id；如果不在，则先存入数据库中，然后再取出id
            project_id = ifexistsselect_elseinsert_thenselect("gitstats_project", each_project)
            
            #根据工程名字获取到所有的产品id
            all_product_id_list = get_product_id_from_project(each_project)
            cur_id_list = [] 
            for each_result in analyzed_log_result:
                #判断当前作者是否在数据库，如果在取出对应id；如果不在，则先存入数据库中，然后再取出id
                author_id = ifexistsselect_elseinsert_thenselect("gitstats_author", each_result[1])
                result_flag = ifsaved_currentrecord(each_project, branch_name, each_result[0])
                if result_flag:
                    commit_message = detect_code(each_result[3])
                    log("each result is :" + str(each_result))
                    cur_id = insert_commit_record(author_id, project_id, branch_name, each_result[0], each_result[3], each_result[2], package_path, flag)
                    cur_id_list.append(cur_id)
                    for each_product_id in all_product_id_list:
                        insert_product_commit_record(each_product_id, cur_id)
                        print "current insert record is: %d" % each_product_id
            log("cur_id_list is: %s" % str(list)) 
    print "Game Over!"


if __name__ == "__main__":
    main()

