#!/usr/bin/env bash

# ----------------------------
# 快速下载日志
# $1 robot id 关键字过滤
# $2 指定拉取第$2行，默认0
# ----------------------------

pwd=$( cd "$( dirname "$0"  )" && pwd )
$pwd/query_log_url.sh $@ | xargs -I URL curl -LO URL
