#!/bin/bash -x

#--------------------------------------------
# 配置到jenkins构建步骤中，token须换成真实token
#--------------------------------------------

set -e

env=dev
words=`git log -n 1 | sed '/\(commit\|Author\|Date\|Merge:\|Merge branch\|See merge\|^[ ]*$\)/d'`
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
token=XXXXXX
echo $env $words $timestamp $token

notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token

content_dev="业务软件更新：\n$words"

json="{
    \"msgtype\": \"text\",
    \"text\": {
        \"content\": \"$content_dev\",
        \"mentioned_mobile_list\":[\"17718390905\", \"18811497615\", \"13693217025\"]
    }
}"

echo $json

curl $notify_url \
    -H 'Content-Type: application/json' \
    -d "$json"
