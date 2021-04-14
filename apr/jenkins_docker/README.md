# Jenkins in docker 参数化构建方案

## 方案简介

1. docker 快速部署
2. 参数化打包
3. 构建结果存档web服务器
4. 企业微信通知
5. 远程出发构建，结合postman，高效打包

## docker部署

基于jenkins官方镜像作为底包，通过dockerfile构建的镜像:[docker-jenkins](https://github.com/laxian/dockerfiles/tree/master/docker-jenkins-android)

## Jenkins参数化构建

1. [参数化构建](https://plugins.jenkins.io/build-with-parameters/)

2. [Remote Access Api](https://www.jenkins.io/doc/book/using/remote-access-api/)

结合Jenkins提供的参数化能力，可以动态的提供参数，实现灵活的打包需求。

参数化打包页面：
![20210220141532](https://raw.githubusercontent.com/laxian/picgo-picbed/main/images/20210220141532.png)

部分参数配置截图：
![20210220141727](https://raw.githubusercontent.com/laxian/picgo-picbed/main/images/20210220141727.png)

Postman触发截图：
![20210220141818](https://raw.githubusercontent.com/laxian/picgo-picbed/main/images/20210220141818.png)

## curl触发

1. oneliner

    ```shell
    curl http://admin:11b114575809164aebae456cbc855af368@10.10.80.25:8002/job/app-apr-food-delivery-debug/buildWithParameters\?br\=origin/release
    ```

2. multiliner

    ```shell
    curl http://10.10.80.25:8002/job/app-apr-food-delivery-debug/buildWithParameters \
    --user admin:11b114575809164aebae456cbc855af368 \
    --data br=origin/release
    ```

### Postman 触发

导入curl：Import -> Raw text -> Ctrl+V
