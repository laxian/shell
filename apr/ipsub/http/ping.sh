#!/usr/bin/env bash

ips=(api-doc-delivery.lllll.com
jira.sssssrobotics.com
amazonaws.com.cn
amazonaws.com
robot-base-us.lllll.com
robot-base.lllll.com
nav-demo-mqtt.lllll.com
nav-release-mqtt.lllll.com
nav-internal-mqtt.lllll.com
robot-base-alpha.lllll.com
api-gate-alpha-delivery.lllll.com
api-gate-dev-delivery.lllll.com
api-gate-internal-delivery.lllll.com
api-gate-delivery.lllll.com
alpha-api-sssssgo.sssssrobotics.com
dev-api-sssssgo.sssssrobotics.com
internal-api-sssssgo.sssssrobotics.com
api-sssssgo.sssssrobotics.com
ota-robot-base.s3.cn-north-1.amazonaws.com.cn
ore-apr-robot-base.s3.us-west-2.amazonaws.com
120.131.7.82
120.131.2.240
120.92.209.166
120.92.80.137
120.92.78.197
208.67.222.222
60.222.12.83
60.222.12.84
60.222.12.85
60.222.12.77
60.222.12.79
60.222.12.78
60.222.12.80
120.92.14.183
qq.com
z.cn
taobao.com
)

urls=(http://robot-base-us.lllll.com
    http://robot-base.lllll.com
    http://nav-demo-mqtt.lllll.com
    http://nav-release-mqtt.lllll.com
    http://nav-internal-mqtt.lllll.com
    http://robot-base-alpha.lllll.com
    https://api-gate-alpha-delivery.lllll.com/
    https://api-gate-dev-delivery.lllll.com/
    https://api-gate-internal-delivery.lllll.com/
    https://api-gate-delivery.lllll.com/
    https://alpha-api-sssssgo.sssssrobotics.com/
    https://dev-api-sssssgo.sssssrobotics.com/
    https://internal-api-sssssgo.sssssrobotics.com/
    https://api-sssssgo.sssssrobotics.com/
    https://ota-robot-base.s3.cn-north-1.amazonaws.com.cn
    https://ore-apr-robot-base.s3.us-west-2.amazonaws.com)

pingIp() {
    ping -c 1 $1 >/dev/null && echo $1 \\t\\t "\033[42;37m OK \033[0m" || echo $1 \\t\\t "\033[41;37m FAILED \033[0m"
}

head() {
    status=$(curl -s -m 5 -IL $1 | grep -E "HTTP.*?\s\d{3,}" | cut -d' ' -f2 | tr '\n' '-')
    if [ -z $status ]; then
        echo $1 \\t\\t "\033[41;37m FAILED \033[0m"
    else
        echo $1 \\t\\t "\033[42;37m $status \033[0m"
    fi
}

for ip in ${ips[@]}; do
    pingIp $ip
done

# for url in ${urls[@]}; do
#     # head $url && echo $1 \\t\\t "\033[42;37m OK \033[0m" || echo $1 \\t\\t "\033[41;37m FAILED \033[0m"
#     head $url
# done
