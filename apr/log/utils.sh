#!/usr/bin/env bash

# 下载文件
# $1 url, not null
# $2 output_name, optional. If empty, use URL file name
download() {
    if [ $# -eq 1 ]; then
        curl -LO $1
    elif [ $# -eq 2 ]; then
        curl -L $1 -o $2
    fi
}

unzip_to_dir() {
    unzip $1 -d $2
}