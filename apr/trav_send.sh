#!/bin/bash

upload_url=http://localhost:81/upload-summary
dir=hello4


# 扫描当前目录下以及子目录下的apk文件，并上传到$upload_url/$dir
getdir() {
    echo "--->$1"
    for file in $1/*; do
        if test -f $file; then
            # echo $file
            # arr=(${arr[*]} $file)

            if [ "${file##*.}"x = ${suffix}x ]; then
                # echo "cp $file -> $dest"
                curl -u file:file -F "file=@$file" $upload_url/$dir
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
