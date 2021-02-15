# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： XmindToTapd_Tools.py
# Author : YuYanQing
# Desc: XmindToTapd小工具
# Date： 2020/7/16 15:55
'''
import os,xlwt,xmind
import logging,xlrd,chardet
# 为了解决向excel中写入中文字符的问题
import sys,copy,importlib
importlib.reload(sys)
# 对输入编码转码处理
decode_list = ["GB2312", "utf-8", "ISO-8859-2", "ascii", "windows-1252"]
NULL = None
is_macOS = True
is_python3 = sys.version_info.major == 3
if is_python3:
    unicode = str

def get_decode_str(en_string):
    if isinstance(en_string, unicode):
        return en_string
    if en_string is None:
        return ''
    encode_info = chardet.detect(en_string)
    # 如果为 None
    if not encode_info["encoding"]:
        return en_string
    de_string = en_string
    for key in decode_list:
        try:
            # print("try to decode by %s" % key)
            de_string = en_string.decode(key)
            # print("success to decode by %s" % key)
            break
        except Exception:
            continue
    return de_string

# 限定xmind用例层次为10层
def max_sub_num_is_true(note, num):
    print(note.getTitle())
    lens = note.getSubTopics()
    if lens:
        num = num + 1
        for i in lens:
            result = max_sub_num_is_true(i, num)
            if not result:
                return False
    else:
        return False if num > 10 else True
    return True


class FormatError(Exception):
    def __init__(self, note):
        self.note = note if is_macOS else note.encode('gb18030')
    def __str__(self):
        return repr(self.note)


# 用例类，
class case(object):
    def __init__(self):
        '''用例目录	用例名称	需求ID	前置条件	用例步骤	预期结果	用例类型	用例状态	用例等级	创建人'''
        self.caseid = ""
        self.casename = ""
        self.story_id = ""
        self.casedirectory = ""
        self.caseversion = ""
        self.casetype = ""
        self.casepriority = ""
        self.casestep = ""
        self.caseresult = ""
        self.casefunction = ""
        self.casenotes = ""  # 用例备注
        self.caseprecondition = ""
        self.casedescribe = ""
        self.user_name = ""

    def properties(self):
        """返回该类的所有属性
        :return 所有属性放在一个list中
        """
        list_properties = []
        for key in vars(self).items():
            list_properties.append(key)
        return list_properties

    def setcaseid(self, id):
        """设置用例ID
        :param id: 对应ATT平台上的用例ID
        :type id:  string
        """
        self.caseid = id

    def setcasename(self, name):
        """设置用例名称
        :param name: 用例名称
        :type name:  string
        """
        self.casename = name

    def setStoryId(self, story_id):
        """设置需求ID
        :param name: 用例名称
        :type name:  string
        """
        self.story_id = story_id

    def setStoryId(self, username):
        """设置创建人
        :param name: 创建人
        :type name:  string
        """
        self.username = username

    def setcasedirectory(self, directory):
        """设置用例目录
        :param directory: 用例目录名称
        :type directory:  string
        """
        self.casedirectory = directory

    def setcaseversion(self, version):
        """设置用例版本号
        :param version: version号
        :type version:  string
        """
        self.caseversion = version

    def setcasetype(self, type):
        """设置用例类型
        :param type: 用例类型
        :type type:  string
        """
        self.casetype = type

    def setcasepriority(self, priority):
        """设置用例优先级
        :param priority: 用例优先级
        :type priority:  string
        """
        self.casepriority = priority

    def setcasestep(self, step):
        """设置用例输入
        :param step: 用例步骤
        :type step:  string
        """
        self.casestep = step

    def setcaseresult(self, result):
        """设置用例输出
        :param result: 用例结果
        :type result:  string
        """
        self.caseresult = result


    def setcasefunction(self, function):
        """设置用例关联的功能点
        :param function: 用例功能点
        :type function:  string
        """
        self.casefunction = function


    def setcasenotes(self, notes):
        """设置用例备注
        :param notes: 用例备注
        :type notes:  string
        """
        self.casenotes = notes

    def setcasedescribe(self, describe):
        """设置用例描述
        :param describe: 用例描述
        :type describe:  string
        """
        self.casedescribe = describe

    def setcaseprecondition(self, precondition):
        """设置用例前提条件
        :param precondition: 用例前提条件
        :type precondition:  string
        """
        self.caseprecondition = precondition


    # 增加用例层级
    def setcasetable(self, table):
        """设置用例名称
        :param table: 用例层级
        :type table:  string
        """
        self.casetable = table

class XmindFileHandle:
    # 初始化一些需要用到的列表，及对象
    def __init__(self):
        self.case_list = []
        # 根据需要修改
        self.marker_to_priority = {'flag-red': 0, 'priority-1': 1, 'priority-2': 2, 'priority-3': 3,'priority-4': 4,'priority-5': 5,'priority-6': 6,'priority-7': 7}

    def read_xmind(self, filepath):
        ver = ""  # 版本号
        xmind_file = xmind.load(filepath)
        ele = xmind_file.getPrimarySheet()
        root_topic = ele.getRootTopic()  # 根节点，对应用例目录
        topics = root_topic.getSubTopics()  # 二级节点，对应用例功能点
        if topics is None:
            raise RuntimeError("xmind文件不能为空")
        flag_ok1 = [True]
        for note in topics:
            if note.getSubTopics() is None:  # 避免功能节点无子节点导致异常
                if note.getTitle() is not None:
                    self.log_print(note.getTitle() + "  节点无子节点")
                continue
            if not max_sub_num_is_true(note, 2):
                raise FormatError("xmind层次结构超过8层，请修改后重试!")
            notedic = {}  # 每条分支转换的用例字典
            notepaths = []  # 功能点下所有用例字典列表
            notepaths = self.read_topics(note, notedic, notepaths, flag_ok=flag_ok1)
            for k in range(0, len(notepaths)):  # 循环取每条路径解析存储用例对象
                casefile = case()
                casefile.setcasedirectory(root_topic.getTitle())
                casefile.setcasefunction(note.getTitle())
                casefile.setcaseversion(ver)
                if notepaths[k].__contains__(u'用例层级'):
                    casefile.setcasetable(notepaths[k][u'用例层级'])
                else:
                    casefile.setcasetable(' ')  # 空节点，默认填空
                if notepaths[k].__contains__(u'优先级'):
                    casefile.setcasepriority(notepaths[k][u'优先级'])
                if notepaths[k].__contains__(u'输入'):
                    casefile.setcasestep(notepaths[k][u'输入'])
                if notepaths[k].__contains__(u'输出'):
                    casefile.setcaseresult(notepaths[k][u'输出'])
                if notepaths[k].__contains__(u'备注'):
                    casefile.setcasenotes(notepaths[k][u'备注'])
                # 用例类型不标记默认为功能逻辑，标志减号则为兼容性
                if notepaths[k].__contains__(u'用例类型'):
                    casefile.setcasetype(notepaths[k][u'用例类型'])
                else:
                    casefile.setcasetype(u"功能逻辑")
                if notepaths[k].__contains__(u'用例名称'):
                    casefile.setcasename(notepaths[k][u'用例名称'])
                if notepaths[k].__contains__(u'用例描述'):
                    casefile.setcasedescribe(notepaths[k][u'用例描述'])
                if notepaths[k].__contains__(u'前提条件'):
                    casefile.setcaseprecondition(notepaths[k][u'前提条件'])
                self.case_list.append(casefile)
        if not flag_ok1[0]:
            raise FormatError("部分测试用例没有标记优先级，请添加后重试!")
        return self.case_list

    def read_topics(self, note, notesdic={}, notepaths=[], casepath='', casestep='', casenote='', flag_ok=[True]):
        lens = note.getSubTopics()
        if not lens:  # 无节点[]，返回
            marks = self.readmark(note)
            if marks is not None:
                notesdic[u'优先级'] = marks[u'优先级']
                notes = self.read_note_to_dict(note)
                if notes is not None:
                    if u'输入' in notes.keys():
                        casestep = notes[u'输入']
                    else:
                        casestep = ''
                    if notes.__contains__(u'输出'):
                        caseresult = notes[u'输出']
                    else:
                        caseresult = ''
                    if notes.__contains__(u'备注'):
                        casenote = notes[u'备注']
                    else:
                        casenote = ''
                else:
                    casestep, caseresult, casenote = '', '', ''
                tempdic = copy.copy(notesdic)
                notesdic = {}
                if note.getTitle() is None:
                    self.log_print("预期结果为空")
                    return
                tempdic[u'用例名称'] = note.getTitle()
                tempdic[u'用例层级'] = casepath
                tempdic[u'输入'] = casestep
                tempdic[u'输出'] = caseresult
                tempdic[u'备注'] = casenote
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
            if casepath == '':
                casepath = note.getTitle()
            else:
                casepath = casepath + "-" + note.getTitle()
            for i in lens:
                self.read_topics(i, notesdic, notepaths, casepath, casestep, casenote, flag_ok)
        return notepaths

    def read_notes(self, topic):
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
                self.log_print("备注中:" + rows.encode('utf-8') + "输入格式有误，请检查")
                return None
            notes_dict[get_decode_str(row_split[0].strip())] = str(
                get_decode_str(row_split[1].strip()))  # 最后一个字符为换行符，写入字典时进行了处理
        return notes_dict

    @staticmethod
    def read_note_to_dict(topic):
        notes_dict = {u"输入": '', u'输出': '', u'备注': ''}  # 可拓展加入其他字段
        key_temp = ''
        value_temp = ''
        replace_list = [(":", "："), ("输入：", "输入\n"), ("输出：", "输出\n"), ("备注：", "备注\n"), ("1、", "\n1、"),
                        ("2、", "\n2、"), ("3、", "\n3、"), ("4、", "\n4、"), ("5、", "\n5、"), ("6、", "\n6、"),
                        ("输入 ：", "输入\n"), ("输出 ：", "输出\n"), ("备注 ：", "备注\n"), ("输入  ：", "输入\n"), ("输出  ：", "输出\n"),
                        ("备注  ：", "备注\n")]
        notes = topic.getNotes()
        if not notes:  # 无备注直接返回
            return
        notes_str = notes if is_macOS else notes.getContent().decode('utf-8')
        if (u"输入：" in notes_str) or (u"输出：" in notes_str) or (u"备注：" in notes_str) or (u"输入 ：" in notes_str) or (
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

    def readmark(self, topic):
        if topic is None:
            self.log_print("主题元素不存在")
            return
        if topic.getTitle() is None:
            self.log_print("主题元素内容为空")
            return
        markers = topic.getMarkers()
        if markers is None:
            return
        dict = {u'优先级': ''}
        for marker in markers:
            mark_str = str(marker.getMarkerId())
            if self.marker_to_priority.__contains__(mark_str):
                dict[u'优先级'] = self.marker_to_priority[mark_str]
            else:
                # 其他的标识，那么认为出错
                self.log_print("标题为: " + topic.getTitle() + " 的主题存在未指定的标识，读取标志信息失败")
                return None
        return dict

    @staticmethod
    def log_print(msg):
        """打印指定的日志信息
        :author  gordanjiang
        :param msg: 日志信息
        :type msg:  string
        """
        log_msg = "INFO: " + msg if is_macOS else ("INFO: " + msg).encode('gb18030')
        print(log_msg)


class ExeclFileHandle(case):
    def __init__(self):
        # 列名顺序用list固定
        self.list_names = [u"用例目录", u"用例名称", u"需求ID", u"前置条件", u"用例步骤", u"预期结果", u"用例类型", u"用例状态", u"用例等级", u"创建人"]
        self.filename = []

    def read_excel_file(self, filepath):
        bk = xlrd.open_workbook(filepath)
        sheet_list = []
        table = bk.sheets()[0]
        rows = table.nrows
        cols = table.ncols
        for i in range(0, rows):  # 行
            dics = {}  # 存储每行用例
            for j in range(0, cols):  # 列
                if table.cell(0, j).value in self.list_names:
                    dics[table.cell(0, j).value] = table.cell(i, j).value
            if i == 0:  # 去掉用例excel里第一行列表名
                continue
            sheet_list.append(dics)
        return sheet_list

    def write_excel_file(self, list, path, filename, story_id,username):
        # 取出首节点的名称；
        root_topic_title = list[0].casedirectory if is_macOS else list[0].casedirectory.decode('utf-8')
        new_workbook = xlwt.Workbook()  # 创建新的工作簿
        sheet1 = new_workbook.add_sheet(root_topic_title, cell_overwrite_ok=True)
        sheet1.set_panes_frozen(True)
        sheet1.set_horz_split_pos(1)  # 冻结首行
        # 设置格式
        sheet1.col(0).width = 256 * 40
        sheet1.col(1).width = 256 * 60
        sheet1.col(2).width = 256 * 15
        sheet1.col(3).width = 256 * 50
        sheet1.col(4).width = 256 * 50
        sheet1.col(5).width = 256 * 50
        xlwt.add_palette_colour("custom_colour", 0x21)
        new_workbook.set_colour_RGB(0x21, 146, 205, 220)
        xlwt.add_palette_colour("custom_colour1", 0x22)
        new_workbook.set_colour_RGB(0x22, 196, 215, 155)
        xlwt.add_palette_colour("custom_colour2", 0x23)
        new_workbook.set_colour_RGB(0x23, 149, 179, 215)
        style_title = xlwt.easyxf(
            'font:bold on,name Arial;align:wrap on;borders:left thin,right thin,top thin,bottom thin;pattern:pattern solid,fore_colour orange')
        style_item = xlwt.easyxf(
            'font:name Times New Roman;align:wrap on,vert center;borders:left thin,right thin,top thin,bottom thin')
        style_item_for_prioroty = xlwt.easyxf(
            'font:name Arial;align:wrap on,vert center,horz center;borders:left thin,right thin,top thin,bottom thin')
        if (not list):  # list不能为空
            logging.debug("用例列表为空，不能写入excel")
            return False
        for i in range(0, len(self.list_names)):
            name = self.list_names[i] if is_macOS else self.list_names[i].decode('utf-8')
            sheet1.write(0, i, name, style_title)
        k = 0
        for j in range(0, len(list)):
            if is_macOS:
                casetable = list[j].casetable
                casename = list[j].casename
                casenotes = list[j].casenotes
                casestep = list[j].casestep
                caseresult = list[j].caseresult
            else:
                casetable = list[j].casetable.decode('utf-8')
                casename = list[j].casename.decode('utf-8')
                casenotes = list[j].casenotes.decode('utf-8')
                casestep = list[j].casestep.decode('utf-8')
                caseresult = list[j].caseresult.decode('utf-8')
            sheet1.write(k + j + 1, 0, "%s-%s" % (root_topic_title, casetable), style_item)
            # 是否自动化暂时为空
            sheet1.write(k + j + 1, 1, casename, style_item)
            # int不需要去解码；
            sheet1.write(k + j + 1, 2, story_id, style_item_for_prioroty)
            # 备注暂时为空
            sheet1.write(k + j + 1, 3, casenotes, style_item)
            sheet1.write(k + j + 1, 4, casestep, style_item)
            sheet1.write(k + j + 1, 5, caseresult, style_item)
            # 用例类型
            sheet1.write(k + j + 1, 6, "", style_item)
            # 用例状态
            sheet1.write(k + j + 1, 7, "", style_item)
            # 用例等级
            sheet1.write(k + j + 1, 8, list[j].casepriority, style_item)
            # 创建人
            sheet1.write(k + j + 1, 9, username, style_item_for_prioroty)
        if filename == NULL:
            filename = list[0].casedirectory if is_macOS else list[0].casedirectory.decode('utf-8')
        else:
            self.filename = filename
        if path == NULL:
            path = os.getcwd()
        savepath = os.path.join(path, u"%s.xls" % filename)
        print(savepath)
        new_workbook.save(savepath)
        return savepath


if __name__ == '__main__':
    instruct = "\
#########################################################\n\
   Xmind转Tapd工具 By Liquor Email：mryu168@163.com\n\
#########################################################\n\
使用规范如下：\n\
1、xmind文件不超过10级分层\n\
2、根节点为需求或模块名称，末节点为用例名称，中间节点为1-9级目录 \n\
3、末节点必须包含用例优先级标志其中红旗为0级，优先级1-6为用例1-6级）\n\
4、节点上的备注可选填 输入/输出/备注"
    print(instruct)
    try:
        while True:
                if is_macOS:
                    filePath = os.path.abspath(input(r"请将要转换的xmind文件拖至此处:").replace('"', ''))
                    story_id = input("请输入需求ID:")
                    username = input("请输入创建人:")
                    xls_filename = str(filePath.split(os.sep)[-1]).replace(".xmind", "")
                else:
                    # windows
                    filePath = os.path.abspath(input(r"请将要转换的xmind文件拖至此处:".encode("gb18030")).replace('"', ''))
                    filePath = filePath.decode("gb18030")
                    story_id = input("请输入需求ID:".encode("gb18030"))
                    username = input("请输入需求ID:".encode("gb18030"))
                    xls_filename = filePath.split(os.sep)[-1].replace(".xmind", "")
                xls_filepath = os.path.split(filePath)[0]
                if filePath.split('.')[-1] == 'xmind':
                    xmind_file = XmindFileHandle()
                    excel_file = ExeclFileHandle()
                    newpath = get_decode_str(filePath)
                    lists = xmind_file.read_xmind(newpath)
                    if not lists:
                        raise RuntimeError("读取xmind文件失败")
                    else:
                        excel_filepath = excel_file.write_excel_file(lists, path=xls_filepath, filename=xls_filename,
                                                                     story_id=story_id, username=username)
                        xmind_file.log_print(u"转换后excel路径:%s" % excel_filepath)
                else:
                    xmind_file.log_print("输入文件非xmind和xls类型!!")
    except Exception as e:
        if "invalid worksheet name" in str(e):
            print ("xmind根节点带有windows不支持命名excel sheet的字符（如：?\ * | “ < : /）,请修改根节点名称")
        elif  "list index out of range" in str(e):
            print ("!!!!!!关键日志：请检查是否缺少一级节点，一级节点不可缺少！!!!!!!")
        elif "[Errno 13] Permission denied:" in str(e):
            print("手动关闭已转化过的Execl")
        else:
            print(e)