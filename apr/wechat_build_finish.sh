#!/bin/sh

set -e

token=xxxxxx
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token

timestamp=$(date "+%Y-%m-%d %H:%M:%S")
./t.sh app/build/outputs/apk/ /share/$timestamp

content="## 打包完成 \n 
    [apk](http://192.168.1.68/share/)"

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
