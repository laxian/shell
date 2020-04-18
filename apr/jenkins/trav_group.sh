#!/bin/bash

. ./env.sh
dir=com/segway/robot/app/$BUILD_TAG/$version.$git_version
short_dir=$BUILD_TAG/$version.$git_version
upload_url=http://localhost:8082/upload-jenkins
nexus_url=http://localhost:8081/repository/rawrepo

# maven params
nexus_url=http://localhost:8081/service/rest/v1/components?repository=maven-releases
groupId=com.segway
prefix=delivery
extension=apk
apk_raw_prefix=segway-delivery-

. ./server_check.sh
# 扫描当前目录下以及子目录下的apk文件，复制到指定目录，然后发送到指定服务器
getdir() {
    echo "--->$1"
    for file in $1/*; do
        if test -f $file; then
            # echo $file
            # arr=(${arr[*]} $file)

            if [ "${file##*.}"x = ${suffix}x ]; then
                echo "cp $file -> $dest"

                # move to nginx share folder
                if [ $nginx ]; then
                    if [ ! -d "$dest" ]; then
                        mkdir -p $dest
                    fi
                    cp $file $dest
                fi

                # upload openresty server
                if [ $resty ]; then
                    curl -u file:file -F "file=@$file" $upload_url/$short_dir
                fi

                # upload nexus raw repo
                if [ $nexus ]; then
                    curl -v -u admin:admin --upload-file $file $nexus_url/$dir/$(basename $file)
                fi

                # upload maven repo
                if [ $maven ]; then
                    name=$(basename $file)
                    classifier=$(echo $name | awk -F "$apk_raw_prefix" '{print $NF}')
                    curl -v -u admin:admin -F "maven2.groupId=$groupId" -F "maven2.artifactId=$prefix" -F "maven2.version=$version" -F "maven2.asset1=@$file" -F "maven2.asset1.extension=$extension" -F "maven2.asset1.classifier="$classifier"" $nexus_url
                fi

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
