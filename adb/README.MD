# 常用ADB

| adb | -e/-d/-s                                           |
|-----|----------------------------------------------------|
| -e  | 指定当前唯一运行的模拟器为命令目标                 |
| -s  | 后跟deviceId，指定设备                             |
| -d  | 指定当前唯一通过 USB 连接的 Android 设备为命令目标 |


列出应用

```shell
# 所有应用
$ adb shell pm list packages
# 系统应用
$ adb shell pm list packages -s
# 三方应用
$ adb shell pm list packages -3
```

adb install

| 参数 | 含义                                                                            |
|------|---------------------------------------------------------------------------------|
| -d   | 允许降级覆盖安装                                                                |
| -g   | 授予所有运行时权限                                                              |
| -l   | 将应用安装到保护目录 /mnt/asec                                                  |
| -r   | 允许覆盖安装                                                                    |
| -s   | 将应用安装到 sdcard                                                             |
| -t   | 允许安装 AndroidManifest.xml 里 application 指定 android:testOnly="true" 的应用 |


清除应用数据与缓存

`adb shell pm clear <packagename>`

查看前台 Activity

`adb shell dumpsys activity activities | grep mResumedActivity`

查看正在运行的 Services

`adb shell dumpsys activity services [<packagename>]`

键盘输入

`adb shell input keyevent <keycode>`

| keycode | 含义                           |
|---------|--------------------------------|
| 3       | HOME 键                        |
| 4       | 返回键                         |
| 5       | 打开拨号应用                   |
| 6       | 挂断电话                       |
| 24      | 增加音量                       |
| 25      | 降低音量                       |
| 26      | 电源键                         |
| 27      | 拍照（需要在相机应用里）       |
| 64      | 打开浏览器                     |
| 82      | 菜单键                         |
| 85      | 播放/暂停                      |
| 86      | 停止播放                       |
| 87      | 播放下一首                     |
| 88      | 播放上一首                     |
| 122     | 移动光标到行首或列表顶部       |
| 123     | 移动光标到行末或列表底部       |
| 126     | 恢复播放                       |
| 127     | 暂停播放                       |
| 164     | 静音                           |
| 176     | 打开系统设置                   |
| 187     | 切换应用                       |
| 207     | 打开联系人                     |
| 208     | 打开日历                       |
| 209     | 打开音乐                       |
| 210     | 打开计算器                     |
| 220     | 降低屏幕亮度                   |
| 221     | 提高屏幕亮度                   |
| 223     | 系统休眠                       |
| 224     | 点亮屏幕                       |
| 231     | 打开语音助手                   |
| 276     | 如果没有 wakelock 则让系统休眠 |

输入文本

`adb shell input text hello`

查看设备信息

- 型号

`adb shell getprop ro.product.model`

- 屏幕

```shell
$ adb shell wm size
Physical size: 1920x1200
$ adb shell wm density
Physical density: 225
```

- 显示器参数

`adb shell dumpsys window displays`

- 系统版本

`adb shell getprop ro.build.version.release`

- ip

`adb shell ifconfig | grep Mask`
或者，部分机型：
`adb shell netcfg`

- MAC 地址

`adb shell cat /sys/class/net/wlan0/address`

- CPU 信息

`adb shell cat /proc/cpuinfo`

- 内存信息

`adb shell cat /proc/meminfo`

屏幕截图

`adb exec-out screencap -p > sc.png`

录制屏幕

`adb shell screenrecord /sdcard/filename.mp4`

系统操作

```shell
# root 身份运行
$ adb root
# 重启
$ adb reboot
# 重新挂载
$ adb remount
# 重启到 Recovery 模式
$ adb reboot recovery
# 重启到 Fastboot 模式
$ adb reboot bootloader
# 禁用dm_verity
$ adb disable-verity
# 查看进程
$ adb shell ps
# 查看实时资源占用情况
$ adb top
```

无线连接

```shell
adb tcpip 5555
adb connect <device-ip-address>
adb devices
adb disconnect <device-ip-address>
```


## expert_installed_apk
导出已安装的apk
```shell
# 以豆瓣为例
~ adb shell pm list packages | grep douban
package:com.douban.frodo

~ adb shell pm path com.douban.frodo
package:/data/app/com.douban.frodo-3MPKjrePTfpmBRjP24ESnw==/base.apk

~ adb pull /data/app/com.douban.frodo-3MPKjrePTfpmBRjP24ESnw==/base.apk ./douban.com
/data/app/com.douban.frodo-3MPKjrePTfp.... 38.9 MB/s (41950908 bytes in 1.030s)
➜  ~
```

