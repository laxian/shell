# 半自动刷课程脚本

1. 进入列表页，xpath提取courseId，抓取cookie

2. 执行get_all_course_time.sh，获取每个courseId对应的时长

3. 执行schedule.sh，自动打开浏览器，并各那句可的时长，定时打开下一个课程