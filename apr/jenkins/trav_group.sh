#!/bin/bash

. ./env.sh
dir=com/segway/robot/app/$BUILD_TAG/$version.$git_version
short_dir=$BUILD_TAG/$version.$git_version
upload_url=http://localhost:8082/upload-jenkins
nexus_url=http://localhost:8081/repository/rawrepo
maven_url=http://localhost:8081/service/rest/v1/components?repository=maven-releases

# maven params
groupId=com.segway
prefix=delivery
extension=apk
apk_raw_prefix=segway-delivery-

. ./server_check.sh

# 扫描当前目录下以及子目录下的apk文件，复制到指定目录，然后发送到指定服务器
. ./utils/scan.sh $1
dest=${2-.}

for file in ${apk_array[@]}; do

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
        curl -v -u admin:admin -F "maven2.groupId=$groupId" -F "maven2.artifactId=$prefix" -F "maven2.version=$version" -F "maven2.asset1=@$file" -F "maven2.asset1.extension=$extension" -F "maven2.asset1.classifier="$classifier"" $maven_url
    fi

done
