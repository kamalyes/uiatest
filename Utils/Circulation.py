# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : Circulation.py
@Author: v_yanqyu
@Desc  : 修饰创建自行的switch效果
@Date  : 2020/10/21 23:05
'''

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

if __name__ == '__main__':
    v = 'ten'
    for case in switch(v):
        if case('one'):
            print (1)
            break
        if case('two'):
            print (2)
            break
        if case('ten'):
            print(3)
            break
        if case('eleven'):
            print(7)
            break
        if case():  # 默认
            print("something else!")