#!/bin/bash

#------------------------------------
# remove_ip <path>
# 在<path>目录下搜索本机ip，替换成localhost
#------------------------------------

subtext=localhost
workdir=$(
    cd $(dirname $0)
    pwd
)
ip=$($workdir/getip.sh)
echo $ip
sed -i s/${ip}/${subtext}/g $(grep ${ip} -rl $1)
