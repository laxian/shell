#!/bin/bash

. ./scan.sh $1
dest=${2-.}

for file in ${apk_array[@]}; do
    if [ ! -d "$dest" ]; then
        mkdir -p $dest
    fi
    cp $file $dest
done

cp2share $1 $2
