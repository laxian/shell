#!/usr/bin/env bash

function readfile() {
  #这里`为esc下面的按键符号
  for file in $(ls $1); do
    #这里的-d表示是一个directory，即目录/子文件夹
    if [ -d $1"/"$file ]; then
      #如果子文件夹则递归
      echo "----"$1/$file
      readfile $1"/"$file
    else
      #否则就能够读取该文件的地址
      #      echo $1"/"$file
      #读取该文件的文件名，basename是提取文件名的关键字
      #    echo `dirname $file`
      echo $(basename $file)
      iconv -f gbk -t utf8 $1"/"$file >$1"/"new_$file
      mv $1"/"new_$file $1"/"$file
    fi
  done
}

readfile .
