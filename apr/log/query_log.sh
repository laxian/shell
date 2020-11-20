#!/usr/bin/env bash

# ----------------------------
# 快速下载日志
# $1 robot id 关键字过滤
# $2 跳过前n个，可选
# ----------------------------

keyword=$1
line=${2-1}

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

echo pull log of $keyword, the `ordinal ${line}` line

curl -s "http://${host_part_1}-api.${host_part_2}/robot/log/management?page=1&pageSize=10&startCreateTime=&endCreateTime=&robotId=$keyword&logPath=&logType=&environment=&mapName=&commandStatus=" \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H "authToken: ${auth}" \
  -H "Origin: http://${host_part_1}.${host_part_2}" \
  -H "Referer: http://${host_part_1}.${host_part_2}/" \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  --compressed \
  --insecure \
  | grep logUrl \
  | head -n $(($line+1)) \
  | tail -n 1 \
  | sed 's/.*\(http.*\.zip\).*/\1/g' \
  | xargs -I URL curl -LO URL

