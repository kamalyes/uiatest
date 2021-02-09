# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： YamlToCase.py
# Author : YuYanQing
# Desc: 解析yaml
# Date： 2021/2/1 0:37
'''

import os,yaml
import BaseSetting
from Utils.OkHttps import OpenServlet

class OperYaml:
	def __init__(self, yamlPath=None,params=None):
		"""
		设置yaml文件路径
		:param yamlPath:
		"""
		self.yamlPath = yamlPath
		self.headers = OpenServlet().set_headers(params)

	def statist_case(self):
		"""
		读取Yaml文件转化为dict
		:return: 
		"""
		with open(self.yamlPath, 'r', encoding='utf-8') as file:
			contents = file.read()
			testCase_dict = yaml.safe_load(contents)
			case_list = []
			for caseName, caseInfo in testCase_dict.items():
				new_dict = {}
				new_dict[caseName] = caseInfo
				case_list.append(new_dict)
			return  case_list

if __name__ == "__main__":
	casePath = os.path.join(BaseSetting.AbsPath, "YamlCase", "Login.yaml")
	print(OperYaml(casePath).statist_case())



