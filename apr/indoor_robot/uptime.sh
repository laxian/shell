#!/bin/bash

# --------------------------------
# 读取日志文件名，获取开始时间
# 读取改日志文件最后一行，获取结束时间
# --------------------------------

for f in $(ls 2022*); do
	echo $f | sed 's/_[0-9]\+$//g;s/2022-//'
	end_time=`tail -n1 $f | awk '{time=$1"-"$2;print time}' | sed 's/.[0-9]\+$//'`
	echo $end_time 
	echo "--"
done > time
