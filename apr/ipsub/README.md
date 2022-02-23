# IP压缩方案自动化部署工具集

IP自动部署工具

## http目录

### http.sh

遍历各个项目，替换http地址
接收一个参数，指定项目路径列表。可空，使用同目录下的列表

## mqtt目录

### mqtt.sh

遍历各个项目，替换mqtt地址
接收一个参数，指定项目路径列表。可空，使用同目录下的列表

## deploy.sh

一键部署功能

1. 根据projs指定项目目录
2. 对每一个项目执行：
3. 从最新dev分支创建新分支
4. 从ip键值对执行全量搜索替换
5. gradle构建
6. apk签名并复制到根目录
7. apk安装

## netbare_log.sh

实时查看日志

```Bash
./netbare_log tcp
./netbare_log http
./netbare_log
```

## remove_all.sh

移除所有列表中的app

## root.sh

root、remount、disverity、reboot

## view_install.sh

验证安装路径
