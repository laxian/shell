#!/usr/bin/env bash

# ----------------------------
# https://www.codewars.com/kata/515decfd9dcfc23bb6000006/train/shell
# For a given string s find the character c (or C) with longest consecutive repetition and return:
# ----------------------------

isValidIp() {
    adr=$1
    OLD_IFS=$IFS
    IFS='.'
    seg=0
    for i in $adr; do
        echo $i | grep "^[1-9][0-9]*" > /dev/null || continue
        if [ $i -lt 0 -o $i -gt 255 ]; then
            echo False
            return
        fi
        let seg++
    done
    IFS=$OLD_IFS
    if [ $seg -lt 4 ]; then
        echo False
    else
        echo True
    fi
}

isValidIp $1