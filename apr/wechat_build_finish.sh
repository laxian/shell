#!/bin/bash

set -e

token=`cat token`
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token
archive_url=http://192.168.1.68/share/
nexus_url=http://192.168.1.68:8081/#browse/browse:rawrepo
resty_url=http://192.168.1.68:8082/files/jenkins/

timestamp=$(date "+%Y%m%d%H%M%S")
# mkdir -p /share/build-$BUILD_NUMBER/
bash -x ./trav.sh app/build/outputs/apk/ /share/build-$BUILD_NUMBER/

env=alpha
versionCode=`git rev-list HEAD --first-parent --count`
version=3.0.$versionCode

content="<font color = \\\"info\\\">【$JOB_NAME】</font>构建<font color=\\\"info\\\">成功~</font>😊\n>[查看控制台](${BUILD_URL}console) \n>版本: <font color=\\\"info\\\">${version}</font> \n>存档: - [nginx](${archive_url}) - [resty](${resty_url}) - [nexus](${nexus_url})"

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
