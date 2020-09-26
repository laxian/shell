#!/usr/bin/env bash

for l in `cat course_id_time`;do
    echo "$l"
    id=`echo $l | cut -d':' -f 1`
    time=`echo $l | cut -d':' -f 2`
    echo $id
    echo $time
    url=`cat course_url | sed -e "s#COURSEID#$id#g"`
    echo $url
    python -mwebbrowser $url
    sleep $(($time*60+10))
    echo "next course is coming"
done