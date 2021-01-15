# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AppStability.py
# Author : v_yanqyu
# Desc: XmindToExcel
# Date： 2020/1:11 10:57
'''
import os
import xlwt
import xmind
import xlrd
import sys
import copy
import importlib
importlib.reload(sys)
is_macOS = True

def maxConverLevel  (note, num,max):
    lens = note.getSubTopics()
    if lens:
        num = num + 1
        for i in lens:
            result = maxConverLevel (i, num,max)
            if not result:
                return False
    else:
        return False if num > max else True
    return True

class InitVariable(object):
    def __init__(self):
        """
        初始化变量
        """
        self.Casedirectory = ""
        self.Casename = ""
        self.Casetype = ""
        self.Casepriority = ""
        self.Casestep = ""
        self.Caseprecond =""
        self.Caseresult = ""
        self.Casenotes = ""  # 用例备注

    def setdirectory(self, directory):
        """
        用例目录
        :param directory:
        :return:
        """
        self.Casedirectory = directory

    def setname(self, name):
        """
        设置用例名称
        :param name:
        :return:
        """
        self.Casename = name

    def setpriority(self, priority):
        """
        用例优先级
        :param priority:
        :return:
        """
        self.Casepriority = priority

    def setstep(self, step):
        """
        用例步骤
        :param step:
        :return:
        """
        self.Casestep = step

    def setprecond(self, precond):
        """
        用例步骤
        :param step:
        :return:
        """
        self.Caseprecond = precond

    def setresult(self, result):
        """
        设置用例输出
        :param result:
        :return:
        """
        self.Caseresult = result

    def setnotes(self, notes):
       """
       设置用例备注
       :param notes:
       :return:
       """
       self.Casenotes = notes

    def settable(self, table):
        """
        用例层级
        :param table:
        :return:
        """
        self.Casetable = table

class XmindFileHandle:
    def __init__(self):
        self.Case_list = []
        self.markerPriority = {'flag-red': 0, 'priority-1': 1, 'priority-2': 2, 'priority-3': 3,'priority-4': 4,'priority-5': 5,'priority-6': 6,'priority-7': 7}

    def readXmind(self, filePath,maxlevel):
        root_topic = xmind.load(filePath).getPrimarySheet().getRootTopic()  # 根节点，对应用例目录
        topics = root_topic.getSubTopics()  # 二级节点，对应用例功能点
        if topics is None:
            raise RuntimeError("xmind文件不能为空")
        flag_ok1 = [True]
        for note in topics:
            if note.getSubTopics() is None:  # 避免功能节点无子节点导致异常
                if note.getTitle() is not None:
                    print(note.getTitle() + "  节点无子节点")
                continue
            if not maxConverLevel  (note, 2,maxlevel):
                print("xmind层次结构超过%s层，请修改后重试!"%(maxlevel))
            notedic = {}  # 每条分支转换的用例字典
            notepaths = []  # 功能点下所有用例字典列表
            notepaths = self.readTopics(note, notedic, notepaths, flag_ok=flag_ok1)
            for k in range(0, len(notepaths)):  # 循环取每条路径解析存储用例对象
                Casefile = InitVariable()
                Casefile.setdirectory(root_topic.getTitle())
                if notepaths[k].__contains__(u'用例层级'):
                    Casefile.settable(notepaths[k][u'用例层级'])
                else:
                    Casefile.settable(' ')  # 空节点，默认填空
                if notepaths[k].__contains__(u'优先级'):
                    Casefile.setpriority(notepaths[k][u'优先级'])
                if notepaths[k].__contains__(u'前置条件'):
                    Casefile.setprecond(notepaths[k][u'前置条件'])
                if notepaths[k].__contains__(u'输入'):
                    Casefile.setstep(notepaths[k][u'输入'])
                if notepaths[k].__contains__(u'输出'):
                    Casefile.setresult(notepaths[k][u'输出'])
                if notepaths[k].__contains__(u'备注'):
                    Casefile.setnotes(notepaths[k][u'备注'])
                if notepaths[k].__contains__(u'用例名称'):
                    Casefile.setname(notepaths[k][u'用例名称'])
                self.Case_list.append(Casefile)
        if not flag_ok1[0]:
            print("部分测试用例没有标记优先级，请添加后重试!")
        return self.Case_list

    def readTopics(self, note, notesdic={}, notepaths=[], Casepath='', Caseprecond='',Casestep='', Casenote='', flag_ok=[True]):
        lens = note.getSubTopics()
        if not lens:  # 无节点[]，返回
            marks = self.readMarker(note)
            if marks is not None:
                notesdic[u'优先级'] = marks[u'优先级']
                notes = self.readNoteDict(note)
                if notes is not None:
                    if notes.__contains__(u'前置条件'):
                        Caseprecond = notes[u'前置条件']
                    else:
                        Caseprecond = ''
                    if u'输入' in notes.keys():
                        Casestep = notes[u'输入']
                    else:
                        Casestep = ''
                    if notes.__contains__(u'输出'):
                        Caseresult = notes[u'输出']
                    else:
                        Caseresult = ''
                    if notes.__contains__(u'备注'):
                        Casenote = notes[u'备注']
                    else:
                        Casenote = ''
                else:
                    Casestep,Caseprecond,Caseprecond, Caseresult, Casenote = '', '', '','',''
                tempdic = copy.copy(notesdic)
                notesdic = {}
                if note.getTitle() is None:
                    print("预期结果为空")
                    return
                tempdic[u'用例名称'] = note.getTitle()
                tempdic[u'用例层级'] = Casepath
                tempdic[u'前置条件'] = Caseprecond
                tempdic[u'输入'] = Casestep
                tempdic[u'输出'] = Caseresult
                tempdic[u'备注'] = Casenote
                notepaths.append(tempdic)
            else:
                # 作异常处理；
                print("%s ---没有用例优先级标记!" % note.getTitle())
                if not flag_ok[0]:
                    pass
                else:
                    flag_ok[0] = False
            return notepaths
        else:
            if Casepath == '':
                Casepath = note.getTitle()
            else:
                Casepath = Casepath + "-" + note.getTitle()
            for i in lens:
                self.readTopics(i, notesdic, notepaths, Casepath, Casestep,Caseprecond, Casenote, flag_ok)
        return notepaths

    def readNotes(self, topic):
        """获取节点上备注"""
        notes = topic.getNotes()
        if notes == None:  # 无备注直接返回
            return
        notes_str = notes.getContent()
        notes_rows = notes_str.split('\n')
        notes_dict = {}
        for rows in notes_rows:
            if rows[:-1].strip() == "":  # 处理某些行为空行的特殊情况
                continue
            rows = rows.replace(":", "：")  # 替换英文冒号为中文冒号
            row_split = rows.split(u"：")  # 用冒号分割每一行
            if len(row_split) != 2:
                print("备注中:" + rows.encode('utf-8') + "输入格式有误，请检查")
                return None
            notes_dict[(row_split[0].strip())] = str((row_split[1].strip()))  # 最后一个字符为换行符，写入字典时进行了处理
        return notes_dict

    @staticmethod
    def readNoteDict(topic):
        notes_dict = {u"前置条件": '',u"输入": '', u'输出': '', u'备注': ''}  # 可拓展加入其他字段
        key_temp = ''
        value_temp = ''
        replace_list = [(":", "："), ("前置条件：", "前置条件：\n"),  ("输入：", "输入\n"),("输出：", "输出\n"), ("备注：", "备注\n"), ("1、", "\n1、"),
                        ("2、", "\n2、"), ("3、", "\n3、"), ("4、", "\n4、"), ("5、", "\n5、"), ("6、", "\n6、"), ("前置条件  ：", "前置条件  ：\n"),
                        ("输入 ：", "输入\n"), ("输出 ：", "输出\n"), ("备注 ：", "备注\n"), ("输入  ：", "输入\n"), ("输出  ：", "输出\n"),
                        ("备注  ：", "备注\n")]
        notes = topic.getNotes()
        if not notes:  # 无备注直接返回
            return
        notes_str = notes if is_macOS else notes.getContent()
        if  (u"前置条件：" in notes_str) or (u"输入：" in notes_str) or (u"输入：" in notes_str) or (u"输出：" in notes_str) or (u"备注：" in notes_str) or (u"前置条件 ：" in notes_str) or(u"输入 ：" in notes_str) or (
                    u"输出 ：" in notes_str) or (u"备注  ：" in notes_str):
            for mReplace in replace_list:
                notes_str = notes_str.replace(mReplace[0], mReplace[1])
            notes_rows = notes_str.split('\n')
            for rows in notes_rows:
                if rows[:-1].strip() == "":  # 处理某些行为空行的特殊情况
                    continue
                if notes_dict.__contains__(rows):
                    if key_temp != '' and value_temp != '':
                        notes_dict[key_temp] = value_temp
                        key_temp = rows
                        value_temp = ''
                    else:
                        key_temp = rows
                else:
                    if value_temp == '':
                        value_temp = rows
                    else:
                        value_temp = value_temp + '\n' + rows
            else:
                if key_temp != '' and value_temp != '':
                    notes_dict[key_temp] = value_temp
        return notes_dict

    def readMarker(self, topic):
        '''获取节点上标志
        :author  cathy
        :注意点   1、获取topic的所有标识符   2、目前暂时支持标志：数字1-3分别表示用例优先级p0-p2
        :param topic: 主题标题
        :type topic:  TopicElement
        :返回值   包含备注里所有支持标志的一个字典,{'优先级':'';} 若函数执行错误，返回None
        '''

        if topic is None:
            print("主题元素不存在")
            return
        if topic.getTitle() is None:
            print("主题元素内容为空")
            return
        markers = topic.getMarkers()
        if markers is None:
            print( "标题为: " +topic.getTitle()+" 的主题没有标志，读取标志信息失败" )
            return
        dict = {u'优先级': ''}
        # print markers
        for marker in markers:
            mark_str = str(marker.getMarkerId())
            if self.markerPriority.__contains__(mark_str):
                dict[u'优先级'] = self.markerPriority[mark_str]
            else:
                # 其他的标识，那么认为出错
                print("标题为: " + topic.getTitle() + " 的主题存在未指定的标识，读取标志信息失败")
                return None
        return dict

class ExeclFileHandle(InitVariable):
    def __init__(self):
        self.list_names = [u"用例名称", u"是否自动化", u"用例等级", u"前置条件",u"输入",  u"输出", u"备注", u"创建人"]

    def writeExcel(self, list, path=None, filename=None,creater=None):
        root_topic_title = list[0].Casedirectory
        new_workbook = xlwt.Workbook()  # 创建新的工作簿
        sheet1 = new_workbook.add_sheet(root_topic_title, cell_overwrite_ok=True)
        sheet1.set_panes_frozen(True)
        sheet1.set_horz_split_pos(1)  # 冻结首行
        # 设置格式
        sheet1.col(0).width = 256 * 50
        sheet1.col(1).width = 256 * 13
        sheet1.col(2).width = 256 * 13
        sheet1.col(3).width = 256 * 30
        sheet1.col(4).width = 256 * 70
        sheet1.col(5).width = 256 * 60
        sheet1.col(6).width = 256 * 30
        sheet1.col(7).width = 256 * 20
        xlwt.add_palette_colour("custom_colour", 0x21)
        new_workbook.set_colour_RGB(0x21, 146, 205, 220)
        xlwt.add_palette_colour("custom_colour1", 0x22)
        new_workbook.set_colour_RGB(0x22, 196, 215, 155)
        xlwt.add_palette_colour("custom_colour2", 0x23)
        new_workbook.set_colour_RGB(0x23, 149, 179, 215)
        xlwt.add_palette_colour("custom_colour3", 0x25)
        new_workbook.set_colour_RGB(0x23, 149, 179, 215)
        style_title = xlwt.easyxf(
            'font:bold on,name Arial;align:wrap on;borders:left thin,right thin,top thin,bottom thin;pattern:pattern solid,fore_colour orange')
        style_table1 = xlwt.easyxf(
            'font:bold on,name Arial;align:wrap on;borders:left thin,right thin,top thin,bottom thin;pattern:pattern solid,fore_colour custom_colour')
        style_table2 = xlwt.easyxf(
            'font:bold on,name Arial;align:wrap on;borders:left thin,right thin,top thin,bottom thin;pattern:pattern solid,fore_colour custom_colour1')
        style_table3 = xlwt.easyxf(
            'font:bold on,name Arial;align:wrap on;borders:left thin,right thin,top thin,bottom thin;pattern:pattern solid,fore_colour custom_colour2')
        style_table5 = xlwt.easyxf(
            'font:bold on,name Arial;align:wrap on;borders:left thin,right thin,top thin,bottom thin;pattern:pattern solid,fore_colour custom_colour3')
        style_item = xlwt.easyxf(
            'font:name Times New Roman;align:wrap on,vert center;borders:left thin,right thin,top thin,bottom thin')
        style_item_for_prioroty = xlwt.easyxf(
            'font:name Arial;align:wrap on,vert center,horz center;borders:left thin,right thin,top thin,bottom thin')
        if (not list):  # list不能为空
            print("用例列表为空，不能写入excel")
            return False
        for i in range(0, len(self.list_names)):
            sheet1.write(0, i, self.list_names[i], style_title)
        k = 0
        dir0, dir1, dir2,dir3 = [], [], [],[]
        for rows in range(0, len(list)):
            if list[rows].Casetable != '':
                table_list = list[rows].Casetable.split('_')
                for m in range(0, len(table_list)):
                    table_temp = table_list[m].replace('*', '')
                    if 0 == m and table_temp not in dir0:
                        dir0.append(table_temp)
                        dir1, dir2 = [], []
                        sheet1.write_merge(k + rows + 1, k + rows + 1, 0, 7, ('*' + table_temp),style_table1)  # 0，6表示的是列的index
                        k += 1
                    if 1 == m and table_temp not in dir1:
                        dir1.append(table_temp)
                        dir2 = []
                        sheet1.write_merge(k + rows + 1, k + rows + 1, 0, 7, ('**' + table_temp),style_table2)
                        k += 1
                    if 2 == m and table_temp not in dir2:
                        dir2.append(table_temp)
                        sheet1.write_merge(k + rows + 1, k + rows + 1, 0, 7, ('***' + table_temp),style_table3)
                        k += 1
                    if 3 == m and table_temp not in dir3:
                        dir3.append(table_temp)
                        sheet1.write_merge(k + rows + 1, k + rows + 1, 0, 7, ('****' + table_temp),style_table5)
                        k += 1

            sheet1.write(k + rows + 1, 0, list[rows].Casename, style_item)
            # 是否自动化暂时为空
            sheet1.write(k + rows + 1, 1, '', style_item)
            sheet1.write(k + rows + 1, 2, list[rows].Casepriority, style_item_for_prioroty)
            sheet1.write(k + rows + 1, 3, list[rows].Caseprecond, style_item)
            sheet1.write(k + rows + 1, 4, list[rows].Casestep, style_item)
            sheet1.write(k + rows + 1, 5, list[rows].Caseresult, style_item)
            # 备注
            sheet1.write(k + rows + 1, 6, list[rows].Casenotes, style_item)
            # 创建人暂时为空
            sheet1.write(k + rows + 1, 7, creater, style_item)
        if (filename == None):
            filename = list[0].Casedirectory
        else:
            self.filename = filename
        if (path == None):
            path = os.getcwd()
        savepath = path + os.sep + filename + '.xls'
        new_workbook.save(savepath)
        return savepath

    def mergeExcel(self, fristExcel, secondExcel):
        '''合并2个execl的测试用例  '''
        list1 = []
        fristWb = xlrd.open_workbook(fristExcel, 'r')
        secondWb = xlrd.open_workbook(secondExcel, 'r')
        wb = copy(fristWb)
        sheet1 = fristWb.sheets()[0]
        sheet2 = secondWb.sheets()[0]
        rows1 = sheet1.nrows
        rows2 = sheet2.nrows
        for row2 in range(0, rows2):
            '''0:相同，1：不同'''
            flag = 0
            for row1 in range(0, rows1):
                '''相同格式的两个文件，‘用例名称’为第二列，判断用例名称是否相同'''
                if sheet2.cell(row2, 1).value == sheet1.cell(row1, 1).value:
                    flag = 0
                    break
                if sheet2.cell(row2, 1).value != sheet1.cell(row1, 1).value:
                    flag = 1
                    continue
            '''将不同那行信息存入列表'''
            if flag == 1:
                list1.append(sheet2.row_values(row2))

        ws = wb.get_sheet(0)
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                ws.write(rows1 + i, j, list1[i][j])
        '''写入文件'''
        wb.save(fristExcel)


if __name__ == '__main__':
    instruct = "\
    #########################################################\n\
                    Xmind转Excel工具 By Liquor\n\
    #########################################################\n\
    使用规范如下：\n\
    1、xmind文件不超过10级分层；\n \
    2、根节点为需求或模块名称，末节点为用例名称，中间节点为1-9级目录； \n\
    3、末节点必须包含用例优先级标志（添加用例优先级方法，末节点--右键  \n\
    --图标--任务优先级/旗子，其中红旗为0级，优先级1-6为用例1-6级）；\n\
    4、节点上的备注可选填 输入/输出/备注"
    print(instruct)
    while True:
        filePath = input(r"请将要转换的xmind文件拖至此处,按q退出:").replace('"', '')
        xlsFileName = filePath.split(os.sep)[-1].replace(".xmind", "")
        xlsFilePath = os.path.split(filePath)[0]
        if filePath.split('.')[-1] == 'xmind':
            XmindHandle = XmindFileHandle()
            ExeclHandle = ExeclFileHandle()
            lists = XmindHandle.readXmind(filePath, 10) # 级别限制
            if lists == None:
                print("请检查xmind编写是否符合规范")
            else:
                execl_filePath = ExeclHandle.writeExcel(lists, xlsFilePath, xlsFileName,input("请输入创建人："))
                print("转换后execl路径:%s" % execl_filePath)
        else:
            print("输入文件非xmind和xls类型!!")
