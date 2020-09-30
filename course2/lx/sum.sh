#!/usr/bin/env bash


sum=0
for l in $(cat course_id_time3); do
    learned_time=$(echo $l | cut -d':' -f 3)
    duration=$(echo $l | cut -d':' -f 4)
    # echo "$learned_time" $duration
    result=0
    if [[ $learned_time -gt $duration ]]; then
        result=$duration
    else
        result=$learned_time
    fi
    echo "$result"
    sum=$(($sum+$result))
    echo $sum
done


