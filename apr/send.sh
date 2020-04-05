#!/bin/bash

# curl 模拟表单上传文件
curl -u file:file -F "filename=@$1" http://localhost:81/upload-jenkins/jenkins
curl -u file:file -F "filename=@$1" http://localhost:81/upload-jenkins/jenkins
