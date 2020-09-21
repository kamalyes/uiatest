#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
@File  :LibraryManage.py
@Author:v_yanqyu
@Desc  : Py第三方库管理类
@Date  :2020/9/21 13:18
'''
import subprocess
from Logger import GlobalLog  # 导入日志模块
logger = GlobalLog.Logger.write_log() #调用日志模块

class JarManage():
    def check_import(self,filepath):
        """
        导入所需要的第三方库
        :return:
        """
        try:
            jarlist = []
            file = open(filepath, encoding='utf-8')
            while True:
                content = file.readline()
                if content == '':
                    break
                else:
                    jarlist.append(content.strip())
            file.close()
            for i in range(len(jarlist)):
                # logger.info(jarlist[i])
                __import__(jarlist[i])
        except Exception as IOError:
            logger.error(IOError)

    def updatejar(self):
        """
        # 批量更新python所有的三方库
        :param com_list 显示需要更新的python列表并存储到list中
        :return:
        """
        com_list = 'pip list -o'
        list = subprocess.Popen(com_list, shell=True, stdout=subprocess.PIPE)
        out = list.communicate()[0]
        # 二进制转utf-8字符串
        out = str(out, 'utf-8')

        # 切出待升级的包名, 并存入列表
        need_update = []
        for i in out.splitlines()[2:]:
            need_update.append(i.split(' ')[0])

        # 执行升级命令，每次取一个包进行升级，pip只支持一个包一个包的升级
        for nu in need_update:
            com_update = 'pip install -U {py}'.format(py=nu)
            subprocess.call(com_update)
        logger.info("检查更新情况:")
        subprocess.call(com_list)

JarManage().check_import(filepath=r'../requirements.txt')
# JarManage().updatejar()
