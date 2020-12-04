# 快速上传并拉日志

### 上传
`upload_log.sh <robot_id> <path>`

远程上传日志，须指定完整robot_id 和文件准确路径

### 一键上传并轮询下载，解压并vscode打开
`./auto_get.sh <robot_id> <path>`

上传和下载是异步过程，上传后，等待上传完成后才出现在列表并提供下载，
所以，上传成功后，根据url上的时间，判断最新url是否是上传成功后的url，
条件满足后下载，解压到download，vscode打开

### 拉取
`query_log.sh <robot_id_key_word> <index>`

### 查询url
`query_log_url.sh <robot_id_key_word> <index>`

robot_id_key_word是指robot_id可以输入一部分，用于过滤
index是指日志列表的index，可不传，默认是第一个，也就是index=0

### login过期自动刷新token
`login.sh`

链式调用，自动读取旧token，获取新token，全面替换成新token