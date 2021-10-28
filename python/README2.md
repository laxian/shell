# 机器人segway系列命令行工具使用说明

我们有完善的日志上传体系，但是上传、检索、下载、解压、打开、查看，仍是一个冗余耗时的操作。

此工具集的初衷，就是简化日志操作，将上传、检索、下载、解压、打开、查看，合并到一行命令，最初是shell实现，随着功能的复杂，改用Python实现。后续又添加了一系列便捷功能，希望可以save your time。

后期的修改舍弃了Python2.x的兼容测试，Python2.x的bug不再修改，建议使用Python3.9。

## 安装

本文假设Python环境变量设置正确，在Windows和Mac上经过了一段时间实际场景的测试，

```Bash
# 最新版本0.0.9
pip install http://${adb_ip}:8080/files/pull_log-0.0.9.tar.gz
```

## 配置

### 查看配置

```Bash
$ segway_showconfig
{
    "env": "release",
    "log_dir": "~/Downloads",
    "open_app": "code",
    "password": "******",
    "retry_interval": 1,
    "log_start_time": "2020-12-18_00:00:00"
    "retry_limit": 20,
    "token": "${token}",
    "username": "${username}"
}
```

### 修改配置

```Bash
segway_config username=xxx.xxx@ninebot.com password=******
```

## 功能列表

安装完成，直接打开终端输入`segway`查看

```Bash
$ segway
author ${username}
version 0.0.9
Commands:
    segway_adb adb解密
    segway_auto <robot_id> <log_path> (上传->查询->拉取->下载->打开)自动获取远程日志
    segway_config 个性化配置：可配置项见配置部分
    segway_download <url> 下载日志
    segway_fetch <url>  下载并打开日志
    segway_nav GUI窗口，拉取nav日志
    segway_login 登录刷新token
    segway_pull <path> 本地拉取指定path日志并打开
    segway_pull_ex [Deprecated]本地拉取/sdcard/ex 日志并打开
    segway_pull_s2 本地拉取/sdcard/logs_folder/com.segway.robotic.app 日志并打开
    segway_pull_sys 本地拉取/data/logs 日志并打开
    segway_query <robot_id> [index] 查询日志url
    segway_query2 <robot_id> [option] 高级查询，输入segway_query2 获取帮助
    segway_showconfig 显示配置
    segway_upload <robot_id> 上传指定robot_id的日志
    segway_status <robot_id> 格式化打印机器人状态（导航）
    segway_status2 <robot_id> [dev|alpha|...] 格式化打印机器人状态（业务）
    segway_restore <robot_id> [dev|alpha|...]重置
    segway_available <robot_id> [false|true|] [dev|alpha|...]可用
    segway_arrive <robot_id> [dev|alpha|...]到达
    segway_share <file_path> 开启文件服务器，以url方式分享本地文件
    segway_broken <robot_id> [env=dev] [error_code=110123] [msg=test] 模拟机器人进故障
    segway_shield <robot_id> [true|false] [env=dev] 屏蔽导航
    segway_clear_tasks <robot_id> [env=dev] 中断并完成所有任务
    segway_box <robot_id> 0123 ['open'|'close'] [env=dev] 开关箱
```

## 主要功能说明

### 查看所有commands

```Bash
segway
```

### 一键展现日志

1. 上传日志，记录当前时间；
2. 轮询日志，比对时间，没1s轮询，默认20次
3. 时间在发起上传[-1s, 5s]取件内
4. 下载
5. 解压
6. 打开，默认使用code打开，

如果失败，使用文件管理器打开目录：

```Bash
Windows： start
linux：nautilus
Mac OS：open
```

```Bash
segway_auto GXBOX-S2DGH2032C0003 /sdcard/ex
```

### adb解密(via adb)

```Bash
segway_adb
```

### 上传指定目录日志

```Bash
segway_upload GXBOX-S2DGH2032C0003 /sdcard/ex
```

### 查询日志后台

```Bash
# 查询所有
segway_query GXBOX-S2DGH2032C0003 
# 查询第一个
segway_query GXBOX-S2DGH2032C0003 0
# sample
$ segway_query GXBOX-S2DGH2032C0003 0
http://robot-base.${host_part_2}.com/aws/web/file/download/?bucketName=ota-robot-base&objectKey=log/GXBOX-S2DGH2032C0003_2020-12-14_14-13-23-175_M.zip
```

### 新查询日志后台

```Bash
# 建议使用segway_query2，支持查询指定字段
segway_query2 GXBOX-S1RLM2103C0006 logUrl logPath commandMessage
# outputs 如下：
---------
"/data/logs"
"指令已发出"
---------
"http://robot-base.${host_part_2}.com/aws/web/file/download?bucketName=ota-robot-base&objectKey=log/GXBOX-S1RLM2103C0006_2021-09-01_16-10-20-002_M.zip"
"/sdcard/ex/app"
"指令已完成"
```

还可以指定值过滤查询

```Bash
segway_query2 <id> [option]
# sample
segway <id> logUrl logPath=/sdcard/ex
```

### 下载

```Bash
segway_download https://.../xxx.zip
```

### 下载并打开

```Bash
segway_fetch https://.../xxx.zip
```

### 拉取nav日志(via adb)

```Bash
# 修改了王晶的 dumpNavlog.py工具，给窗口添加了滚动条
segway_nav
```

### 拉取本地日志(via adb)

```Bash
# 指定path
segway_pull /sdcard/ex
# 快捷拉取业务(日志路径已变更，后续将移除)：/sdcard/ex
segway_pull_ex
# 快捷拉取S2业务日志：/sdcard/logs_folder/<S2App包名>/
segway_pull_s2
# 快捷拉取data/logs
segway_pull_sys
```

### 获取机器人状态(导航)

```Bash
# 所有含0003的机器人的状态
segway_status 0003

# 获取EVT7-10状态
$ segway_status EVT7-10
<Response [200]>

        ID：  EVT7-10
        状态：  offline
        系统：  RK-navigation-userdebug-dev_1.1.711
        环境：  alpha3
        navAppId:  0.6.1334
        楼座：  东升科技园北领地A4号楼-1
        errcodeId:  101
        ttsId：  12
        在线时间： 2020-12-11 16:57:42
        离线时间： 2020-12-11 18:06:57
        设置：
{
    "NavServicURL": "ssl://120.131.7.82:8885"
}

# 查询所有含0003的机器人的ID(Windows 可使用findStr 替换grep)
$ segway_status 0003 | grep ID
        ID：  B2D120D12F0003
        ID：  ${PREFIX}0003
        ID：  S1RLM2047C0003
        ID：  S1RLM2048C0003
        ID：  S1RLM2049C0003
        ID：  S2DGH2032C0003

# Windows
segway_status 0003 | findStr ID
```

### 获取机器人状态(业务)

```Bash
segway_status2 0003
---------------------------------------
        ID:  S2DGH2032C0003
        状态:  Moving
        可用:  False
        在线:  True
        broken:  True
        电量:  90.0
        昵称:  秀秀_小赛
        箱格数:  4
        预占:  0
        剩余:  4
        已使用:  0
        待命点:  饮水机
        当前站点: 饮水机
        楼宇:  测试楼宇
        楼座:  None
        警告:  True
```

### 机器人操作

```Bash
# 初始化
segway_restore EVT6-2-1
# 可用
segway_available EVT6-2-1
# 到达
segway_arrive EVT6-2-1
```

### 本地文件分享

```Bash
# 启动http server，分享当前目录
$ segway_share .
http://192.168.1.69:5000
Serving HTTP on :: port 5000 (http://[::]:5000/) ...
```

## BUG REPORT

如遇bug，请截图发送给我，谢谢。

企业微信: 周卫贤

email: ${username}
