#!/usr/bin/env bash

curl -s http://ninebot.21tb.com/els/html/specialSubject/specialSubject.loadSpecialSubjectDetail.do\?subjectId\=0179358716e1457795370d218dc782c0\&courseType\=NEW_COURSE_CENTER \
    -H 'Cookie: corp_code=ninebot; nxYongdaoIp=10.0.1.152; href=http%3A%2F%2Fninebot.21tb.com%2Fels%2Fhtml%2Findex.parser.do%3Fid%3DNEW_COURSE_CENTER%26current_app_id%3D8a80810f5ab29060015ad1906d0b3811; accessId=f05eae40-9a31-11e5-83f6-57006c315d67; bad_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c01-00a3-11eb-aea2-1f1941c69e04; nice_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c02-00a3-11eb-aea2-1f1941c69e04; qimo_seosource_f05eae40-9a31-11e5-83f6-57006c315d67=%E7%AB%99%E5%86%85; qimo_seokeywords_f05eae40-9a31-11e5-83f6-57006c315d67=; changId=24b607e92a8bd889a3a478e548cf7d91; eln_session_id=elnSessionId.f6e5ff7b82874997b3acc096042508f3; pageViewNum=9' \
|  grep ":;\" data-id=\"[0-9a-f]\+" \
| sed -e "s#.*\"\(.*\)\".*#\1#g" > course_id