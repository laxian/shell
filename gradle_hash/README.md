# GRADLE distributeUrl 下载加速脚本

> 无聊脚本，再也不想等gradle的..........................................

## 1. 什么是gradle wrapper

gradle wrapper为每一个gradle项目指定了一个gradle版本，并自动下载部署。
这样不同的项目就可以使用不同版本的gradle，而相互不影响。
特别地，对于CI构建项目十分友好。

## 2. gradle部署在哪里？

默认`$HOME/.gradle/wrapper/dists/`目录下。貌似正常人也不会改这个😂

```bash
➜  dists l
total 0
drwxr-xr-x  10 laxian  staff   320B  4 14 00:07 .
drwxr-xr-x   3 laxian  staff    96B  1 24 10:51 ..
drwxr-xr-x   3 laxian  staff    96B  3  9 22:16 gradle-4.1-all
drwxr-xr-x   3 laxian  staff    96B  4 12 23:45 gradle-5.2.1-bin
drwxr-xr-x   4 laxian  staff   128B  4 12 23:46 gradle-5.6.4-all
drwxr-xr-x   5 laxian  staff   160B  4 12 23:53 gradle-6.5-all
drwxr-xr-x   3 laxian  staff    96B  2 21 12:07 gradle-6.5-bin
drwxr-xr-x   3 laxian  staff    96B  4  3 11:48 gradle-6.7-all
drwxr-xr-x   3 laxian  staff    96B  4 13 23:35 gradle-7.0-all
drwxr-xr-x   3 laxian  staff    96B  4 14 00:07 gradle-7.0-bin
➜  dists pwd
/Users/laxian/.gradle/wrapper/dists
```

## 3. 怎么执行任务？

Android项目为我们做好了脚本，我们只需通过Android项目根目录的`gradlew/gradlew.bat`去执行gradle命令就可以。

eg: `./gradlew assembleDebug`

## gradle-wrapper.jar 是什么？

gradlew/gradlew.bat 是一个脚本，最终执行的任务的，是gradle-wrapper.jar，gradlew assemble，本质上是在执行：
`java -classpath gradle-wrapper.jar assemble`，当然还有一些附加参数省略了。
并且gradle-wrapper.jar检测到本地没有对应版本的gradle，会根据`gradle-wrapper.properties`配置的`distributionUrl`自动下载安装。

## gradle官方的distributionUrl下载缓慢怎么办？

- 1. 可以手动下载。但是安装是有规则的。看路径，有一层类似hash的目录，稍后说。

```bash
➜  dists l gradle-7.0-bin
total 0
drwxr-xr-x   3 laxian  staff    96B  4 14 00:07 .
drwxr-xr-x  10 laxian  staff   320B  4 14 00:07 ..
drwxr-xr-x   5 laxian  staff   160B  4 14 00:07 2p9ebqfz6ilrfozi676ogco7n
➜  dists l gradle-7.0-bin/2p9ebqfz6ilrfozi676ogco7n
total 0
drwxr-xr-x  5 laxian  staff   160B  4 14 00:07 .
drwxr-xr-x  3 laxian  staff    96B  4 14 00:07 ..
drwxr-xr-x  8 laxian  staff   256B  2  1  1980 gradle-7.0
-rw-r--r--  1 laxian  staff     0B  4 14 00:07 gradle-7.0-bin.zip.lck
-rw-r--r--  1 laxian  staff     0B  4 14 00:07 gradle-7.0-bin.zip.ok
```

- 2. 可以使用国内镜像

如：`https://mirrors.cloud.tencent.com/gradle`

## 下载容易，解压到哪里呢？如何避免gradle重复下载？

- 1. 使用file协议

将http地址改为
`distributionUrl=file\:///Users/laxian/Downloads/gradle-7.0-bin.zip`
借助gradle，自动部署。

缺点：前面提到的hash，和uri是对应的，不同的uri，会生成不同的hash。

- 2. 找到hash生成方法

hash是25位的，包含0-9a-z，一眼没看出是什么。
但是有两个方法可以生成。

1. 借助gradle，自动生成，然后取消gradle下载任务，复制自动生成的目录hash
2. gradle是开源的，看源码分析。
[getHash](https://github.com/gradle/gradle/blob/124712713a/subprojects/wrapper/src/main/java/org/gradle/wrapper/PathAssembler.java#L63)
找到规则，一切就好说了。

## hash规则

uri的md5，转byte[]，然后转36进制

## 脚本实现

hash.py 实现了hash生成。

main.sh 实现了获取gradle版本，镜像下载并部署的整个流程

## 使用方法

`./main.sh /path/to/android/project`

## REF

[github/gradle](https://github.com/gradle/gradle)
