#!/bin/bash

# ----------------------------
# https://www.codewars.com/kata/5667e8f4e3f572a8f2000039/solutions/shell
# ----------------------------

accum() {
    s=$(echo $1 | tr '[A-Z]' '[a-z]')
    for i in $(seq 1 ${#s}); do
        L=${s:$i-1:1}
        echo -n "$(capitalize $(multi $L $i))"
        if [ $i != ${#s} ]; then
            echo -n "-"
        fi
    done
}

multi() {
    for i in $(seq 1 $2); do
        echo -n $1
    done
}

capitalize() {
    echo $1 | sed -e "s/\b\(.\)/\u\1/g"
}

accum "$1"
