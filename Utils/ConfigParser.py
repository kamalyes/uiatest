# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ConfigParser.py
# Author : v_yanqyu
# Desc: ConfigFile 节点处理类
# Date： 2020/9/6 15:55
'''

import configparser
from Logger.GlobalLog import Logger
logger = Logger.write_log()#调用日志模块

class IniHandle():
    @classmethod
    def openconfig(self,filepath=None):
        """
        打开指定的ini文件
        :param filepath:
        :return: <configparser.ConfigParser object at 0x0000015940785BA8>
        """
        try:
            # logger.info('设置Ini文件路径：%s'%(filepath))
            if filepath is None:
                filepath = r'../Config/config.ini'
            conf = configparser.ConfigParser()
            conf.read(filepath, encoding="utf-8")
            return conf
        except Exception as FileNotFoundError:
            logger.error("文件读取失败，请检查%s是否存在"%(filepath))

    @classmethod
    def allsection(self,filepath=None):
        """
        获取ini文件下所有的section值
        :return:  all_section
        """
        conf = self.openconfig(filepath)
        return conf.sections()

    @classmethod
    def options(self,section_name,filepath=None):
        """
        获取指定section的所有option
        :return:
        """
        conf = self.openconfig(filepath)
        if conf.has_section(section_name):
            return conf.options(section_name)
        else:
            raise ValueError(section_name)

    @classmethod
    def optvalue(self,node,key,filepath=None):
        """
        获取指定section下option的value值
        :param filepath 需要读取的文件
        :param node 父类节点
        :param key  所需要查询内容的单一key
        :return: result 返回对应key的value值
        """
        conf = self.openconfig(filepath)
        result = conf.get(node, key)
        return result

    @classmethod
    def all_items(self,section,filepath=None):
        """
        获取指定section下的option的键值对
        :return: List形式的 [('a', 'b'),('aa', 'bb')]
        """
        conf = self.openconfig(filepath)
        if conf.has_section(section):
            return conf.items(section)

    @classmethod
    def  all_items(self,filepath=None):
        """
        打印配置文件所有的值(该方法并不是很常用)
        :return:
        """
        conf = self.openconfig(filepath)
        for section in self.allsection():
            logger.info("[" + section + "]")
            for K, V in conf.items(section):
                logger.info(K + "=" + V)


if __name__ == '__main__':
    filepath = r'../Config/config.ini'
    logger.info(IniHandle.openconfig(filepath))
    logger.info(IniHandle.optvalue(node="Proxy_Setting",key="proxy_switch"))
    logger.info(IniHandle.allsection())
    logger.info(IniHandle.options(section_name="Proxy_Setting"))
    # logger.info(IniHandle.all_items())
