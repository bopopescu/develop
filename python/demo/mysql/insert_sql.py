#-*- encoding:utf-8 -*-
import MySQLdb
import time
import functools



DB_HOST = ""
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = ""

def take_time(func):
    @functools.wraps(func)
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print end - start
    return wrapper


#这个插入速度最快，因为他与数据库之间的连接等操作，只进行了一次。
@take_time
def insert_table():
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD)   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    insert_sql = 'insert into %s (Days_display) values(%s)' % ("blog_web_params", "100")
    for i in xrange(10000):
        cursor.execute(insert_sql)
    conn.commit()
    cursor.close()   
    conn.close()


#这个速度很慢，因为每插入一条数据就与数据库进行一次连接关闭等操作。
@take_time
def insert_table1():
    num = 0
    while num < 10000:
        num += 1
        conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD)   
        conn.select_db(DB_NAME)        
        cursor = conn.cursor()     
        insert_sql = 'insert into %s (Days_display) values(%s)' % ("blog_web_params", "100")
        cursor.execute(insert_sql)
        conn.commit()
        cursor.close()   
        conn.close()
        

#这个速度很慢，因为每插入一条数据就与数据库进行一次连接关闭等操作。
@take_time
def insert_table2():
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD)   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    insert_sql = 'insert into %s (Days_display) values(%s)' % ("blog_web_params", "100")
    for i in xrange(10000):
        cursor.execute(insert_sql)
        conn.commit()
    cursor.close()   
    conn.close()


@take_time
def select_table():
    conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD)   
    conn.select_db(DB_NAME)        
    cursor = conn.cursor()     
    select_sql = 'select * from %s where Days_display <> "100"' % ("blog_web_params")
    cursor.execute(select_sql)
    conn.commit()
    cursor.close()   
    conn.close()




if __name__ == "__main__":
    select_table()

    insert_table()
    print "************************************************"
    insert_table1()
    print "************************************************"
    insert_table2()
