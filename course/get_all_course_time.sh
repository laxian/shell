#!/usr/bin/env bash

for l in $(cat course_id); do
    cat get_time | sed -e "s#COURSEID#$l#g" >tmp.sh
    chmod +x tmp.sh
    time=`./tmp.sh`
    echo $l $time
done > $1
