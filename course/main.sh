#!/usr/bin/env bash

# ----------------------------
# 自动刷课入口
# 1. 设置cookie
# 2. 获取课时长
# 3. 开始定时任务
# ----------------------------

# ./login.sh $1 $2

./setup_cookie.sh

./get_all_course_time.sh course_id_time

./schedule.sh