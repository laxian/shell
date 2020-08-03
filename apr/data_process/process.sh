#!/usr/bin/env bash

# ----------------------------
# 处理格式化数据，显示第一第四列，第一列加上引号
# ----------------------------

script_dir=$( cd "$( dirname "$0"  )" && pwd )
# script_name=$(basename ${0})

while read line; do
    echo $line | awk '{print "\""$1"\"" ":" $4 ","}'
done < ${script_dir}/codes.txt >output.txt
