# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： XmindToExcel_3.7.py
# Author : v_yanqyu
# Desc: Xmind转Excel（可定义限级）
# Date： 2021/1/15 10:19
'''
import json
import os
import sys,xlrd,xlwt
import importlib
import xmind
sys.setrecursionlimit(100000)
importlib.reload(sys)
from Logger.GlobalLog import Logger
logger = Logger.write_log()#调用日志模块
# 对输入编码转码处理
is_macOS = True
is_python3 = sys.version_info.major == 3
if is_python3: unicode = str
decode_list = ["GB2312", "utf-8", "ISO-8859-2", "ascii", "windows-1252"]

class ReadXmind():
    def __init__(self,filePath=None):
        """
        初始化需要读取的一些字段值
        :param catalog 目录
        :param title 标题
        :param priority 优先级
        :param preconditions 前置条件
        :param input 输入
        :param output 输出
        :param remarks 备注
        :param type 类型
        :param isautomated 是否自动化
        :param creater 创建人
        :param filePath xmind路径
        :param fileName 由于后期创建excel命名用
        """
        self.null = ""
        self.priority_0 = ['flag-red']  # [重要级别-紧急（红旗优先级标志）,标识]
        self.priority_1 = ['priority-1']  # [重要级别-高（1号优先级标志）,标识]
        self.priority_2 = ['priority-2']  # [重要级别-中（2号优先级标志）,标识]
        self.priority_3 = ['priority-3']  # [重要级别-低（3号优先级标志）,标识]
        self.priority_4 = ['priority-4']  # [重要级别-低（4号优先级标志）,标识]
        self.priority_5 = ['priority-5']  # [重要级别-低（5号优先级标志）,标识]
        self.priority_6 = ['priority-6']  # [重要级别-低（6号优先级标志）,标识]
        self.people_orange = ['people-orange']
        self.symbol_attention = ['symbol-attention']
        self.symbol_wrong = ['symbol-wrong']
        # 节点分割符
        self.node_split = '/'  # 节点分割符
        # Xmind备注信息模板解析（严格按照此顺序解析）
        self.xmind_note_model = [['【前提】', '内容'],
                                 ['【输入】', '内容'],
                                 ['【输出】', '内容'],
                                 ['【备注】', '内容']]

        self.markers = [self.null, self.priority_0, self.priority_1, self.priority_2, self.priority_3, self.priority_4,
                        self.priority_5, self.priority_6, self.people_orange, self.symbol_attention, self.symbol_wrong]
        self.xmindPath =filePath

    def readXmind(self):
        """
        读取Xmind文件
        :param fileName 用于到时候存储用的文件名
        :param generalTitle 根标题
        :param generalTopics 最开始的分支起点
        :param priority
        :return:
        """
        workboot = xmind.load(self.xmindPath)
        xmindData = json.loads(workboot.to_prettify_json())[0]

    def analysisXmind(self,xmindInfo):
        """
        解析Xmind内容
        :param titles 总标题
        :param topics 一级topics
        :param topics_num 一级topics_num
        :return:
        """


class ExeclFileHandle():
    def __init__(self):
        """
        初始化需要写入时的字段
        :param list_names 列名顺序用list固定
        :param case_catalog 用例目录
        :param case_name 用例名称
        :param case_id 需求Id||用例编号
        :param case_level 用例等级
        :param preconditions 前置条件
        :param case_steps 用例步骤
        :param expected_results 预期结果
        :param actual_results  实际结果
        :param remarks 备注
        :param case_type 用例类型
        :param isautomated 是否自动化
        :param case_status 用例状态
        :param creater 创建人
        """
        self.list_names = [u"用例目录", u"用例名称",u"需求ID", u"用例等级",u"前置条件", u"用例步骤", u"预期结果",u"实际结果",u"备注", u"用例类型",u"是否自动化" , u"用例状态",u"创建人"]
        self.case_catalog = ""
        self.case_name = ""
        self.case_id = ""
        self.case_level = ""
        self.preconditions = ""
        self.case_steps = ""
        self.expected_results = ""
        self.actual_results = ""
        self.remarks = ""
        self.case_type = ""
        self.isautomated = ""
        self.case_status = ""
        self.creater = ""
        logger.info(self.list_names)

if __name__ == '__main__':
    # ExeclFileHandle()
    ReadXmind(r"E:\WorkSpace\PycharmProjects\AutoFramework\Config\XmindToExcel.xmind").readXmind()
