#!/bin/sh

set -e

token=`cat token`
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token
archive_url=http://192.168.1.68/share/

timestamp=$(date "+%Y-%m-%d_%H:%M:%S")
mkdir -p "share/$timestamp/"
./trav.sh app/build/outputs/apk/ /share/$timestamp/

# content="## 打包完成 \n 
#     [apk](http://192.168.1.68/share/)"

env=alpha
versionCode=`git rev-list HEAD --first-parent --count`
version=3.0.$versionCode

content="<font color="info">${env}</font>打包 \n 
    >版本:${version}
    >存档:${archive_url}}
    >发布时间:${timestamp}"

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
