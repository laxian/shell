#!/bin/bash

. ./env.sh
nexus_url=http://localhost:8081/service/rest/v1/components?repository=maven-releases
dir=com/segway/robot/app/$BUILD_TAG/$version.$git_version
groupId=com.segway
prefix=delivery
extension=apk
apk_raw_prefix=segway-delivery-

# 扫描当前目录下以及子目录下的apk文件，并发送到nexus仓库
getdir() {
    echo "--->$1"
    for file in $1/*; do
        if test -f $file; then
            if [ "${file##*.}"x = ${suffix}x ]; then
                name=`basename $file`
                classifier=`echo $name | awk -F "$apk_raw_prefix" '{print $NF}'`
                curl -v -u admin:admin -F "maven2.groupId=$groupId" -F "maven2.artifactId=$prefix" -F "maven2.version=$version" -F "maven2.asset1=@$file" -F "maven2.asset1.extension=$extension" -F "maven2.asset1.classifier="$classifier"" $nexus_url
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

# curl -v -u admin:admin -F "maven2.version=1.0.1" -F "maven2.groupId=com.segway" -F "maven2.artifactId=delivery" -F "maven2.asset1=@jenkins.sh" -F "maven2.asset1.extension=apk" -F "maven2.asset1.classifier="unsigned"" "http://localhost:8081/service/rest/v1/components?repository=maven-releases"
curl -v -u admin:admin -F maven2.groupId=com.segway -F maven2.artifactId=delivery maven2.version=3.0.88 -F maven2.asset1=@app/build/outputs/apk//alpha/segway-delivery-alpha.apk -F maven2.asset1.extension=apk -F maven2.asset1.classifier=alpha.apk 'http://localhost:8081/service/rest/v1/components?repository=maven-releases'
