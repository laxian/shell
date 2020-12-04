# 快速上传并拉日志

### 一键上传-下载-打开
`./auto_get.sh <robot_id> <path>`

### 上传
`upload_log.sh <robot_id> <path>`

远程上传日志，须指定完整robot_id 和文件准确路径

上传和下载是异步过程，上传后，等待上传完成后才出现在列表并提供下载，
所以，上传成功后，根据url上的时间，判断最新url是否是上传成功后的url，
条件满足后下载，解压到download，vscode打开

### 查询url
`query_log_url.sh <robot_id_key_word> <index>`

只查询，指定id或部分id；index表示显示列表的第几个，默认0

### 拉取并打开
`fetch_and_open.sh <url>`
如果已知url，一键下载并打开

### login过期自动刷新token
`login.sh`

链式调用，自动读取旧token，获取新token，全面替换成新token