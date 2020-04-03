#!/bin/bash


# 扫描当前目录下以及子目录下的apk文件，并复制到当前目录
getdir() {
    echo "--->$1"
    for file in $1/*; do
        if test -f $file; then
            # echo $file
            # arr=(${arr[*]} $file)

            if [ "${file##*.}"x = ${suffix}x ]; then
                echo "cp $file -> $dest"
                cp $file $dest
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

cp2share $1 $2
