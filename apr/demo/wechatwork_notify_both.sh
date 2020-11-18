#!/bin/bash -x

#--------------------------------------------
# 发送消息到wechat work机器人
# 必须带两个参数，env和version
#--------------------------------------------

set -e

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

if [[ $env == "release" ]]; then
    token=$(cat ../private/token)
else
    token=$(cat ../private/token-dev)
fi

notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token

content="业务软件在<font color=\\\"info\\\">${env}</font>环境下发布, 请相关同学注意 \n >版本: <font color=\\\"info\\\">${version}</font> \n>[更新日志](${wiki}) \n>发布时间: ${timestamp}"

content_dev="业务软件更新：\n$version"

json="{
        \"msgtype\": \"markdown\",
        \"markdown\": {
            \"content\": \"$content\"
        }
   }"

json_dev="{
    \"msgtype\": \"text\",
    \"text\": {
        \"content\": \"$content_dev\",
        \"mentioned_mobile_list\":[\"17718390905\", \"18811497615\", \"13693217025\"]
    }
}"

if [[ $env != "release" ]]; then
    json=$json_dev
fi

echo $json

curl $notify_url \
    -H 'Content-Type: application/json' \
    -d "$json"
