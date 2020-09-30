
cat urls| sed -e "s#.*classes/\([0-9a-f]\+\).*#\1#g" > course_id