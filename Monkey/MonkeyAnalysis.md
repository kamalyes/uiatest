☀ 伪随机种子数与事件总数
:Monkey: seed=1519697655236 count=10

☀ 允许测试包
:AllowPackage: com.mryu.devstudy

☀ Category包含的LAUNCHER
:IncludeCategory: android.intent.category.LAUNCHER

☀ Category包含的MONKEY
:IncludeCategory: android.intent.category.MONKEY

☀ 查询允许包的activity 结果列表
// Selecting main activities from category android.intent.category.LAUNCHER

☀ 这些都不是指定包的activity
//   - NOT USING main activity com.android.browser.BrowserActivity (from package com.android.browser)
//   - NOT USING main activity com.android.calendar.homepage.AllInOneActivity (from package com.android.calendar)
//   - NOT USING main activity com.android.camera.Camera (from package com.android.camera)

.... ☀ 中间忽略，从这也可以看出你手机上都安装了哪些应用
☀ 这个就是我们指定的包的activity
// + Using main activity 包名1.ui.portal.WelcomeActivity (from package 包名1)
//   Selecting main activities from category android.intent.category.MONKEY

☀ 种子为1519697655236
// Seeded: 1519697655236

☀ 事件百分比
// Event percentages:
//   0: 15.0%
//   1: 10.0%
//   2: 2.0%
//   3: 15.0%
//   5: -0.0%
//   5: -0.0%
//   6: 25.0%
//   7: 15.0%
//   8: 2.0%
//   9: 2.0%
//   10: 1.0%
//   11: 13.0%

☀ 表示跳转到com.mryu.devstudy包中的com.mryu.devstudy.MainActivity里
☀ 查看log中第一个Switch，主要是查看 Monkey 执行的是那一个 Activity，譬如下面的 log 中，执行的是com.yulore.yellowpage/.activity.SplashActivity，
在下一个swtich之间的，如果出现了崩溃或其他异常，可以在该Activity中查找问题的所在。
:Switch:
#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;launchFlags=0x10200000;component=cn.yaomaitong.app.daily/cn.yaomaitong.app.ui.portal.WelcomeActivity;end

☀ 允许此Intent跳转
// Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=cn.yaomaitong.app.daily/cn.yaomaitong.app.ui.portal.WelcomeActivity } in package cn.yaomaitong.app.daily
// Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=cn.yaomaitong.app.daily/cn.yaomaitong.app.ui.portal.WelcomeActivity } in package cn.yaomaitong.app.daily

☀ 以下就是事件间的延迟和发送的各种事件
☀ --pct-nav事件
☀ sleeping for 0 milliseconds这句 log 是执行Monkey测试时，throttle设定的间隔时间，每出现一次，就代表一个事件。(这个事件是指从用户角度来说的一个事件，比如点击：实际包括手指按下与抬起两个动作，monkey日记将被记为2个事件）
Sleeping for 0 milliseconds
:Sending Key (ACTION_DOWN): 82    // KEYCODE_MENU
:Sending Key (ACTION_UP): 82    // KEYCODE_MENU
Sleeping for 0 milliseconds
:Switch:
#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;launchFlags=0x10200000;component=cn.yaomaitong.app.daily/cn.yaomaitong.app.ui.portal.WelcomeActivity;end
    // Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=cn.yaomaitong.app.daily/cn.yaomaitong.app.ui.portal.WelcomeActivity } in package cn.yaomaitong.app.daily
    // Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=cn.yaomaitong.app.daily/cn.yaomaitong.app.ui.portal.WelcomeActivity } in package cn.yaomaitong.app.daily

☀ --pct-touch事件
Sleeping for 0 milliseconds
:Sending Touch (ACTION_DOWN): 0:(532.0,1392.0)
:Sending Touch (ACTION_UP): 0:(552.05725,1391.5958)

☀ --pct-motion事件
Sleeping for 0 milliseconds
:Sending Touch (ACTION_DOWN): 0:(838.0,113.0)
:Sending Touch (ACTION_UP): 0:(852.82526,101.77225)

☀ --pct-trackball事件
Sleeping for 0 milliseconds
:Sending Trackball (ACTION_MOVE): 0:(1.0,5.0)
:Sending Trackball (ACTION_MOVE): 0:(-5.0,-3.0)

☀ --pct-rotation屏幕旋转百分比 ####隐藏事件
: Sending rotation degree=0, persist=true
: Sending rotation degree=1, persist=false:
: Sending rotation degree=2, persist=true
: Sending rotation degree=3, persist=false

☀ 注入事件10
Events injected: 10

☀ 发送屏幕翻转 度=0，存留=假
:Sending rotation degree=0, persist=false

☀ 丢弃：键=0，指针=0，轨迹球=0，键盘轻弹=0，屏幕翻转=0
:Dropped: keys=0 pointers=0 trackballs=0 flips=0 rotations=0

☀ 网络状态：占用时间=52ms（手机0ms，wifi0ms，未连接52ms）
## Network stats: elapsed time=52ms (0ms mobile, 0ms wifi, 52ms not connected)

☀ 如果 Monkey 测试顺利执行完成，在 log 的最后，会打印出当前执行事件的次数和所花费的时间Monkey finished代表执行完成。Monkey 执行完成的 log 具体如下：
Events injected: 100:Sending rotation degree=0, persist=false:Dropped: keys=0 pointers=0 trackballs=0 flips=0 rotations=0## Network stats: elapsed time=2052ms (0ms mobile, 0ms wifi, 2052ms not connected)// Monkey finished

☀ Monkey 执行中断，在 log 的最后也能查看到当前大约已执行的次数
:Sending Trackball (ACTION_MOVE): 0:(-3.0,1.0):Sending Trackball (ACTION_MOVE): 0:(5.0,0.0)    //[calendar_time:2021-01-12 11:23:50.322  system_uptime:718998]    // Sending event #7500:Sending Trackball (ACTION_MOVE): 0:(3.0,-2.0)

☀ Monkey测试完成
// Monkey finished

☀ CRASH输出LOG：

// CRASH: com.mryu.devstudy (pid 22244)
// Short Msg: java.lang.NullPointerException
// Long Msg: java.lang.NullPointerException: Attempt to invoke virtual method 'android.graphics.drawable.Drawable android.widget.TextView.getBackground()' on a null object reference
// Build Label: vivo/PD1616B/PD1616B:8.1.0/OPM1.171019.019/compil10091613:user/release-keys
// Build Changelist: eng.compil.20201009.161326
// Build Time: 1602231206000
// java.lang.RuntimeException: Unable to start activity ComponentInfo{com.mryu.devstudy/com.mryu.devstudy.activity.SplashActivity}: java.lang.NullPointerException: Attempt to invoke virtual method 'android.graphics.drawable.Drawable android.widget.TextView.getBackground()' on a null object reference
// 	at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:3012)
// 	at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:3090)
// 	at android.app.ActivityThread.-wrap11(Unknown Source:0)
// 	at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1794)
// 	at android.os.Handler.dispatchMessage(Handler.java:106)
// 	at android.os.Looper.loop(Looper.java:192)
// 	at android.app.ActivityThread.main(ActivityThread.java:6866)
// 	at java.lang.reflect.Method.invoke(Native Method)
// 	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:549)
// 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:817)
// Caused by: java.lang.NullPointerException: Attempt to invoke virtual method 'android.graphics.drawable.Drawable android.widget.TextView.getBackground()' on a null object reference
// 	at com.mryu.devstudy.activity.SplashActivity.initView(SplashActivity.java:73)
// 	at com.mryu.devstudy.activity.SplashActivity.onCreate(SplashActivity.java:54)
// 	at android.app.Activity.performCreate(Activity.java:7122)
// 	at android.app.Activity.performCreate(Activity.java:7113)
// 	at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1220)
// 	at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2965)
// 	... 9 more
Terminated 
☀ ANR输出LOG
//NOT RESPONDING:com.android.quicksearchbox(pid 6333)
ANR in com.android.quicksearchbox(com.android.quicksearchbox/.SearchActivity)
CPU usage from 8381ms to 2276ms ago:
procrank: ->adb shell procrank
anr traces: ->保存于/data/anr/traces.txt
meminfo: ->adb shell dumpsys meminfo
Bugreport ->adb bugreport 可选通过 --bugreport 参数控制


 算术异常类：ArithmeticExecption
 空指针异常类：NullPointerException
 类型强制转换异常：ClassCastException
 数组负下标异常：NegativeArrayException
 数组下标越界异常：ArrayIndexOutOfBoundsException
 违背安全原则异常：SecturityException
 文件已结束异常：EOFException
 文件未找到异常：FileNotFoundException
 字符串转换为数字异常：NumberFormatException
 操作数据库异常：SQLException
 输入输出异常：IOException
 违法访问错误：IllegalAccessError
 内存不足错误：OutOfMemoryError
 堆栈溢出错误：StackOverflowError