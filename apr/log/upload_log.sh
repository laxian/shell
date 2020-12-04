#!/usr/bin/env bash

# ----------------------------
# 发送上传日志命令
# $1 robot id
# $2 日志路径
# 拉取环境release，暂无自定义必要
# 拉取时间为2020-06-01 -> now
# 发送成功后，使用query_log.sh 拉取
# ----------------------------

env=release
robot_id=$1
path=$2
endtime=`date +%s`

curl "http://nav-center-api.loomo.com/robot/log/toUploadLog" \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H "authToken: 1165a2f238cc4cf8babc367ab34ce77b" \
  -H "Origin: http://nav-center.loomo.com" \
  -H "Referer: http://nav-center.loomo.com/" \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  --data-binary "{\"robotId\":\"$robot_id\",\"environment\":\"$env\",\"logPath\":\"$path\",\"startTime\":1590984000000,\"endTime\":${endtime}000}" \
  --compressed \
  --insecure