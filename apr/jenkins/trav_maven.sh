#!/bin/bash

. ./env.sh
nexus_url=http://localhost:8081/service/rest/v1/components?repository=maven-releases
dir=com/segway/robot/app/$BUILD_TAG/$version.$git_version
groupId=com.segway
prefix=delivery
extension=apk
apk_raw_prefix=segway-delivery-

. ./utils/scan.sh $1

for file in ${apk_array[@]}; do

    name=$(basename $file)
    classifier=$(echo $name | awk -F "$apk_raw_prefix" '{print $NF}')
    curl -v -u admin:admin -F "maven2.groupId=$groupId" -F "maven2.artifactId=$prefix" -F "maven2.version=$version" -F "maven2.asset1=@$file" -F "maven2.asset1.extension=$extension" -F "maven2.asset1.classifier="$classifier"" $nexus_url

done
