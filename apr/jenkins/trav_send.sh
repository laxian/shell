#!/bin/bash

. ./env.sh
short_dir=$BUILD_TAG/$version.$git_version
upload_url=http://localhost:8082/upload-jenkins

# 扫描当前目录下以及子目录下的apk文件，并上传到nexus服务器
getdir() {
    echo "--->$1"
    for file in $1/*; do
        if test -f $file; then
            if [ "${file##*.}"x = ${suffix}x ]; then
                # echo "cp $file -> $dest"
                curl -u file:file -F "file=@$file" $upload_url/$short_dir
            fi
        elif [ -d $file ]; then
            getdir $file
        fi
    done
}

cp2share() {
    dest=${2-.}
    suffix=${3-"apk"}
    echo $suffix
    getdir $1
}

# 对$1目录扫码到的所有apk文件，执行$2
cp2share $1 $2
