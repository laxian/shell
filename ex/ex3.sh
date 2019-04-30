#!/bin/bash

# 将一目录下所有的文件的扩展名改为bak

for file in `ls -a`
do
    if [ -f $file ]
    then
        echo $file
        mv $file ${file%%.*}.bak
    fi
done

