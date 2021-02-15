# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : setup.py
@Author: YuYanQing
@Desc  : 
@Date  : 2020/10/1 10:39
'''

import re
import sys, os
from setuptools import setup, find_packages
version = '1.0.0'

if not version:
    raise RuntimeError('Cannot find version information')

with open('readme.md', 'rb') as f:
    readme = f.read().decode('utf-8')

install_requires = []
with open('requirements.txt') as f:
    for req in f :
        req = str(req).strip()
        if not req.startswith('git+') :
            install_requires.append(req)
        else :
            os.system('pip install -U %s' % req)

setup(
    name='AutoFramework',
    version=version,
    description="自动化框架",
    long_description=readme,
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    author='mryu168@163.com',
    url='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
)
