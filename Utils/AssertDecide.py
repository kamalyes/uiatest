# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AssertDecide.py
# Author : MrYu
# Desc: 效验判断
# Date： 2021/2/15 12:15
'''

def is_not_null(content):
    """
    非空字符串
    :param content: 字符串
    :return: 非空 - True，空 - False
    """
    if content and content.strip():
        return True
    else:
        return False
