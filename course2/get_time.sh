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
 -H 'Cookie: corp_code=ninebot; nxYongdaoIp=10.0.1.152; href=http%3A%2F%2Fninebot.21tb.com%2Fels%2Fhtml%2Findex.parser.do%3Fid%3DNEW_COURSE_CENTER%26current_app_id%3D8a80810f5ab29060015ad1906d0b3811; accessId=f05eae40-9a31-11e5-83f6-57006c315d67; bad_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c01-00a3-11eb-aea2-1f1941c69e04; nice_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c02-00a3-11eb-aea2-1f1941c69e04; qimo_seosource_f05eae40-9a31-11e5-83f6-57006c315d67=%E7%AB%99%E5%86%85; qimo_seokeywords_f05eae40-9a31-11e5-83f6-57006c315d67=; changId=24b607e92a8bd889a3a478e548cf7d91; eln_session_id=elnSessionId.f6e5ff7b82874997b3acc096042508f3; pageViewNum=9' \
 --data-binary "courseId=COURSEID&courseType=NEW_COURSE_CENTER" \
 --compressed \
 | sed -e 's/.*minStudyTime\":\([0-9]\+\).*/\1\n/g'