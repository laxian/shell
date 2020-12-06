# 拉取日志-Python版本

> 使用Shell版本写了一套拉取日志的代码，实际使用中，可以在3s内将日志呈现在vscode窗口中，大大节省了查找线上问题
的准备环节。但由于Shell糟糕的兼容性，所以我用Python实现一下。虽然自用还是倾向于Shell版

## 配置环境
推荐使用virtualenv。本项目同事支持Python2.x和Python3.x，推荐使用Python3.x

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

 ## issue
 - [x] 解压跨平台实现