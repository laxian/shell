#!/usr/bin/env bash

#----------------------------------------------------------------
# 根据courseId/时长(分钟)，将url模板里替换为真实的courseId，并打开浏览器，
# 然后脚本sleep，sleep时长为课程时长多60秒
#----------------------------------------------------------------

source ./countdown.sh
for l in $(cat course_id_time); do
    id=$(echo $l | cut -d':' -f 1)
    course_id=$(echo $l | cut -d':' -f 2)
    learned_time=$(echo $l | cut -d':' -f 3)
    duration=$(echo $l | cut -d':' -f 4)
    url=$(cat course_url | sed -e "s#CLASSID#$id#g")
    echo class id: $id
    echo 时长: $learned_time/$duration
    remain_time=$(($duration - $learned_time))
    echo "剩余：$remain_time"
    echo 地址: $url
    echo "class id $id"
    echo "course id $course_id"
    if [[ $remain_time -gt 0 ]]; then
        python -mwebbrowser $url
        # count_down $remain_time
        while test $remain_time -ge 0; do
            sleep 1
            echo -ne "倒计时：$((remain_time--))\r"
            # mod=`echo $remain_time % 30 | bc`
            # learned_time=$(($duration-$remain_time))
            # echo -ne "实时已学：$learned_time; $mod 后上传\r"
            # if [[ $mod == 0 ]] ; then
            #     tmp=`mktemp`
            #     chmod +x $tmp
            #     ts=`date +%s%8`
            #     uuid=$(md5 -s `date +%s%8` | cut -d' ' -f4)
            #     cat study.sh | sed -e "s#CLASSID#$id#g" -e "s#COURSEID#$course_id#g" \
            #     -e "s#LEARN_TIME#$learned_time#g" -e "s#IS_ENDED#false#g" \
            #     > $tmp
            #     response=`$tmp`

            #     cat code_rp.sh | sed -e "s#CLASSID#$id#g" -e "s#COURSEID#$course_id#g" \
            #     -e "s#LEARN_TIME#$learned_time#g" -e "s#IS_ENDED#false#g" \
            #     -e "s#{TIMESTAMP}#$ts#g" -e "s#{UUID}#$uuid#g" \
            #     > $tmp
            #     response=`$tmp`
            # fi
        done
    fi
    echo "next course is coming"
done
