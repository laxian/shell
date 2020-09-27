#!/usr/bin/env bash

#----------------------------------------------------------------
# 获取课程时长，只取整数部分
#----------------------------------------------------------------

curl -s 'https://ninebot.21tb.com/els/html/course/course.getCourseDetail.do'\
 -H 'Host: ninebot.21tb.com' \
 -H 'Accept: */*' \
 -H 'X-Requested-With: XMLHttpRequest' \
 -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36' \
 -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
 -H 'Origin: https://ninebot.21tb.com' \
 -H 'Sec-Fetch-Site: same-origin' \
 -H 'Sec-Fetch-Mode: cors' \
 -H 'Sec-Fetch-Dest: empty' \
 -H 'Referer: https://ninebot.21tb.com/els/html/courseStudyItem/courseStudyItem.learn.do?courseId=COURSEID&courseType=NEW_COURSE_CENTER&vb_server=http%3A%2F%2F21tb-video.21tb.com' \
 -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
 -H 'Cookie: YOUR_COOKIE' \
 --data-binary "courseId=COURSEID&courseType=NEW_COURSE_CENTER" \
 --compressed \
 | sed -e 's/.*minStudyTime\":\([0-9]\+\).*/\1\n/g'