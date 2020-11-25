#!/usr/bin/env bash

isMain() {
    invoke_name=$(basename $0)
    if [ $invoke_name = $script_name ]; then
        return 0
    else
        return 1
    fi
}

function count_down() {
    i=$1
    while test $i -ge 0; do
        sleep 1
    echo -ne "                 \r"
    echo -ne "剩余时间: $((i--))\r"
    done
}

if isMain; then
    count_down $1
fi