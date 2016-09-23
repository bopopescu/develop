#-*- encoding:utf-8 -*-
'''
Created on 2016-09-19

@author: dedong.xu

@description: 封装mysql，实现增删改查的功能
'''

import MySQLdb

DB_HOST = "localhost"
DB_USER = "username"
DB_PASSWD = "password"
DB_NAME = "db"
TB_NAME = "tb"



class Sql(object):
    """ 封装一个mysql类，提供一些简单的方法 """
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
    
    
    def connect_db(self):
        """ 连接数据库 """
        try:
            self.conn = MySQLdb.connect(host = self.host, user = self.user, passwd = self.passwd, db = self.db, charset = "utf8")
            self.cursor = self.conn.cursor()
        except:
            self.conn = None
            self.cursor = None
            
            
    def select_data(self, tb_name):
        """ 获取指定表中的所有数据 """
        select_sql = "select * from %s" % tb_name
        self.cursor.execute(select_sql)
        record = self.cursor.fetchall()
        return record
    
    
    def insert_data(self, tb_name, **kwargs):
        """ 向数据库中插入数据 """
        #注掉的获取key和value的方法也可行
        #import string
        #keys = string.join(kwargs.keys(), ",")
        #values = string.join(kwargs.values(), "','")
        keys = ",".join([str(i) for i in kwargs.keys()])
        values = "','".join([str(i) for i in kwargs.values()])
        insert_sql = "insert into %s (%s) values ('%s')" % (tb_name, keys, values)
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            
            
    def delete_data(self, tb_name, **kwargs):
        """ 删除数据 """
        delete_condition = " AND ".join(["%s='%s'" % (i, kwargs[i]) for i in kwargs])
        if kwargs:
            delete_sql = "delete from %s WHERE %s" % (tb_name, delete_condition)
        else:
            delete_sql = "delete from %s" % (tb_name)
        try:
            self.cursor.execute(delete_sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            
            
    def update_data(self, tb_name, new_data, **kwargs):
        """ 更新数据库 """
        new_data_cmd = ", ".join(["%s='%s'" % (i, new_data[i]) for i in new_data])
        update_condition = " AND ".join(["%s='%s'" % (i, kwargs[i]) for i in kwargs])
        if kwargs:
            update_sql = "update %s SET %s WHERE %s" % (tb_name, new_data_cmd, update_condition)
        else:
            update_sql = "update %s SET %s" % (tb_name, new_data_cmd)
        try:
            self.cursor.execute(update_sql)
            self.conn.commit()
        except:
            self.conn.rollback()
    
    
    def has_record(self, tb_name, **kwargs):
        """ 判断某个表中某个字段是否有某个值 """
        cmd = " AND ".join(["%s='%s'" % (key, kwargs[key]) for key in kwargs])
        select_sql = "select * from %s WHERE %s" % (tb_name, cmd)
        print select_sql
        self.cursor.execute(select_sql)
        record = self.cursor.fetchone()
        if record:
            return True
        return False
    
            
    def close_db(self):
        """ 关闭数据库 """
        self.cursor.close()
        self.conn.close()
        
        
    def get_hostname(self):
        """ 获取服务器名字 """
        return self.host
    
    
    def get_username(self):
        """ 获取用户名 """
        return self.user
    

def main():
    sql = Sql(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
    sql.connect_db()
    sql.select_data(TB_NAME)
    print sql.has_record(TB_NAME, age = "13428", name = "13sda")
    sql.insert_data(TB_NAME, name = "456", age = "789")
    sql.delete_data(TB_NAME, name = "qwe1", age = "678")
    sql.update_data(TB_NAME, {"name": "13", "age": 13428})
    sql.close_db()
    
    
if __name__ == "__main__":
    main()
    
    