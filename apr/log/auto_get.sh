#!/usr/bin/env bash

if [ $# -ne 2 ]; then
    cat <<-EOF
		Usage: ./auto_get.sh <id> <path>
	EOF
    exit 1
fi


# id 需要被子shell使用
export id=$1
path=$2
# success_words="指令下发成功并已收到！"
SUCCESS_CODES="9000"
# 轮询日志url的最大次数
POLL_LIMIT=120

pwd=$( cd "$( dirname "$0"  )" && pwd )
$pwd/clean.sh
json=`./upload_log.sh $id $path`
result=`echo $json| grep $SUCCESS_CODES`

if [[ -n $result ]]; then
    # 上传成功后，以当前时间时间戳为准，轮询当前id下最新日志url，如果url最新包含该时间戳，则认为是
    # 本次上传的日志。理论上此本地时间戳和网络时间戳可能以一秒之差分布在两分钟。实际使用中
    # 尚未遇到，不考虑此情况
    # 循环获取url，如果时间戳不一致，1秒后再次获取。累计达到一定次数，停止轮询
    cnt=1
    time_tag=$(date +"%Y-%m-%d_%H-%M")
    until [[ $new_url =~ $time_tag ]];
    do
        if [ $cnt -gt $POLL_LIMIT ]; then
            echo "POLL_LIMIT exceeded!"
            exit 1
        fi
        
        sleep 1
        new_url=$(./query_log_url.sh $id)
        # 次数计数器，防止过多查询
        let cnt++
    done
    $pwd/fetch_and_open.sh $new_url
else
    echo request failed.
    echo $json
fi

