#!/bin/bash

set -e

. ./env.sh
token=$(cat token)
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token
nginx_url=http://localhost/share/
resty_url=http://localhost:8082/files/jenkins/
nexus_url=http://localhost:8081/#browse/browse:rawrepo
maven_url=http://localhost:8081/#browse/browse:maven-releases

nginx_status=$(curl -s -m 5 -IL $nginx_url | grep 200 | cut -d' ' -f2)
resty_status=$(curl -s -m 5 -IL $resty_url | grep 200 | cut -d' ' -f2)
nexus_status=$(curl -s -m 5 -IL $nexus_url | grep 200 | cut -d' ' -f2)
maven_status=$(curl -s -m 5 -IL $maven_url | grep 200 | cut -d' ' -f2)

[[ "$nginx_status" == 200 ]] && nginx="[nginx](${nginx_url})"
[[ "$resty_status" == 200 ]] && resty="[resty](${resty_url})"
[[ "$nexus_status" == 200 ]] && nexus="[nexus](${nexus_url})"
[[ "$maven_status" == 200 ]] && maven="[maven](${maven_url})"

content="<font color = \\\"info\\\">【$JOB_NAME】</font>构建<font color=\\\"info\\\">成功~</font>😊\n>[查看控制台](${BUILD_URL}console) \n>版本: <font color=\\\"info\\\">${version}</font> \n>commit: <font color=\\\"info\\\">${git_version}</font> \n>存档: $nginx $resty $nexus $maven"

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
