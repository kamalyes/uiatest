#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： IniHandle.py
# Author : v_yanqyu
# Desc: ConfigFile 节点处理类
# Date： 2020/9/6 15:55
'''
__author__ = 'v_yanqyu'
import os,configparser
from Logger import GlobalLog
logger = GlobalLog.Logger().write_log()#调用日志模块

class IniHandle():
    def __init__(self):
        """
        初始化
        """
        self.conf = configparser.ConfigParser()
        self.filepath = ''

    def checkSection(self, section):
        """
        检查节点
        :param section: 
        :return: 
        """
        try:
            self.conf.items(section)
        except Exception:
            logger.info(">> 无此section，请核对[%s]" % section)
            return None
        return True

    def readSectionItems(self, filepath):
        """
        读取ini，并获取所有的section名
        :param filepath: 
        :return: 
        """
        if not os.path.isfile(filepath):
            logger.info(">> 无此文件，请核对路径[%s]" % filepath)
            return None
        self.filepath = filepath
        self.conf.read(filepath, encoding="utf-8")
        return self.conf.sections()

    def readOneSection(self, section):
        """
        读取一个section，list里面对象是元祖
        :param section:
        :return:
        """
        try:
            item = self.conf.items(section)
        except Exception:
            logger.info(">> 无此section，请核对[%s]" % section)
            return None
        return item

    def prettySecToDic(self, section):
        """
        读取一个section到字典中
        :param section:
        :return:
        """
        if not self.checkSection(section):
            return None
        res = {}
        for key, val in self.conf.items(section):
            res[key] = val
        return res

    def prettySecsToDic(self):
        """
        读取所有section到字典中
        :return:
        """
        res_1 = {}
        res_2 = {}
        sections = self.conf.sections()
        for sec in sections:
            for key, val in self.conf.items(sec):
                res_2[key] = val
            res_1[sec] = res_2.copy()
            res_2.clear()
        return res_1

    def removeItem(self, section, key):
        """
        删除一个 section中的一个item（以键值KEY为标识）
        :param section:
        :param key:
        :return:
        """
        if not self.checkSection(section):
            return
        self.conf.remove_option(section, key)

    def removeSection(self, section):
        """
        删除整个section这一项
        :param section:
        :return:
        """
        if not self.checkSection(section):
            return
        self.conf.remove_section(section)

    def addSection(self, section):
        """
        添加一个section
        :param section:
        :return:
        """
        self.conf.add_section(section)

    def addItem(self, section, key, value):
        """
        往section添加key和value
        :param section:
        :param key:
        :param value:
        :return:
        """
        if not self.checkSection(section):
            return
        self.conf.set(section, key, value)

    def actionOperate(self, mode):
        """
        执行write写入, remove和set方法并没有真正的修改ini文件内容，只有当执行conf.write()方法的时候，才会修改ini文件内容
        :param mode:
        :return:
        """
        if mode == 'r+':
            self.conf.write(open(self.filepath, "r+", encoding="utf-8"))   # 修改模式
        elif mode == 'w':
            self.conf.write(open(self.filepath, "w"))                      # 删除原文件重新写入
        elif mode == 'a':
            self.conf.write(open(self.filepath, "a"))                      # 追加模式写入


if __name__ == '__main__':
    filepath = r'../Config/config.ini'
    IniHandle = IniHandle()
    sections = IniHandle.readSectionItems(filepath)
    content = IniHandle.readOneSection('MySQL-Info')
    logger.info("扫描单个子节点下的所有键值：%s"%(content))
    logger.info("扫描到ini配置文件中所有的节点：%s"%(sections))
    content = IniHandle.readOneSection('MySQL-Info')
    logger.info("扫描单个子节点下的所有键值：%s"%(content))
    dic = IniHandle.prettySecToDic('MySQL-Info')
    logger.info("读取单个子节点的所有内容以字典形式展示：%s"%(dic))
    dics = IniHandle.prettySecsToDic()
    logger.info("读取所有节点的内容以字典形式展示：%s"%(dics))