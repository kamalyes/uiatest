# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : RandomText.py
@Author: v_yanqyu
@Desc  : 随机文本(id/姓名/邮箱/身份证)
@Date  : 2020/10/1 15:01
'''
import re,random,string
from Logger import GlobalLog
logger = GlobalLog.Logger().write_log()#调用日志模块
class RandomNum():
    def email(self,emailtype=None,maxnum=None,rad_count=None):
        """
        :param emailtype: 邮箱类型
        :param count:     所生成的数量
        :param maxnum:    邮箱地址最大长度
        :param temp       临时存储生成的字符  temp_str转化list为str
        :return: email_list 最终输出的邮箱集合
        """
        temp = []
        count = 0
        email_list = []
        email_array = ['@126.com', '@163.com', '@sina.com', '@sohu.com', '@yahoo.com.cn', '@gmail.com', '@yahoo.com']
        if emailtype == None:
            emailtype = random.choice(email_array)
        if maxnum == None:
            maxnum = random.randint(6, 10)
        if rad_count == None:
            rad_count = 1
        while count<rad_count:
            for i in range(0, maxnum):
                status = random.randint(0, 1)
                if status == 0:
                    letters = string.ascii_letters
                    random_letter = random.choice(letters)
                    temp.append(random_letter)
                else:
                    random_num = random.randint(0, 1)
                    temp.append(str(random_num))
            temp_str = "".join(temp)
            # 每次转化后就丢弃temp、避免出现遍历追加['VJT000Ho@qq.com', 'VJT000Ho0110fm0w@qq.com'............]
            temp.clear()
            email_list.append(temp_str + emailtype)
            count +=1
        # logger.info("已成功生成%s个，%s个前缀，且类型为%s邮箱地址"%(count,maxnum,emailtype))
        return email_list

    def verifi(self,maxnum,radcount):
        """
        随机生成6位的验证码
        :param maxnum:  最多可生成的长度
        :param radcount: 需要生成的数量
        :return: verifi_code 输出结果集
        """
        # 注意： 这里我们生成的是0-9A-Za-z的列表，当然你也可以指定这个list，这里很灵活
        # 比如： code_list = ['P','y','t','h','o','n','T','a','b'] # PythonTab的字母
        count = 0
        verifi_code = []
        while count < radcount:
            code_list = []
            for i in range(10):  # 0-9数字
                code_list.append(str(i))
            for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
                code_list.append(chr(i))
            for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
                code_list.append(chr(i))
            myslice = random.sample(code_list, maxnum)  # 从list中随机获取6个元素，作为一个片断返回
            verifi_code.append(''.join(myslice))  # list to string
            count += 1

        return verifi_code

    def phone(self,radcount):
        """
        随机生成有效手机号码
        :param radcount: 需要生成的数量
        :return:
        """
        count = 0
        phone_num =[]
        while count < radcount:
            prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                        "153", "155", "156", "157", "158", "159", "186", "187", "188"]
            cell =random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
            phone_num.append(''.join(cell))  # list to string
            count +=1
        return phone_num

if __name__ == '__main__':
    print(RandomNum().email(emailtype = "@qq.com",maxnum=10,rad_count=10))
    print(RandomNum().verifi(maxnum=5,radcount=2))
    print(RandomNum().phone(radcount=2))
