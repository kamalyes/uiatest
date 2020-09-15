#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： Insert_DB.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/9/15 18:51
'''
__author__ = 'v_yanqyu'
from Logger import GlobalLog
logger = GlobalLog.Logger.write_log()
from Common.MysqlManager import MySQLConnection

def insertByIndex():
    """
    使用下标索引的方式插入数据
    """
    sql = "insert into user(id,name) values(%s,%s)"
    # 获取数据库连接
    connect = MySQLConnection()
    try:
        # 执行插入动作
        connect.insert(sql, ("1", "张三"))
        # 提交
        connect.commit()
    except Exception as TypeError:
        logger.error(TypeError)
    finally:
        # 关闭数据库连接
        connect.close()


def insertBatchByIndex():
    """
    使用下标索引的方式批量插入数据
    """
    sql = "insert into user(id,name) values(%s,%s)"
    # 获取数据库连接
    connect = MySQLConnection()
    try:
        # 执行批量插入动作
        data = []
        # 放入的是元祖
        data.append(("1", "张三"))
        data.append(("2", "张三2"))
        connect.batch(sql, data)
        # 提交
        connect.commit()
    except Exception as TypeError:
        logger.error(TypeError)
    finally:
        # 关闭数据库连接
        connect.close()


def insertByDict():
    """
    使用下标索引的方式插入数据
    """
    sql = "insert into user(id,name) values(%(id)s,%(name)s)"
    # 获取数据库连接
    connect = MySQLConnection()
    try:
        # 执行插入动作
        # 此时我们使用的是字典
        connect.insert(sql, {"name": "张三", "id": "1"})
        # 提交,必须
        connect.commit()
    except Exception as TypeError:
        logger.error(TypeError)
    finally:
        # 关闭数据库连接,必须
        connect.close()


def insertBatchByDict():
    """
    使用下标索引的方式批量插入数据
    """
    sql = "insert into user(id,name) values(%(id)s,%(name)s)"
    # 获取数据库连接
    connect = MySQLConnection()
    try:
        # 执行批量插入动作
        data = []
        # 放入的是自字典
        data.append({"name": "张三", "id": "1"})
        data.append({"name": "张三1", "id": "2"})
        connect.batch(sql, data)
        # 提交
        connect.commit()
    except Exception as TypeError:
        logger.error(TypeError)
    finally:
        # 关闭数据库连接
        connect.close()

sql="select id,name,address from restaurant where province=%s "
connect=MySQLConnection()
try:
      page=1
      size=500
      pagination=connect.listByPage(sql,page,size,'浙江省')
except Exception as TypeError:
    logger.error(TypeError)
finally:
    # 关闭数据库连接
    connect.close()