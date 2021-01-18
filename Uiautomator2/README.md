### uiautomator2 一款比appium还好用的app自动化测试框架
###（一）uiautomator2简介和原理分析
uiautomator2是一个自动化测试开源工具，仅支持Android平台的原生应用测试。它本来是Google提供的一个自动化测试的Java库，后来发展了python-uiautomator2，封装了谷歌自带的uiautomator测试框架，提供便利的python接口，用它可以很便捷的编写python脚本来实现app的自动化测试
原理解析：
#####python端：运行脚本，往移动端发送HTTP请求移动端：安装atx-agent，然后atx-agent启动uiautomator2服务进行监听，并识别python脚本，转换为uiautomator2的代码
#####移动设备通过WIFI(同一网段)或USB接收到PC上发来的HTTP请求，执行制定的操作
###（二）安装
##### 1、下载androidsdk，并配置环境变量
##### 2、安装uiautomator2  这里推荐用清华源或者豆瓣源来安装
``` pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --pre -U uiautomator2 ```
##### 3、设备初始化：首先设备连接到PC adb devices发现该设备后安装atx-agent
```
xxxxx\AutoFramework>adb devices
List of devices attached
M960BDQH222CP   device
python -m uiautomator2 init
``` 
##### 4、首先看设备连接上了导包
``` 
import uiautomator2 as uiauto 
ui= uiauto.connect('M960BDQH222CP')
print(ui.device_info)
``` 
##### 5、打印出来这个设备的所有信息、这就说明连接是成功的接下来需要定位元素，这里介绍一款好用的定位工具：weditor ，不仅可以实时定位，而且还可以在里面编写调试代码
###（三）视图化插件 weditor
##### 1、安装
``` pip install -i https://pypi.douban.com/simple weditor``` 
##### 2、初始化启动
``` python -m weditor```  
浏览器打开一个网页 点击Dump Hierarchy，就可以在浏览器显示出手机的屏幕了，打开实时，能实时看到
