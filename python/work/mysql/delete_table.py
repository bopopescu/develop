#-*- encoding:utf-8 -*-
'''
Created on 2017/09/07

@author: dedong.xu

@description: 根据给定的表名，从给定的数据库中批量删除，表名可以是完整的，也可以是一部分，详情见get_delete_sql方法说明。
'''

import MySQLdb

HOST = "localhost"
USER = "user"
PASSWORD = "password"
DB_NAME = "db_name"        
TB_NAME = "tb_name"              #表名或者表名的一部分


class MySql(object):
    """ mysql类实现批量删除表的功能 """
    def __init__(self, host, user, passwd, db):
        """ 初始化变量 """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        
    def connect_db(self):
        """ 连接数据库 """
        self.conn = MySQLdb.connect(host = self.host, 
                                    user = self.user, 
                                    passwd = self.passwd, 
                                    charset = "utf8"
                                    )
        self.cursor = self.conn.cursor()
        
    def get_delete_sql(self, like_str, flag):
        """ 获得删除table的sql语句 ，
		    参数like_str表示要删除的表明胡或者表明的一部分；
			flag有四个值分别是0,1,2,3。
            0表示：以like_str开头的表名
            1表示：以like_str结尾的表名
            2表示：含有like_str的表名
            3表示：精准匹配like_str表名
            
            返回值：返回一个列表
        """
        if flag == 0:
            search_str = "%s%%" % like_str
        elif flag == 1:
            search_str = "%%%s" % like_str
        elif flag == 2:
            search_str = "%%%s%%" % like_str
        elif flag == 3:
            search_str = "%s" % like_str
        else:
            raise ValueError("Invalid arg value; must be 0 or 1 or 2 or 3")
        sql_cmd = "Select CONCAT('drop table if exists ', '%s.', table_name, ';') FROM information_schema.tables Where table_name LIKE '%s';" % (self.db, search_str)
        #下面这条命令可以一次性列出所有待删除的表名。最后返回的列表就会只有一个元素。返回值的类型暂不更改。
        #下面这条命令有些问题，MYSQL中group_concat有长度限制！默认1024；如果我们需要更大，就需要手工去修改配置文件。
        #sql_cmd = "Select CONCAT('drop table if exists ', GROUP_CONCAT('%s.', table_name), ';') FROM information_schema.tables Where table_name LIKE '%s';" % (self.db, search_str)
        self.cursor.execute(sql_cmd)
        res = self.cursor.fetchall()
        if not res:
            return []
        return [j for j in set([i[0] for i in res])]
        
        
    def execute_sql(self, sql_cmd):
        """ 执行sql语句 """
        self.cursor.execute(sql_cmd)
        
    def commit(self):
        """ 提交操作 """
        self.conn.commit()
		
    def rollback(self):
        """ 回滚操作 """
        self.conn.rollback()
    
    def close_db(self):
        """ 关闭数据库  """
        self.cursor.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    sql = MySql(HOST, USER, PASSWORD, DB_NAME)
    sql.connect_db()
    sql_cmd_list = sql.get_delete_sql(TB_NAME, flag = 0)
    sql.execute_sql("SET foreign_key_checks = 0;")              #关闭对外键的检查
    for sql_cmd in sql_cmd_list:
        sql.execute_sql(sql_cmd)
    sql.execute_sql("SET foreign_key_checks = 1;")              #打开对外键的检查
    sql.close_db()
        