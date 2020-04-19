#!/bin/bash

. ./env.sh
nexus_url=http://localhost:8081/repository/rawrepo
dir=com/segway/robot/app/$BUILD_TAG/$version.$git_version

. ./utils/scan.sh $1

for file in ${apk_array[@]}; do
    curl -v -u admin:admin --upload-file $file $nexus_url/$dir/$(basename $file)
done
