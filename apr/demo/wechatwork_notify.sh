#!/bin/bash

#--------------------------------------------
# 发送消息到wechat work机器人
# 必须带两个参数，env和version
#--------------------------------------------

set -e
token=$(cat ../private/token)
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token

Usage() {
    echo
    echo "参数错误" 1>&2
    echo "eg: wechatwork_notify.sh alpha 1.1.9" 1>&2
    exit 1
}

if [ $# -lt 2 ]; then
    Usage
fi

env=$1
version=$2
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
wiki="https://wiki.segwayrobotics.com/pages/viewpage.action?pageId=50280499"
echo $env $version

content="业务软件在<font color=\\\"info\\\">${env}</font>环境下发布, 请相关同学注意 \n >版本:${version} >更新日志:${wiki} >发布时间:${timestamp}"

json="{
        \"msgtype\": \"markdown\",
        \"markdown\": {
            \"content\": \"$content\"
        }
   }"

echo $json

curl $notify_url \
    -H 'Content-Type: application/json' \
    -d "$json"
