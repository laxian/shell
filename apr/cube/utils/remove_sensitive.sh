#!/usr/bin/env bash -x


sub() {
    echo $1
    arr=(${1//,/ })
    old=${arr[0]}
    new=${arr[1]}
    echo $old == $new
    ./sub.sh $old $new ../env/
}

res() {
    echo $1
    arr=(${1//,/ })
    old=${arr[0]}
    new=${arr[1]}
    echo $old == $new
    ./sub.sh $new $old ../env/
}

if [ $1 = "sub" ]; then
    for l in $(cat ../private/sub); do
    sub $l
    done
elif [ $1 = "res" ]; then
    for l in $(cat ../private/sub); do
    res $l
    done
else
    echo error cmd $1
fi
