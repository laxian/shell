#!/bin/bash

set -e

. ./env.sh
token=`cat token`
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token
archive_url=http://localhost/share/
nexus_url=http://localhost:8081/#browse/browse:rawrepo
resty_url=http://localhost:8082/files/jenkins/


content="<font color = \\\"info\\\">【$JOB_NAME】</font>构建<font color=\\\"info\\\">成功~</font>😊\n>[查看控制台](${BUILD_URL}console) \n>版本: <font color=\\\"info\\\">${version}</font> \n>commit: <font color=\\\"info\\\">${git_version}</font> \n>存档: - [nginx](${archive_url}) - [resty](${resty_url}) - [nexus](${nexus_url})"

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
