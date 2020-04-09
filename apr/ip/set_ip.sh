#!/bin/bash -e

#------------------------------------
# set_ip <path>
# 在<path>目录下搜索localhost，替换成本机ip
#------------------------------------

subtext=localhost

workdir=$(
    cd $(dirname $0)
    pwd
)
ip=$($workdir/getip.sh)
echo $ip
sed -i s/${subtext}/${ip}/g $(grep ${subtext} -rl $1)
