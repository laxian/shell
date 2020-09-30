#!/usr/bin/env bash

function count_down() {
    i=$1
    while test $i -ge 0; do
        sleep 1
        echo -ne "倒计时：$((i--))\r"
    done
}
