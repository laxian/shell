#!/usr/bin/env bash

# ----------------------------
# Move to AndroidX
# 按照官方要求，先将android support library 版本升级至28
# 将类映射，一一替换
# 将依赖映射，一一替换
# 由于对每一行替换，都进行了一次文件搜索，运行效率较低，暂不打算优化
# ----------------------------

WORKSPACE=/Users/admin/Work/app-apr-cabinet/GxCabinetApp

sub() {
    arr=(${1//,/ })
    old=${arr[0]}
    new=${arr[1]}
    echo $old == $new
    ../utils/sub.sh $old $new $WORKSPACE gradle
}

for l in $(cat ./artifacts_mapping.csv); do
    sub $l
done

for l in $(cat ./classes_mapping.csv); do
    sub $l
done
