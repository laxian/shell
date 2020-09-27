#!/usr/bin/env bash

curl -s http://ninebot.21tb.com/els/html/specialSubject/specialSubject.loadSpecialSubjectDetail.do\?subjectId\=0179358716e1457795370d218dc782c0\&courseType\=NEW_COURSE_CENTER \
    -H 'Cookie: YOUR_COOKIE' \
|  grep ":;\" data-id=\"[0-9a-f]\+" \
| sed -e "s#.*\"\(.*\)\".*#\1#g" > course_id