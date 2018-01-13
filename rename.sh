#!/bin/bash

for file in `ls`
do
    if test -f $file
    then
        pre=`echo $file | cut -c1-4`
        if test $pre = $1; then
            mv $file v3_$file
        else
            echo ----
        fi
    fi
done