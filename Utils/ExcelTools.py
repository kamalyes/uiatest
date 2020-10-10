# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ExcelTools.py
# Author : v_yanqyu
# Desc: Excel工具类
# Date： 2020/10/9 11:18
'''
import xlrd
workbook = None

def open_excel(path):
     """
     打开excel
     :param path: 打开excel文件的位置
     """
     global workbook
     if (workbook == None):
        workbook = xlrd.open_workbook(path, on_demand=True)

def get_sheet(sheetName):
     """
     获取页名
     :param sheetName: 页名
     :return: workbook
     """
     global workbook
     return workbook.sheet_by_name(sheetName)

def get_rows(sheet):
    """
    获取行号
    :param sheet: sheet
    :return: 行数
    """
    return sheet.nrows

def get_content(sheet, row, col):
    """
    获取表格中内容
    :param sheet: sheet
    :param row: 行
    :param col: 列
    :return:
    """
    return sheet.cell(row, col).value

def release(path):
    """释放excel减少内存"""
    global workbook
    workbook.release_resources()
    del workbook
    # todo:没有验证是否可用