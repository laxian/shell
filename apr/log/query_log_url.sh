#!/usr/bin/env bash

# ----------------------------
# 快速下载日志
# $1 robot id 关键字过滤
# $2 指定拉取第行，默认0
# ----------------------------

keyword=$1
line=${2-0}

ordinal() {
  if [ $1 == 1 ]; then
    echo 1st
  elif [ $1 == 2 ]; then
    echo 2nd
  elif [ $1 == 3 ]; then
    echo 3rd
  else
    echo ${1}th
  fi
}

curl -s "http://nav-center-api.loomo.com/robot/log/management?page=1&pageSize=10&startCreateTime=&endCreateTime=&robotId=$keyword&logPath=&logType=&environment=&mapName=&commandStatus=" \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H "authToken: 1165a2f238cc4cf8babc367ab34ce77b" \
  -H "Origin: http://nav-center.loomo.com" \
  -H "Referer: http://nav-center.loomo.com/" \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  --compressed \
  --insecure \
  | grep logUrl \
  | head -n $(($line+1)) \
  | tail -n 1 \
  | grep "http.*\.zip" \
  | sed 's/.*\(http.*\.zip\).*/\1/g' \
  | grep zip || echo "NOT FOUND!!!"

