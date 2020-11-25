#!/usr/bin/env bash

# ----------------------------
# 删除当前目录下的文件夹和zip压缩包
# ----------------------------

for file in $(ls); do
    if [[ -d "$file" && $file != "private" ]]; then
        rm -rf $file
    elif [[ $file =~ .zip$ ]]; then
        rm $file
    fi
done
