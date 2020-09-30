#!/usr/bin/env bash


for l in $(cat course_id);do
    echo -n $l:
    ./lx_time.sh $l
done > course_id_time3