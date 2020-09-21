#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： MysqlManager.py
# Author : v_yanqyu
# !@Desc:  获取指定目录下所有的文件名并返回一个列表，剔除其中的__init__.py和__pycache__。
# Date： 2020/9/15 12:25
'''
import os
def get_dirlist(filePath):
    '''
    获取指定目录下所有的文件名并返回一个列表
    :param filePath:
    :return:
    '''
    current_files = os.listdir(filePath)
    all_files = []
    for file_name in current_files:
        full_file_name = os.path.join(filePath, file_name)
        all_files.append(full_file_name)
        if os.path.isdir(full_file_name):
            next_level_files = get_dirlist(full_file_name)
            all_files.extend(next_level_files)
    return all_files


if __name__ == '__main__':
    print(get_dirlist(filePath="../Result"))