#!/bin/bash



. ./env.sh
nexus_url=http://localhost:8081/repository/rawrepo
dir=com/segway/robot/app/$BUILD_TAG/$version.$git_version


# 扫描当前目录下以及子目录下的apk文件，并发送到nexus仓库
getdir() {
    echo "--->$1"
    for file in $1/*; do
        if test -f $file; then
            # echo $file
            # arr=(${arr[*]} $file)

            if [ "${file##*.}"x = ${suffix}x ]; then
                echo "cp $file -> $dest"
                if [ ! -d "$dest"]; then
                    mkdir -p $dest
                fi
                cp $file $dest
                curl -v -u admin:admin --upload-file $file $nexus_url/$dir/`basename $file`
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
