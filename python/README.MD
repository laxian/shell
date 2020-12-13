# 拉取日志-Python版本

> 让拉取远程和本地日志，想浏览网页一样容易

## 配置环境
推荐使用virtualenv。本项目使用Python3.9开发，通过Python2.7兼容测试
Python3.0 ~ Python3.5 有部分语法不支持

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
```json
{
  "username": "${username}",
  "password": "${password}",
  "token": "${token}",
  "env": "release",
  "open_app": "code",
  "retry_limit": 20,
  "retry_interval": 1,
  "log_dir": "/Users/leochou/Downloads"
}
```

key | 作用 |
---------|----------
 username | 用户名
 password | 用户密码
 token | 用户token，如有则无需登录
 env | 日志环境
 open_app | 打开应用带路径
 retry_limit | 重试次数
 retry_interval | 重试时间间隔
 log_dir | 日志解压绝对路径

 ## 使用

 - 安装
 ```
 pip install pull-log-0.0.2
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
    segway_showconfig 显示配置
    segway_upload <robot_id> 上传指定robot_id的日志
    segway_status <robot_id> 格式化打印机器人状态
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
 - [ ] adb解密跳过未加密设备
 - [ ] More samples
 - [ ] 本地日志分享
 - [ ] 代码优化
 - [ ] 高频操作（可用、初始化、到达）支持