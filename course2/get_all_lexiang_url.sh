#!/usr/bin/env bash -x

#----------------------------------------------------------------
# 批量获取课程时长，并保存id和时长键值对，':'分割
#----------------------------------------------------------------

tmp=`mktemp`
for l in $(cat course_id); do
    cat get_lexiang_url.sh | sed -e "s#COURSEID#$l#g" >$tmp
    chmod +x $tmp
    time=`$tmp`
    echo $l:$time
done > $1
