# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : MySQLDB.py
@Author: YuYanQing
@Desc  : MySQL驱动类
@Date  : 2020/10/1 9:11
'''
import pandas as pd
import MySQLdb
class MysqlTools(object) :
    def __init__(self,host,user,pass_word,database = None,port = 3306) :
        self.MYSQL_HOST       =     host
        self.MYSQL_USER       =     user
        self.MYSQL_PW         =     pass_word
        self.MYSQL_DATABASE   =     database
        self.MYSQL_PORT       =     port
        self.conn             =     None
        self.cur              =     None

    def init(self) :
        """
        连接数据库
        """
        if self.MYSQL_DATABASE != None :
            self.conn= MySQLdb.connect(
            host    =   self.MYSQL_HOST,
            port    =   self.MYSQL_PORT,
            user    =   self.MYSQL_USER,
            passwd  =   self.MYSQL_PW,
            db      =   self.MYSQL_DATABASE,
            charset='utf8'
            )
            self.cur = self.conn.cursor()
            self.cur.execute("show tables")
            desc = self.cur.fetchall()
        else :
            self.conn= MySQLdb.connect(
            host    =   self.MYSQL_HOST,
            port    =   self.MYSQL_PORT,
            user    =   self.MYSQL_USER,
            passwd  =   self.MYSQL_PW,
            charset='utf8'
            )
            self.cur = self.conn.cursor()
            self.cur.execute("show databases")
            desc = self.cur.fetchall()

    def call_sql(self,sql) :
        '''
        查询数据
        返回结果为pandas的DataFrame
        '''
        try :
            return pd.read_sql_query(sql,self.conn)
        except Exception as e :
            raise Exception('sql:%s,error:%s' % (sql,e))

    def do_sql(self,sql) :
        '''
        修改数据
        执行相关sql
        '''
        try :
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e :
            raise Exception('sql:%s,error:%s' % (sql,e))

    def to_sql(self,df,table_name,index=False) :
        '''
        DataFrame写入mysql的table
        '''
        df.to_sql(table_name, self.conn, index=index)

    def restart(self):
        """
        重启
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.init()

    def __del__(self) :
        '''
        对象结束
        '''
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    msq = MysqlTools(host='139.196.120.128', user='root', pass_word='QINg0201$', database='student', port=3306)
    msq.init()  # init函数为连接数据库
    data = msq.call_sql('select * from china limit 10')
    print(data)
    # msq.do_sql(r"INSERT INTO `china` VALUES ('05', '中国', '0');")
    msq.to_sql(df=data_df, table_name='test_table', index=False)


