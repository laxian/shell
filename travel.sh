#!/bin/bash

#--------------
# 递归扫描$1下文件
# 将结果复制到$2，默认当前目录
# $3过滤扩展名，默认apk
#--------------

dest=${2-.}
suffix=${3-"apk"}
echo $suffix

# 扫描当前目录下以及子目录下的apk文件，并复制到当前目录
function getdir() {
  echo "--->$1"
  for file in $1/*; do
    if test -f $file; then
      # echo $file
      arr=(${arr[*]} $file)

      if [ "${file##*.}"x = ${suffix}x ]; then
        echo "cp $file -> $dest"
        cp $file $dest
      fi
    elif [ -d $file ]; then
      getdir $file
    fi
  done
}

getdir $1
# echo  ${arr[@]}
