# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ExcelTools.py
# Author : v_yanqyu
# Desc: Excel工具类
# Date： 2020/10/9 11:18
'''

import os, xlrd
import shutil
from datetime import datetime
from xlrd import xldate_as_tuple
from Logger.GlobalLog import Logger
logger = Logger.write_log()
class ExcelHandle:
    @classmethod
    def open_excel(self, filepath):
        """
        :param filepath 文件路径
        :return: workbook 工作区
        """
        try:
            with xlrd.open_workbook(filepath) as workbook:
                return workbook
        except Exception as e:
            logger.error(e)

    @classmethod
    def list_excel(self, workbook):
        """
        读取全部的excel数据/合并单元格不支持
        :param workbook: open_excel传入的值、不可以缺少
        :param name_sheets 获取到所有的sheet列表
        :param sheet  for得到具体遍历的单个sheet
        :return:
        """
        name_sheets = workbook.sheet_names()
        logger.info("检索到所有的工作节点有%s个、依次为：%s" % (len(name_sheets), name_sheets))
        for index in range(0, len(name_sheets)):
            sheet = workbook.sheet_by_name(name_sheets[index])
            rows = sheet.nrows
            cols = sheet.ncols
            content = []
            for i in range(rows):
                row_content = []
                for j in range(cols):
                    ctype = sheet.cell(i, j).ctype  # 表格的数据类型
                    cell = sheet.cell_value(i, j)
                    if ctype == 2 and cell % 1 == 0:  # 如果是整形
                        cell = int(cell)
                    elif ctype == 3:
                        # 转成datetime对象
                        date = datetime(*xldate_as_tuple(cell, 0))
                        cell = date.strftime('%Y/%d/%m %H:%M:%S')
                    elif ctype == 4:
                        cell = True if cell == 1 else False
                    row_content.append(cell)
                content.append(row_content)
                # logger.debug('[' + ','.join("'" + str(element) + "'" for element in row_content) + ']')
            return content

    @classmethod
    def once_read(self, workbook):
        """
        一次性读取excel的全部内容/可识别合并单元格
        :param workbook: open_excel传入的值、不可以缺少
        :param name_sheets 获取到所有的sheet列表
        :param sheet_info  for得到具体遍历的单个sheet
        :param first_line  过滤出首行数据
        :param other_line  主干内容的数据
        :param merge_cells 检索出对应合并的单元格的key合value值、例如：[(1, 3, 1, 2)]
        :param value_mg_cell 则输出对应的内容
        :param merge 具体合并坐标及合并内容
        :return: all_content 结果集
        """
        content = []
        merge = {}
        name_sheets = workbook.sheet_names()
        logger.info("检索到所有的工作节点有%s个、依次为：%s" % (len(name_sheets), name_sheets))
        for index in range(0, len(name_sheets)):
            sheet_info = workbook.sheet_by_name(name_sheets[index])
            first_line = sheet_info.row_values(0)
            merge_cells = sheet_info.merged_cells
            for (rlow, rhigh, clow, chigh) in merge_cells:
                value_mg_cell = sheet_info.cell_value(rlow, clow)
                # logger.debug(value_mg_cell)
                if rhigh - rlow == 1:
                    for n in range(chigh - clow - 1):
                        merge[(rlow, clow + n + 1)] = value_mg_cell
                elif chigh - clow == 1:
                    for n in range(rhigh - rlow - 1):
                        merge[(rlow + n + 1, clow)] = value_mg_cell
            logger.info("检索到%s工作录下所有的合并单元格坐标及内容：%s" % (name_sheets[index], merge))
            for i in range(1, sheet_info.nrows):  # 开始为组成字典准备数据
                other_line = sheet_info.row_values(i)
                for key in merge.keys():
                    if key[0] == i:
                        other_line[key[1]] = merge[key]
                dic = dict(map(lambda x, y: [x, y], first_line, other_line))
                content.append(dic)
        return content

    @classmethod
    def term_read(self, workbook):
        """
        查询出指定行列的数据
        :param workbook: open_excel传入的值、不可以缺少
        :return:
        """

    @classmethod
    def sheet_name(self, workbook):
        """
        获取sheet内容
        :param workspace:
        :return:
        """
        sheet_name = workbook.sheet_names()[0]
        return sheet_name

    @classmethod
    def designat_unit(self, workbook,row,clow):
        """
        获取指定单元格的内容
        :param workspace:
        :return:
        """
        designat = workbook.cell_value(row, clow)
        return designat

    @classmethod
    def copy_excel(self, filepath, target=None):
        """
        备份Excel
        :param filepath:
        :param target:
        :return:
        """
        try:
            if filepath is not None:
                if target is None:
                    head, tail = os.path.split(filepath)
                    target = r"%s\%s.bak" % (head, tail)
                    logger.warning("已成功备份至：%s" % (target))
                    shutil.copy(filepath, target)
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

    @classmethod
    def cell_process(self, filepath):
        """
        呼叫线程组、统一管理读取、删除、写入(该方法暂未实现有时间在看看2020-10-21)
        :return:
        """
        wookbook = ExcelHandle.open_excel(filepath)
        once_read = ExcelHandle.once_read(workbook=wookbook)
        list_excel = ExcelHandle.list_excel(workbook=wookbook)

        if wookbook is not None:
            return wookbook
        if once_read is not None:
            return once_read
        if list_excel is not None:
            return list_excel

if __name__ == '__main__':
    wookbook = ExcelHandle.open_excel(filepath=r'..\Config\district.xls')
    logger.info(wookbook)
    once_read = ExcelHandle.once_read(workbook=wookbook)
    list_excel = ExcelHandle.list_excel(workbook=wookbook)
    cell = ExcelHandle.cell_process(filepath=r'..\Config\Interface.xlsx')
    logger.info(once_read)
    ExcelHandle.copy_excel(filepath=r"E:\WorkSpace\PycharmProjects\AutoFramework\Config\Interface.xlsx")