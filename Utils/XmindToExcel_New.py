# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： XmindToExcel_New.py
# Author : v_yanqyu
# Desc: Xmind转Excel（可定义限级）
# Date： 2021/1/15 10:19
'''
import json,linecache
import os,sys,time,importlib,xmind
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
        self.default = []
        self.today = time.strftime("%Y%m%d").replace("4","6")
        self.priority_0 = ['flag-red',0]  # [重要级别-紧急（红旗优先级标志）,标识]
        self.priority_1 = ['priority-1',1]  # [重要级别-高（1号优先级标志）,标识]
        self.priority_2 = ['priority-2',2]  # [重要级别-中（2号优先级标志）,标识]
        self.priority_3 = ['priority-3',3]  # [重要级别-低（3号优先级标志）,标识]
        self.priority_4 = ['priority-4',4]  # [重要级别-低（4号优先级标志）,标识]
        self.priority_5 = ['priority-5',5]  # [重要级别-低（5号优先级标志）,标识]
        self.priority_6 = ['priority-6',6]  # [重要级别-低（6号优先级标志）,标识]
        # 节点分割符
        self.node_split = '/'  # 节点分割符
        # Xmind备注信息模板解析（严格按照此顺序解析）
        self.xmind_note_model = [['【前提】', '内容'],
                                 ['【输入】', '内容'],
                                 ['【输出】', '内容'],
                                 ['【备注】', '内容']]

        self.markers = [self.priority_0[1], self.priority_1[1], self.priority_2[1],
                        self.priority_3[1], self.priority_4[1],self.priority_5[1], self.priority_6[1] ]
        if filePath !=None:
            self.xmindPath = filePath
        else:
            self.xmindPath =""
        head,tail = os.path.split(os.getcwd())
        self.addNote = "%s\Result\%s-addNote.txt"%(head,self.today)

    def readXmind(self):
        """
        读取Xmind文件
        :param fileName 用于到时候存储用的文件名
        :param generalMarkers 根标识
        :return:
        """
        workboot = xmind.load(self.xmindPath)
        xmindData = json.loads(workboot.to_prettify_json())[0]
        generalMarkers = xmindData["topic"]["markers"]
        topic = xmindData["topic"]
        title = topic["title"]
        topics = topic["topics"]
        if os.path.exists(self.addNote):
            os.remove(self.addNote)
        if generalMarkers == []: # 判断特定的级别不允许设置标识
            self.analysisXmind(title,topics)
        else:
            logger.error("%s"%(generalMarkers))

    def analysisXmind(self,title,topics):
        """
        解析Xmind内容
        :param title 总标题
        :param topic topic分级开始
        :return:
        """
        for top in topics:
            if type(top) == dict :
                if len(top) > 7:
                    title = top["title"]
                    topics = top["topics"]
                    self.analysisXmind(title, topics)
                    if len(topics[0]) > 7:  # 主要提取最后一个
                        self.analysisXmind(title, topics[0])
                else:
                    # logger.info("最终的集合还需再次清洗一遍：%s" % (top))
                    id = top["title"]
                    title = top["title"]
                    note = top["note"]
                    markers = top["markers"]
                    result = {"title":title,"note":note,"markers":markers}
                    with open(self.addNote, "a", encoding="utf-8") as file:
                        file.write("%s\r" % (result))

    def clearNote(self):
        """
        清洗数据
        :return:
        """
        with open(self.addNote,"r",encoding="utf-8") as file:
            line = file.readlines()
            for i in range(len(line)):
                line  = linecache.getline(self.addNote,i).strip()
                if line !="":
                    logger.info("检索到已清洗好的数据：%s"%(line))

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
    ReadXmind().clearNote()
