#!/bin/bash

set -e

. ./env.sh
token=$(cat token)
notify_url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$token

. ./server_check.sh
content="<font color = \\\"info\\\">【$JOB_NAME】</font>构建<font color=\\\"info\\\">成功~</font>😊\n>[查看控制台](${BUILD_URL}console) \n>版本: <font color=\\\"info\\\">${version}</font> \n>commit: <font color=\\\"info\\\">${git_version}</font> \n>存档: $nginx $resty $nexus $maven"

. ./notify.sh
wechat_notify $token "$content"
