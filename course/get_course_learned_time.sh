#!/usr/bin/env bash -x

#----------------------------
# 获取页面内已学时长元素值
#----------------------------

curl -s $1  \
-H 'Cookie: JSESSIONID=67798F3B641CE30EF72668700BB0022C; corp_code=ninebot; nxYongdaoIp=10.0.1.152; qimo_seosource_f05eae40-9a31-11e5-83f6-57006c315d67=%E7%AB%99%E5%86%85; qimo_seokeywords_f05eae40-9a31-11e5-83f6-57006c315d67=; href=http%3A%2F%2Fninebot.21tb.com%2Fels%2Fhtml%2Findex.parser.do%3Fid%3DNEW_COURSE_CENTER%26current_app_id%3D8a80810f5ab29060015ad1906d0b3811; accessId=f05eae40-9a31-11e5-83f6-57006c315d67; bad_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c01-00a3-11eb-aea2-1f1941c69e04; nice_idf05eae40-9a31-11e5-83f6-57006c315d67=0f4f0c02-00a3-11eb-aea2-1f1941c69e04; pageViewNum=4; changId=b457090884e0ee1a4c1d9a29613004a3; eln_session_id=elnSessionId.240bbe6f7cf84d3aaf13e0e19d8c1f10' \
| grep "studiedTime = " | sed -e "s#.*studiedTime = \([0-9]\+\).*#\1#g"