#!/bin/bash

. ./env.sh
short_dir=$BUILD_TAG/$version.$git_version
upload_url=http://localhost:8082/upload-jenkins

. ./utils/scan.sh $1

for file in ${apk_array[@]}; do
    curl -u file:file -F "file=@$file" $upload_url/$short_dir
done
