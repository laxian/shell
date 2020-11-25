#!/bin/bash

#----------------------------
# https://www.codewars.com/kata/5700c9acc1555755be00027e/shell
#----------------------------

containAllRots() {
    rots=$(get_rots $1)
    for item in $rots; do
        # echo "$item"
        if [[ $(contains $item "$2") != 0 ]]; then
            echo "false"
            return 1
        fi
    done
    echo "true"
    return 0
}

get_rots() {
    len=${#1}
    input=$1
    list=$1
    # echo $1
    for ((i = 0; i < len - 1; i++)); do
        # echo "$i"
        rot1=${input:((len - 1)):1}${input:0:((len - 1))}
        # echo $rot1
        input=$rot1
        list="$list $input"
    done
    echo $list
}

contains() {
    strA=$1
    strB="$2"
    if [[ $strB =~ $strA ]]; then
        echo 0
    else
        echo 1
    fi
}

containAllRots $1 "$2"
