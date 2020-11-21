#!/usr/bin/env bash -x

path=$1
cmd=$2
ext=$3

workdir=$(
    cd $(dirname $0)
    pwd
)

sub() {
    echo $1
    arr=(${1//,/ })
    old=${arr[0]}
    new=${arr[1]}
    echo $old == $new
    $workdir/sub.sh $old $new $path $ext
}

res() {
    echo $1
    arr=(${1//,/ })
    old=${arr[0]}
    new=${arr[1]}
    echo $old == $new
    $workdir/sub.sh $new $old $path $ext
}

if [ $cmd = "sub" ]; then
    for l in $(cat $path/private/sub); do
    sub $l
    done
elif [ $cmd = "res" ]; then
    for l in $(cat $path/private/sub); do
    res $l
    done
else
    echo error cmd $cmd
fi
