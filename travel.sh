#!/bin/bash

# 扫描当前目录下以及子目录下的apk文件，并复制到当前目录
function getdir(){
  echo ++++$1
  for file in $1/*
  do
    if test -f $file
    then
      # echo $file
      arr=(${arr[*]} $file)

      if [ "${file##*.}"x = "apk"x ];then
        echo "found" $file
        cp $file .
      fi
    else
      getdir $file
    fi
  done

}
getdir .
# echo  ${arr[@]}
