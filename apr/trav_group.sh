#!/bin/bash



versionCode=`git rev-list HEAD --first-parent --count`
version=3.0.$versionCode
upload_url=http://192.168.1.68:8082/upload-jenkins
nexus_url=http://192.168.1.68:8081/repository/rawrepo
dir=com/segway/robot/app/$version/$BUILD_NUMBER
short_dir=$BUILD_TAG


# 扫描当前目录下以及子目录下的apk文件，并复制到当前目录
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
                curl -u file:file -F "file=@$file" $upload_url/$short_dir
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
