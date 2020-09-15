#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： Adb_Tools.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/9/6 18:41
'''
__author__ = 'v_yanqyu'
import os,re,time,datetime
import configparser,subprocess
from Logger import GlobalLog
from ATestClass import ImportJar
from Until import GetAbspath
logger = GlobalLog.Logger.write_log()
ImportJar.check_import()
conf_ini = "../Config/Logger.ini"
conf = configparser.ConfigParser()
conf.read(conf_ini)
package_name = conf.get("Apk_Info", "package_name")
class Adb_Tools(object):
    def __init__(self):
        self.check_devices_status()

    def check_local_file(self):
        """
        检查本地文件是否存在
        :param superiordirectory:上级目录
        :param GeneralFile:拼接后的APK包存储目录
        :return apk_filepath：拼接后的安卓包完整目录
        """
        apklist = []
        superiordirectory = GetAbspath.get_superiordirectory()
        logger.info("上级所在目录为：{}".format(superiordirectory))
        GeneralFile = superiordirectory + "\APKPath"
        logger.info("APK存储路径：{}".format(GeneralFile))
        try:
            for File_Path in os.listdir(GeneralFile):
                apklist.append(File_Path)
                logger.info("检索到APK_Name：{}".format(File_Path))
                apk_filepath = GeneralFile + "\\" + File_Path
                return apk_filepath
        except Exception as TypeError:
            logger.error(TypeError)

    def check_adb_path(self):
        """
        检查adb 判断是否设置环境变量ANDROID_HOME
        :return:
        """
        adb_info = os.popen("adb version").read()  # window下使用findstr
        error_message = "'adb'不是内部或外部命令，也不是可运行的程序或批处理文件。"
        if adb_info in error_message:
            return False
        else:
            logger.info("\n%s"%(adb_info))
            return True

    def check_devices_status(self):
        """
        检查设备是否连接成功，如果成功返回Device_Nmae，否则返回False
        :param all_info：CMD输入
        :return devices_name：设备ID
        """
        try:
            adb_info = self.check_adb_path()
            if adb_info == True:
                logger.info("----------Start Connect Device--------------")
                str_init = ' '
                all_info = os.popen('adb devices').readlines()
                for i in range(len(all_info)):
                    str_init += all_info[i]
                devices_name = re.findall('\n(.+?)\t', str_init, re.S)
                if devices_name != []:
                    logger.info("设备连接成功%s" % (devices_name))
                    return devices_name
                else:
                    logger.error("请检查目标设备是否与主机连接成功！！！")
                    return False
            else:
                logger.error("本地没有配置Android_SDK环境！！！")
        except Exception as TypeError:
            logger.error("Device Connect Fail:", TypeError)

    def install_apk(self,apk_filepath, devices_name):
        """
        检查本地文件是否存在
        :param devices_name:设备号
        :param apk_filepath：拼接后的安卓包完整目录
        """
        try:
            logger.info("成功接收到check_local_file方法return的安装包绝对路径：{}".format(apk_filepath))
            logger.info("----------Start Install APK--------------")
            if devices_name == False:
                pass
            else:
                # 循环遍历出所有已连接的终端设备,便于后期调用
                logger.info('检索到的设备：{}'.format(devices_name))
                for dev_name in devices_name:
                    logger.info("当前被安装终端ID：%s，安装过程中请勿移除USB连接！！！" % (dev_name))
                    result = os.popen('adb -s %s install -r %s' % (dev_name, apk_filepath))
                    res = result.read()
                    for line in res.splitlines():
                        if line == "Success":
                            logger.info("设备：%s安装成功" % (dev_name))
                        else:
                            logger.error("设备：%s安装失败！！！" % (dev_name))
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def uninstall_apk(self,devices_name):
        """
        卸载apk
        :param devices_name:设备号
        :param package_name:包名
        """
        try:
            if devices_name == False:
                pass
            else:
                logger.info("------- Uninstall Apking ------")
                for dev_name in devices_name:
                    logger.info("当前被安装终端ID：%s，卸载过程中请勿移除USB连接！！！" % (dev_name))
                    result = os.popen('adb -s %s uninstall  %s' % (dev_name, package_name))
                    res = result.read()
                    for line in res.splitlines():
                        if line == "Success":
                            logger.info("设备：%s卸载成功" % (dev_name))
                        else:
                            logger.error("设备：%s卸载失败！！！" % (dev_name))
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def clear_package(self,devices_name):
        """
        清理apk缓存
        :param devices_name:设备号
        :param package_name:包名
        """
        try:
            if devices_name == False:
                pass
            else:
                logger.info("------- Clear Package ------")
                for dev_name in devices_name:
                    logger.info("当前被安装终端ID：%s，卸载过程中请勿移除USB连接！！！" % (dev_name))
                    result = os.popen('adb shell pm clear  %s' % (package_name))
                    res = result.read()
                    for line in res.splitlines():
                        if line == "Success":
                            logger.info("设备：%s清除数据成功" % (dev_name))
                        elif line == "Failed":
                            logger.error("设备：%s清除数据失败！！！" % (dev_name))
                        else:
                            logger.error("未知错误")
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def get_ipconfig(self,devices_name):
        """
        获取已连接的手机IP
        :param ipconfig：wlan0基本Ip信息
        :return ip
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    ipconfig = os.popen("adb shell ifconfig wlan0").read().replace(" ", "")  # window下使用findstr
                    if not ipconfig.strip():
                        logger.error("获取设备IP失败！！！%s" % (ipconfig))
                    else:
                        ipv4 = re.sub("[A-Za-z]", "", str(ipconfig[31:45]))
                        logger.info("检索到设备%s当前IP：%s" % (dev_name, ipv4))
                        return ipv4
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def remote_connectdev(self,devices_name, ipv4):
        """
        远程连接手机
        :param check_ip：检查网络是否通
        :return devices_name：设备ID
        """
        try:
            if ipv4 == False:
                pass
            else:
                for dev_name in devices_name:
                    check_ip = os.popen("ping {}".format(ipv4)).read()
                    restart_adb = os.popen("adb tcpip 5555").read()
                    str = "Ping 请求找不到主机 None。请检查该名称，然后重试。"
                    if str == check_ip or restart_adb == "":
                        logger.error("adb tcpip模式重启adb失败%s" % (check_ip))
                    else:
                        logger.info("adb tcpip模式重启adb成功！！！")
                        connect = os.popen("adb connect {}".format(ipv4)).read()
                        logger.info(connect)
                    return check_ip
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def get_current_package(self,devices_name):
        '''
        获取当前运行
        :param devices_name: 设备号
        :return: pwd_activity：package/activity
        '''
        try:
            for dev_name in devices_name:
                activity = os.popen(
                    "adb shell dumpsys window windows | grep -E 'mCurrentFocus'").read()  # window下使用findstr
                pwd_activity = activity.replace(" ", "")
                logger.info("检索到设备%s当前Activity：%s" % (dev_name, pwd_activity))
                return pwd_activity
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def get_battery_info(self,devices_name):
        '''
        获取Android手机电池电量
          status: 1            #电池状态：2：充电状态 ，其他数字为非充电状态
          health: 2            #电池健康状态：只有数字2表示good
          present: true        #电池是否安装在机身
          level: 55            #电量: 百分比
          scale: 100
          voltage: 3977         #电池电压
          current now: -335232  #电流值，负数表示正在充电
          temperature: 335      #电池温度，单位是0.1摄氏度
          technology: Li-poly    #电池种类=
        '''
        try:
            for dev_name in devices_name:
                battery = os.popen("adb shell dumpsys battery").read().split("\n")  # window下使用findstr
                batterystatus = battery[7]
                batterylevel = battery[10]
                logger.info("成功获取到{}设备电池信息：{},{}".format(dev_name, batterystatus, batterylevel))
                return battery, batterystatus, batterylevel
        except Exception as  ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def create_file(self,devices_name, method, path=""):
        """
        创建目录
        :param  split_path：清理文件尾椎
        :param  mkdir_msg：运行后返回的结果集 1代表False、0代表True
        :param  method: 调用的方法元素、mkdir：创建文件、 touch：创建文件夹
        :param  make_dir：创建文件夹、且会携带返回结果集
        :param  touch_file: 创建文件
        :param  devices_name：设备号
        """
        try:
            if devices_name == False:
                pass
            else:
                if method == "mkdir":
                    # 清理文件尾椎例如：/sdcard/maketest/aaa.text 自动过滤掉为/sdcard/maketest/aaa
                    split_path = os.path.splitext(path)[0]
                    logger.info("------- Make Directory------")
                    make_dir = subprocess.getstatusoutput('adb shell "mkdir %s"' % (split_path))
                    if make_dir[0] == 1:
                        logger.error("%s" % (make_dir[1]))
                    else:
                        logger.info("%s Mkdir 成功" % (make_dir))
                        return split_path

                elif method == "touch":
                    logger.info("------- Touch File------")
                    for dev_name in devices_name:
                        touch_file = subprocess.getstatusoutput('adb shell "touch %s"' % (path))
                        if touch_file[0] == 1:
                            logger.info("%s" % (touch_file[1]))
                        elif touch_file[0] == 0:
                            logger.error("%s Touch 成功" % (path))
                            return touch_file
                        else:
                            logger.error("未知错误")
                    else:
                        pass
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def file_transfer(self,devices_name, method, source, target=""):
        """
        文件基本操作
        :param pull 从手机端拉取文件到电脑端
        :param push 从电脑端复制文件至手机端
        :param remove：强制删除文件
        :param subprocess方法检查返回结果集 1为假 0为真 反人类
        """
        try:
            if devices_name == False:
                pass
            else:
                if method == "pull" or method == "Pull":
                    pull = subprocess.getstatusoutput('adb pull %s %s"' % (source, target))
                    logger.debug(pull)
                    if pull[0] == 0:
                        logger.info("Pull：%s文件到 %s成功." % (source, target))
                        return pull
                    else:
                        logger.error("Pull文件失败，%s" % (pull[1].replace(": ", "_")))

                elif method == "push" or method == "Push":
                    push = subprocess.getstatusoutput('adb push %s %s"' % (source, target))
                    if push[0] == 0:
                        logger.info("Push：%s文件到 %s" % (source, target))
                        return push
                    else:
                        logger.error("Push文件失败，%s" % (push[1].replace(": ", "_")))

                elif method == "remove" or method == "Remove":
                    remove = subprocess.getstatusoutput('adb shell "rm -rf %s" ' % (source))
                    if remove[0]:
                        logger.info("删除%s文件成功" % (source))
                        return remove
                    else:
                        logger.error("删除文件失败！！！")
                else:
                    logger.error("未知错误！！！")
        except Exception as TypeError:
            logger.error(TypeError)

    def get_process(self,devices_name, keyword):
        """
        获取进程信息
        :param devices_name: 设备ID
        :param process: 进程info
        :return: process_id
        """
        try:
            if devices_name == False:
                pass
            else:
                process = subprocess.getstatusoutput("adb shell ps |grep '%s'" % (keyword))
                process_status = process[0]
                process_info = process[1]
                if process_status == 0:
                    logger.info("\n%s" % (process_info))
                    return process
                else:
                    logger.error("暂未获取到%s的进程信息" % (keyword))
                    return False
        except Exception as TypeError:
            logger.error(TypeError)

    def get_screenshot(self,devices_name, source):
        """
        手机截图
        :param nowtime 当前本地格式化的毫秒级时间
        :param target: 目标路径
        :param screen_info 返回的信息，格式：['1','Error opening file: path (Read-only file system)']
        :param screen_status 截图时的状态
        :return:
        """
        try:
            nowtime = datetime.datetime.now().strftime('%Y-%m%d-%H-%M-%S-%f')
            logger.info(nowtime)
            path = "/%s/%s.png" % (source, nowtime)
            screen_info = subprocess.getstatusoutput("adb shell screencap -p %s" % (path))
            screen_status = screen_info[0]
            if screen_status == 0:
                logger.info("截图成功%s" % (path))
                return path
            else:
                logger.error("%s" % (screen_info[1]))
                return False
        except Exception as TypeError:
            logger.error(TypeError)

    def file_exists(self,devices_name,target):
        """
        判断文件在目标路径是否存在
        :param devices_name:设备号
        :param target：目标文件路径
        :return:
        """
        try:
            if devices_name ==False:
                pass
            else:
                for dev_name in devices_name:
                    file_info = subprocess.getstatusoutput("adb -s %s shell ls %s" % (dev_name, target))
                    if file_info[0] == 1:
                        logger.error("%s文件不存在！！！"%(target))
                        return  False
                    else:
                        logger.info("%s文件存在！！！"%(target))
                        return True
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def is_install(self,devices_name, package_name):
        """
        判断目标app在设备上是否已安装
        :param target_app: 目标app包名
        :return: bool
        """
        try:
            if devices_name ==False:
                pass
            else:
                for dev_name in devices_name:
                    file_info = subprocess.getstatusoutput("adb -s %s shell pm list packages %s" % (dev_name, package_name))
                    # logger.info(file_info)
                    if file_info[0] == 1:
                        logger.error("本地未安装：package_name：%s"%(package_name))
                        return  False
                    else:
                        logger.info("本地已安装：package_name：%s"%(package_name))
                        return  True
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    def get_display_state(self,devices_name):
        """
        获取屏幕状态
        :return: 亮屏/灭屏
        """
        try:
            if devices_name ==False:
                pass
            else:
                for dev_name in devices_name:
                    file_info = subprocess.getstatusoutput("adb -s %s shell dumpsys power" %(dev_name))[1].replace("\n","")
                    print(file_info.strip())
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)


    def get_screen_normal_size(self):
        """
        获取设备屏幕分辨率 >> 标配
        :return:
        """
        return self.shell('wm size').read().strip().split()[-1].split('x')

    def get_screen_reality_size(self):
        """
        获取设备屏幕分辨率 >> 实际分辨率
        :return:
        """
        x = 0
        y = 0
        l = self.shell(r'getevent -p | %s -e "0"' % self.__find).readlines()
        for n in l:
            if len(n.split()) > 0:
                if n.split()[0] == '0035':
                    x = int(n.split()[7].split(',')[0])
                elif n.split()[0] == '0036':
                    y = int(n.split()[7].split(',')[0])
        return x, y

    def get_device_interior_sdcard(self):
        """
        获取内部SD卡空间
        :return: (path,total,used,free,block)
        """
        return self.shell('df | %s \/mnt\/shell\/emulated' % self.__find).read().strip().split()

    def get_device_external_sdcard(self):
        """
        获取外部SD卡空间
        :return: (path,total,used,free,block)
        """
        return self.shell('df | %s \/storage' % self.__find).read().strip().split()

    def kill_process(self, pid):
        """
        杀死进程
        pass: 一般需要权限不推荐使用
        :return:
        """
        return self.shell('kill %s' % pid).read().strip()

    def quit_app(self, package):
        """
        退出应用
        :return:
        """
        return self.shell('am force-stop %s' % package).read().strip()

    def recovery(self):
        """
        重启设备并进入recovery模式
        :return:
        """
        self.adb('reboot recovery')

    def fastboot(self):
        """
        重启设备并进入fastboot模式
        :return:
        """
        self.adb('reboot bootloader')

    def get_wifi_state(self):
        """
        获取WiFi连接状态
        :return:
        """
        return 'enabled' in self.shell('dumpsys wifi | %s ^Wi-Fi' % self.__find).read().strip()

    def get_data_state(self):
        """
        获取移动网络连接状态
        :return:
        """
        return '2' in self.shell(
            'dumpsys telephony.registry | %s mDataConnectionState' % self.__find).read().strip()

    def get_network_state(self):
        """
        设备是否连上互联网
        :return:
        """
        return 'unknown host' not in self.shell('ping -w 1 www.baidu.com').read().strip()

    def call(self, number):
        """
        拨打电话
        :param number:
        :return:
        """
        self.shell('am start -a android.intent.action.CALL -d tel:%s' % number)

    def open_url(self, url):
        """
        打开网页
        :return:
        """
        self.shell('am start -a android.intent.action.VIEW -d %s' % url)

    def start_application(self, component):
        """
        启动一个应用
        e.g: com.android.settings/com.android.settings.Settings
        """
        self.shell("am start -n %s" % component)

    def send_keyevent(self, keycode):
        """
        发送一个按键事件
        https://developer.android.com/reference/android/view/KeyEvent.html
        :return:
        """
        self.shell('input keyevent %s' % keycode)

    def rotation_screen(self, param):
        """
        旋转屏幕
        :param param: 0 >> 纵向，禁止自动旋转; 1 >> 自动旋转
        :return:
        """
        self.shell('/system/bin/content insert --uri content://settings/system --bind '
                   'name:s:accelerometer_rotation --bind value:i:%s' % param)

    class KeyCode:
        KEYCODE_CALL = 5  # 拨号键
        KEYCODE_ENDCALL = 6  # 挂机键
        KEYCODE_HOME = 3  # Home键
        KEYCODE_MENU = 82  # 菜单键
        KEYCODE_BACK = 4  # 返回键
        KEYCODE_SEARCH = 84  # 搜索键
        KEYCODE_CAMERA = 27  # 拍照键
        KEYCODE_FOCUS = 80  # 对焦键
        KEYCODE_POWER = 26  # 电源键
        KEYCODE_NOTIFICATION = 83  # 通知键
        KEYCODE_MUTE = 91  # 话筒静音键
        KEYCODE_VOLUME_MUTE = 164  # 扬声器静音键
        KEYCODE_VOLUME_UP = 24  # 音量+键
        KEYCODE_VOLUME_DOWN = 25  # 音量-键
        KEYCODE_ENTER = 66  # 回车键
        KEYCODE_ESCAPE = 111  # ESC键
        KEYCODE_DPAD_CENTER = 23  # 导航键 >> 确定键
        KEYCODE_DPAD_UP = 19  # 导航键 >> 向上
        KEYCODE_DPAD_DOWN = 20  # 导航键 >> 向下
        KEYCODE_DPAD_LEFT = 21  # 导航键 >> 向左
        KEYCODE_DPAD_RIGHT = 22  # 导航键 >> 向右
        KEYCODE_MOVE_HOME = 122  # 光标移动到开始键
        KEYCODE_MOVE_END = 123  # 光标移动到末尾键
        KEYCODE_PAGE_UP = 92  # 向上翻页键
        KEYCODE_PAGE_DOWN = 93  # 向下翻页键
        KEYCODE_DEL = 67  # 退格键
        KEYCODE_FORWARD_DEL = 112  # 删除键
        KEYCODE_INSERT = 124  # 插入键
        KEYCODE_TAB = 61  # Tab键
        KEYCODE_NUM_LOCK = 143  # 小键盘锁
        KEYCODE_CAPS_LOCK = 115  # 大写锁定键
        KEYCODE_BREAK = 121  # Break / Pause键
        KEYCODE_SCROLL_LOCK = 116  # 滚动锁定键
        KEYCODE_ZOOM_IN = 168  # 放大键
        KEYCODE_ZOOM_OUT = 169  # 缩小键
        KEYCODE_0 = 7
        KEYCODE_1 = 8
        KEYCODE_2 = 9
        KEYCODE_3 = 10
        KEYCODE_4 = 11
        KEYCODE_5 = 12
        KEYCODE_6 = 13
        KEYCODE_7 = 14
        KEYCODE_8 = 15
        KEYCODE_9 = 16
        KEYCODE_A = 29
        KEYCODE_B = 30
        KEYCODE_C = 31
        KEYCODE_D = 32
        KEYCODE_E = 33
        KEYCODE_F = 34
        KEYCODE_G = 35
        KEYCODE_H = 36
        KEYCODE_I = 37
        KEYCODE_J = 38
        KEYCODE_K = 39
        KEYCODE_L = 40
        KEYCODE_M = 41
        KEYCODE_N = 42
        KEYCODE_O = 43
        KEYCODE_P = 44
        KEYCODE_Q = 45
        KEYCODE_R = 46
        KEYCODE_S = 47
        KEYCODE_T = 48
        KEYCODE_U = 49
        KEYCODE_V = 50
        KEYCODE_W = 51
        KEYCODE_X = 52
        KEYCODE_Y = 53
        KEYCODE_Z = 54
        KEYCODE_PLUS = 81  # +
        KEYCODE_MINUS = 69  # -
        KEYCODE_STAR = 17  # *
        KEYCODE_SLASH = 76  # /
        KEYCODE_EQUALS = 70  # =
        KEYCODE_AT = 77  # @
        KEYCODE_POUND = 18  # #
        KEYCODE_APOSTROPHE = 75  # '
        KEYCODE_BACKSLASH = 73  # \
        KEYCODE_COMMA = 55  # ,
        KEYCODE_PERIOD = 56  # .
        KEYCODE_LEFT_BRACKET = 71  # [
        KEYCODE_RIGHT_BRACKET = 72  # ]
        KEYCODE_SEMICOLON = 74  # ;
        KEYCODE_GRAVE = 68  # `
        KEYCODE_SPACE = 62  # 空格键
        KEYCODE_MEDIA_PLAY = 126  # 多媒体键 >> 播放
        KEYCODE_MEDIA_STOP = 86  # 多媒体键 >> 停止
        KEYCODE_MEDIA_PAUSE = 127  # 多媒体键 >> 暂停
        KEYCODE_MEDIA_PLAY_PAUSE = 85  # 多媒体键 >> 播放 / 暂停
        KEYCODE_MEDIA_FAST_FORWARD = 90  # 多媒体键 >> 快进
        KEYCODE_MEDIA_REWIND = 89  # 多媒体键 >> 快退
        KEYCODE_MEDIA_NEXT = 87  # 多媒体键 >> 下一首
        KEYCODE_MEDIA_PREVIOUS = 88  # 多媒体键 >> 上一首
        KEYCODE_MEDIA_CLOSE = 128  # 多媒体键 >> 关闭
        KEYCODE_MEDIA_EJECT = 129  # 多媒体键 >> 弹出
        KEYCODE_MEDIA_RECORD = 130  # 多媒体键 >> 录音


if __name__ == '__main__':
    adb = Adb_Tools()
    adb.install_apk(adb.check_local_file(),adb.check_devices_status())
    # adb.clear_package(adb.check_devices_status())
    # adb.check_adb_path()
    # adb.get_current_package(adb.check_devices_status())
    # adb.get_battery_info(adb.check_devices_status())
    # adb.remote_connectdev(adb.check_devices_status(),adb.get_ipconfig(adb.check_devices_status()))
    # adb.create_file(adb.check_devices_status(),method="touch",path="/sdcard/mkdirtes/test.txt")
    # adb.get_current_package(adb.check_devices_status())
    # adb.file_transfer(adb.check_devices_status(),method="remove",source="/sdcard/mkdirtes")
    # adb.get_process(adb.check_devices_status(),keyword="com.tencent.mobileqq")
    # adb.get_screenshot(adb.check_devices_status(),source="sdcard")
    # adb.get_ipconfig(adb.check_devices_status())
    # adb.is_install(adb.check_devices_status(),package_name="com.tencent.mobileqq")
    adb.get_display_state(adb.check_devices_status())