#!/usr/bin/env bash -x

id=$1
path=$2
# success_words="指令下发成功并已收到！"
success_codes="9000"

./clean.sh
result=`./upload_log.sh $id $path | grep $success_codes`

if [[ -n $result ]]; then
    time_tag=$(date +"%Y-%m-%d_%H-%M")
    until [[ $new_url =~ $time_tag ]];
    do
        sleep 1
        new_url=$(./query_log_url.sh $id)
    done
    curl -LO $new_url
    file_name=${new_url##*/}
    mv $file_name ~/Downloads
    cd ~/Downloads
    dir=$id$time_tag
    unzip $file_name -d $dir
    code $dir
    echo enjoy!!!

else
    echo request failed.
fi

