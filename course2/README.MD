# 半自动刷课程脚本

## 使用

1. 提前保存好cookie，和course_id(已有，如果一样，可以直接用)

2. `./load_course_info.sh <username> <password>`下载客人课程列表

2. 执行`./schedule.sh`开始任务

## 思路

1. 手动进入课列表页，xpath提取courseId，存入course_id文件

2. 抓取cookie，存入cookie文件

3. 循环请求获取每个courseId对应的时长，id和时长键值对输出到`course_id_time`

4. 执行schedule.sh，自动打开浏览器，并根据课的时长，定时打开下一个课程

## 查询已学时长

`./query_learned.sh`

## 注意

- Mac上Safari不可用，课程打开不计时；Chrome打开页面即开始计时，无需登录乐享
- 没找到查询已学时长的接口，学过的课程id，会自动跳过
- 网页抓取courseId，我用的xpath-helper chrome扩展，后改为curl+sed抓取
- 抓包Charles/开发者工具