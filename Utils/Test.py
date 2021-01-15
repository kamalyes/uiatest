# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Test.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2021/1/16 13:45
'''
import linecache

with open(r"E:\WorkSpace\PycharmProjects\AutoFramework\Result\20210116-addNote.txt","r",encoding="utf-8") as file:
    line = file.readlines()
    for i in range(len(line)):
        print(linecache.getline(r"E:\WorkSpace\PycharmProjects\AutoFramework\Result\20210116-addNote.txt", i).strip())