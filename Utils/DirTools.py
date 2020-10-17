# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： DirTools.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/5/6 19:15
'''

import os
import zipfile,gzip,shutil
from Logger.GlobalLog import Logger
logger = Logger.write_log()#调用日志模块
class Doc_Process(object):
    @classmethod
    def get_pwd(self):
        """
        获取当前文件路径
        :return: pwd
        """
        pwd = os.path.abspath(os.path.dirname(__file__))
        return pwd

    @classmethod
    def get_superior_dir(self):
        """
        获取上级目录
        :return:  superior_directory
        """
        superior_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        return superior_directory

    @classmethod
    def get_superior_dirs(self):
        """
        获取上上级目录
        :return: superior_directorys
        """
        superior_directorys = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        return superior_directorys

    @classmethod
    def get_dirlist(self,filePath):
        '''
        获取指定目录下所有的文件名并返回一个列表，剔除其中的__init__.py和__pycache__。
        :param filePath:
        :return:
        '''
        current_files = os.listdir(filePath)
        all_files = []
        for file_name in current_files:
            full_file_name = os.path.join(filePath, file_name)
            all_files.append(full_file_name)
            if os.path.isdir(full_file_name):
                next_level_files = self.get_dirlist(full_file_name)
                all_files.extend(next_level_files)
        return all_files

    @classmethod
    def creat_zip(self,method,filepath,target_path=""):
        """
        打包文件为压缩包
        :param filepath  被打包的文件路径
        :param target_path 目标存储的文件路径
        :param method    用于判断是打包单个文件还是遍历文件夹下所有的文件 singfile: 单个、 allfile： 全部
        :param zip_file 声明打包对象、mode改为‘w’
        :param ziplist   多级目录绝对路径
        :return:
        """
        ziplist = []
        zip_file = zipfile.ZipFile(target_path, "w")
        try:
            if not os.path.exists(filepath):
                logger.error('请检查filepath是否正确！')
            else:
                if method == "singfile":
                        zip_file.write(filepath)
                if method == "allfile":
                    hasPDir = not filepath.endswith(os.sep);
                    logger.info(hasPDir)
                    if not hasPDir:
                        filepath = os.path.dirname(filepath);
                        logger.error(filepath)
                    target_path = os.path.dirname(filepath) + os.sep + target_path;
                    logger.info("压缩存储后的路径：" + target_path)
                    if not os.path.exists(os.path.dirname(target_path)):
                        os.makedirs(os.path.dirname(target_path));
                    # 多级目录读取
                    for dirpath, dirnames, filenames in os.walk(filepath):
                        for filename in filenames:
                            ziplist.append(os.path.join(dirpath, filename))
                    for tar in ziplist:
                        zip_file.write(tar)
        except Exception as IOError:
            logger.error(IOError)
        finally:
            zip_file.close()

    @classmethod
    def un_zip(self,method,filepath,target_path=""):
        """
        解压多种类型的压缩包
        :param method: 类型判断
        :param filepath: 需要解压的文件绝对路径
        :param zip_list: 获取压缩包内所有的文件
        :return:
        """
        try:
            zip_file = zipfile.ZipFile(filepath)
            if method == "gzip":
                zip_file.extractall(path=target_path)

            if method == "zip":
                zip_list = zip_file.namelist()
                for f in zip_list:
                    zip_file.extract(f, target_path)
            else:
                pass
        except Exception as IOError:
            logger.error(IOError)

        finally:
            zip_file.close()

    @classmethod
    def get_filetype(self,file_path):
        """
        判断传入的文件状态
        :param file_path:  检查的文件路径
        备注：实际用os自带的即可
        """
        try:
            head, tail = os.path.split(file_path)
            if os.access(file_path, os.F_OK):
                logger.info("%s：文件存在"%(file_path))
                if os.access(file_path, os.R_OK):
                    logger.info("%s：文件可读"%(file_path))
                else:
                    logger.error("%s：文件不支持可读"%(file_path))

                if os.access(file_path, os.W_OK):
                    logger.info("%s：文件可写"%(file_path))
                else:
                    logger.error("%s：文件不支持可写" % (file_path))

                if os.access(file_path, os.X_OK):
                    logger.info("%s：文件可执行"%(file_path))
                else:
                    logger.error("%s：文件不支持可执行" % (file_path))

                if (os.path.isdir(file_path)):
                    logger.info("%s：这是一个文件夹"%(file_path))
                else:
                    logger.info("%s：这是一个文件" %(file_path))
            else:
                logger.error("%s：文件不存在" % (file_path))
        except Exception as IOError:
            logger.error(IOError)

    @classmethod
    def copy_file(self,filepath, target):
        """
        复制文件
        :param method:
        :param filepath:
        :param target:
        :return:
       """
        file_list =[]
        if os.path.exists(filepath):
            if not os.path.exists(target):
                os.makedirs(target)
            # 多级目录读取
            for dirpath, dirnames, filenames in os.walk(filepath):
                for filename in filenames:
                    file_list.append(os.path.join(dirpath, filename))
            for list in file_list:
                shutil.copy(list,target)
        else:
            logger.error('请检查filepath是否正确！')

    @classmethod
    def remove_file(self,filepath):
        """
        删除文件或文件夹
        :param filepath:
        :return:
        """
        try:
            if os.path.exists(filepath):
                for root, dirs, files in os.walk(filepath, topdown=False):
                    # 先删除文件
                    for name in files:
                        os.remove(os.path.join(root, name))
                    # 再删除空目录
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                        # 再删除自己
                        os.rmdir(filepath)
            else:
                logger.error('请检查filepath是否正确！')
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

    @classmethod
    def make_file(self,filepath):
        """
        创建多级文件夹(注意这里必须上级文件夹存在才可以)
        :param filepath:
        :return:
        """
        try:
            if not os.path.exists(filepath):
                os.makedirs(filepath)
                if os.path.exists(filepath):
                    logger.info("目录：%s 创建成功！！！" % (filepath))
            else:
                logger.error("%s已存在，跳过创建！" % (filepath))
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

if __name__ == '__main__':
    logger.info(Doc_Process.get_pwd())
    logger.info(Doc_Process.get_superior_dir())
    logger.info(Doc_Process.get_superior_dirs())
    # Doc_Process.creat_zip(method="allfile",filepath=r"D:\Work_Spaces\PyCharm_Project\UiAutomationFramework\Utils",target_path="aaaa.gzip")
    # Doc_Process.get_filetype(file_path=r"E:\WorkSpace\PycharmProjects\UiAutomationFramework\Utils\not_exist.py")
    # Doc_Process.copy_file(filepath=r"D:\Work_Spaces\PyCharm_Project\UiAutomationFramework\Utils",target=r"D:\Work_Spaces\PyCharm_Project\UiAutomationFramework\Utils\COPYS")
    # Doc_Process.remove_file(filepath=r"..\Result\Logs\2020-09-21\Default_Logs\2020-09-21.log")
    # Doc_Process.make_file(filepath=r"D:\Work_Spaces\PyCharm_Project\UiAutomationFramework\Utils\AA\aaa")
    # Doc_Process.get_dirlist(filePath=r"D:\Work_Spaces\PyCharm_Project\UiAutomationFramework\Utils")