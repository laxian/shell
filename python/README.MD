# 拉取日志-Python版本

> 让拉取远程和本地日志，想浏览网页一样容易

## 配置环境

推荐使用virtualenv。本项目使用Python3.9开发，通过Python2.7兼容测试

- 创建虚拟环境3.9到venv目录

```shell
virtualenv venv --python=python3.9
```

- 激活
  
```shell
source venv/bin/activate
```

- 安装依赖

```shell
pip install -r requirements.txt
```

- 替换敏感信息
代码里有一些`${xxx}`字段，需要替换

- 配置个性化参数

config.json

```JSON
{
  "username": "${username}",
  "password": "${password}",
  "token": "${token}",
  "env": "release",
  "open_app": "code",
  "log_start_time": "2020-12-17_12:00:00",
  "retry_limit": 20,
  "retry_interval": 1,
  "log_dir": "~/Downloads"
}
```

key | 作用 |
---------|----------
username | 用户名
password | 用户密码
token | 用户token，如有则无需登录
env | 日志环境
open_app | 打开应用带路径
log_start_time | 日志起始时间
retry_limit | 重试次数
retry_interval | 重试时间间隔
log_dir | 日志解压绝对路径

## 使用

- 安装
  
```shell
pip install pull-log-0.0.7.tar.gz
```

或者通过url安装

```shell
pip install http://${adb_ip}:8080/files/pull_log-0.0.7.tar.gz
```

- 显示命令列表
  
```shell
$ segway
Commands:
    segway_adb adb 解密
    segway_auto <robot_id> <log_path> (上传->查询->拉取->下载->打开)自动获取远程日志
    segway_config 个性化配置：可配置项见配置部分
    segway_download <url> 下载日志
    segway_fetch <url>  下载并打开日志
    segway_nav GUI窗口，拉取nav日志 
    segway_login 登录刷新token
    segway_pull <path> 本地拉取指定path日志并打开
    segway_pull_ex 本地拉取/sdcard/ex 日志并打开
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
 ```

## 问题记录

[PROBLEMS.MD](https://github.com/laxian/shell/blob/dev/python/PROBLEMS.MD)

## issue

- [x] 解压跨平台实现
- [x] setup.py
- [x] 整合dumpnavLog.py
- [x] dumpnavLog.py 界面优化，添加滚动条
- [x] python实现adb解密
- [x] 整合本地拉取log
- [x] 获取机器人状态
- [x] 高频操作（可用、初始化、到达）支持
- [x] 配置目录支持'~'相对路径
- [x] 拉取起始日期可配置
- [x] adb解密跳过未加密设备
- [x] 高频操作（可用、初始化、到达）可切换环境
- [x] 业务板机器人状态
- [x] 本地日志快速分享
- [x] 一键进故障
- [x] 屏蔽导航
- [x] 一键取消所有订单任务
- [x] 导航日志指定结束时间
- [ ] 100%覆盖自动化测试
- [ ] 可签名且秘钥路径签名可配置
- [ ] 代码优化
- [ ] More samples
- [ ] 输出信息开关与优化
