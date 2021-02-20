#!/usr/bin/env bash

#-------
# 自动复制cli命令到setup.py
#-------

workdir=$(
    cd $(dirname $0)
    pwd
)

funcs=`cat $workdir/../src/log/cli.py| grep Commands -A 100 | grep segway_ | awk -F' ' '{print $1}' | xargs -I NAME echo "\"NAME=src.log.cli:NAME"`
a=$funcs
echo $funcs
sed -i "/segway_/d" $workdir/../setup.py

for l in $funcs;do
    echo $l
    sed -i "/console_scripts/a \
    \\\t\t\t$l\"," $workdir/../setup.py
done


