#!/usr/bin/env bash -x

#----------------------------------------------------------------
# login，更新本地token
#----------------------------------------------------------------

new_token
tmp=`mktemp`
# 读取旧token
# 模拟登陆
# 过滤token行
# 匹配出token
# 写入缓存，等待1s，IO是异步的，否则读取有可能为空
# 递归搜索当前目录下有旧token的文件
# 替换旧token
old_token=`cat ./private/sub| sed -n '/token/p' | awk -F"," '{print $1}'`
curl -s 'http://${host_part_1}-api.${host_part_2}.com/user/login' \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Origin: http://${host_part_1}.${host_part_2}.com' \
  -H 'Referer: http://${host_part_1}.${host_part_2}.com/' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  --data-binary "{\"username\":\"${username}\",\"password\":\"${password}\"}" \
  --compressed \
  --insecure \
  | sed -n '/token/p' \
  | sed 's/.*token":"\(.*\)",/\1/g' \
  | tee \
  > $tmp 

# 这里如果不打破链式调用，文件写入不刷新，cat $tmp 获取不到值
grep $old_token -rl . \
| xargs -n 1 -I F sed -i "s/$old_token/`cat $tmp`/g" F
#   | sed 's/,//g ; s/"token":"\(.*\)"/\1/' \