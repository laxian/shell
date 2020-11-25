#!/bin/bash

# ----------------------------
# https://www.codewars.com/kata/56e3cd1d93c3d940e50006a4/solutions/shell
# How Green Is My Valley
# ----------------------------

makevalley() {
    sorted=($(echo "$1" | xargs -n1 | sort -n -r))
    n=${#sorted[@]}
    for i in $(seq 1 $n); do
        item=${sorted[$i - 1]}
        if [ ${#l[@]} == ${#r[@]} ]; then
            l+=($item)
        else
            r+=($item)
        fi
    done
    echo "${l[@]} $(echo ${r[@]} | xargs -n1 | sort -n | tr '\n' ' ')"
}
makevalley "$1"
