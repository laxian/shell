#!/usr/bin/env bash

#----------------------------------------------------------------
# 根据courseId/时长(分钟)，将url模板里替换为真实的courseId，并打开浏览器，
# 然后脚本sleep，sleep时长为课程时长多60秒
#----------------------------------------------------------------

source ./countdown.sh
for l in $(cat course_id_time); do
    ./query_learned.sh
    id=$(echo $l | cut -d':' -f 1)
    time=$(echo $l | cut -d':' -f 2)
    url=$(cat course_url | sed -e "s#COURSEID#$id#g")
    echo 课程id: $id
    echo 最低时长: $time
    echo 地址: $url
    learned_time=$(./get_course_learned_time.sh $url)
    learned_time=${learned_time:="0"}
    
    echo $learned_time
    remain_time=$(($time-$learned_time))
    echo "课程时长: $time. 已学:$learned_time, 剩余：$remain_time"
    if [[ $remain_time != 0 ]]; then
        python -mwebbrowser $url
        count_down $(($remain_time * 60 + 60))
    fi
    
    echo "next course is coming"
done