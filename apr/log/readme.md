# 快速上传并拉日志

### 上传
`upload_log.sh <robot_id> <path>`

远程上传日志，须指定完整robot_id 和文件准确路径

### 拉取
`query_log.sh <robot_id_key_word> <index>`

robot_id_key_word是指robot_id可以输入一部分，用于过滤
index是指日志列表的index，可不传，默认是第一个，也就是index=0