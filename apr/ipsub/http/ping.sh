#!/usr/bin/env bash

ips=(api-doc-delivery.loomo.com
jira.segwayrobotics.com
amazonaws.com.cn
amazonaws.com
robot-base-us.loomo.com
robot-base.loomo.com
nav-demo-mqtt.loomo.com
nav-release-mqtt.loomo.com
nav-internal-mqtt.loomo.com
robot-base-alpha.loomo.com
api-gate-alpha-delivery.loomo.com
api-gate-dev-delivery.loomo.com
api-gate-internal-delivery.loomo.com
api-gate-delivery.loomo.com
alpha-api-segwaygo.segwayrobotics.com
dev-api-segwaygo.segwayrobotics.com
internal-api-segwaygo.segwayrobotics.com
api-segwaygo.segwayrobotics.com
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

urls=(http://robot-base-us.loomo.com
    http://robot-base.loomo.com
    http://nav-demo-mqtt.loomo.com
    http://nav-release-mqtt.loomo.com
    http://nav-internal-mqtt.loomo.com
    http://robot-base-alpha.loomo.com
    https://api-gate-alpha-delivery.loomo.com/
    https://api-gate-dev-delivery.loomo.com/
    https://api-gate-internal-delivery.loomo.com/
    https://api-gate-delivery.loomo.com/
    https://alpha-api-segwaygo.segwayrobotics.com/
    https://dev-api-segwaygo.segwayrobotics.com/
    https://internal-api-segwaygo.segwayrobotics.com/
    https://api-segwaygo.segwayrobotics.com/
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
