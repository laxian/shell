#!/usr/bin/env bash -x


curl -s https://ninebot.21tb.com/els/html/courseStudyItem/courseStudyItem.learn.do\?courseId\=COURSEID\&courseType\=NEW_COURSE_CENTER\&vb_server\=http%3A%2F%2F21tb-video.21tb.com \
-H 'Cookie: changId=99cea62183aee04f03bb469df380279d;domain=ninebot.21tb.com;path=/;  eln_session_id=elnSessionId.49fbc1b8171b47c7b30f23cdae9ef997;domain=ninebot.21tb.com;path=/;HTTPOnly;  corp_code=ninebot;domain=ninebot.21tb.com;path=/;  nxYongdaoIp=10.0.1.152;domain=ninebot.21tb.com;path=/;  ' \
| grep lexiangla | sed -e "s#.*\"\(.*\)\".*#\1#g"