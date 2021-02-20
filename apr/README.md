# Jenkins 无侵入打包方案

## 1. 整体流程

1. 将脚本和工具发送到jenkins构建项目根目录
2. Docker+Jenkins打包
3. 打包后执行signapk签名
4. 检查配置的nginx、openresty、nexus仓库是否可以访问
5. 将apk发送到可以访问的仓库
6. wechat work 群机器人通知完成，显示可访问的仓库链接

## 2. 脚本说明

```shell
Makefile        // 调度
jenkins.sh      // 脚本总入口
env.sh          // 通用的一些变量

getip.sh        // 获取本机ip
getip_linux.sh
getip_macos.sh

head.sh         // 判断url是否可以访问
jenkins_builtin_env.sh  // 打印JENKINS内置变量
notify.sh       // 微信通知工具封装
remove_ip.sh    // set_ip的逆过程
set_ip.sh       // 将localhost替换成主机ip
send_form.sh    // cURL模拟表单上传文件到openresty服务器示例
send_nexus.sh   // cURL上传文件到nexus仓库示例
sign.sh         // apk签名示例
server_check.sh // 检查server是否可以访问
scan.sh         // 遍历指定扩展名文件存数组

trav_cp.sh      // 将文件复制到指定目录
trav_send.sh    // 将文件发送openresty
trav_nexus.sh   // 将文件发送nexus的raw仓库
trav_maven.sh   // 将文件发送nexus的maven-release仓库
trav_group.sh   // 将文件，四合一

wechat_build_finish.sh  // 企业微信机器人通知
```

## 3. 使用方法

1. `make push`
2. 在jenkins任务添加shell构建步骤，填入
`./jenkins.sh`


## 4. nexus OSS 上传

1. Raw repository

`curl -v -u admin:admin --upload-file $file $nexus_url/$dir/$(basename $file)`

2. Maven repository

```shell
curl -v -u admin:admin \
-F "maven2.version=1.0.1" \
-F "maven2.groupId=com.segway" \
-F "maven2.artifactId=delivery" \ 
-F "maven2.asset1=@jenkins.sh" \
-F "maven2.asset1.extension=apk" \
-F "maven2.asset1.classifier="unsigned"" \
"http://localhost:8081/service/rest/v1/components?repository=maven-releases"
```

详细参数参考
[Components API](https://help.sonatype.com/repomanager3/rest-and-integration-api/components-api?_ga=2.252588809.1278989473.1586491809-667887869.1586017412#ComponentsAPI-Raw)

## private 目录

private 下是未被git收录的隐私文件。
token是企业微信群机器人的token，
rk目录下是apk签名证书

```shell
$ tree
├── rk
│   ├── platform.pem
│   ├── platform.pk8
│   └── platform.x509.pem
└── token
```
