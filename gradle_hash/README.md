# Gradle Wrapper 下载加速脚本

> 无聊脚本，再也不想等gradle的......................................................

## 0. 这是什么？

> 这不是加速gradle里的依赖包下载的工具。

这是加速下载gradle的加速脚本。

eg: `gradle-x.x-all.zip`

## 1. 什么是gradle wrapper?

gradle是一个开源的，项目构建工具。gradle wrapper可以为每一个项目自动地部署一个gradle版本。
这样，当运行一个新项目时，不用关心当前主机是否有gradle，一切由项目自带的gradle wrapper自动管理。
对于CI服务器来说，这特别友好。

## 2. gradle wrapper将gradle部署在哪里？

默认`$HOME/.gradle/wrapper/dists/`目录下。

```bash
➜  dists l
total 0
drwxr-xr-x  10 laxian  staff   320B  4 13 21:59 .
drwxr-xr-x   3 laxian  staff    96B  1 24 10:51 ..
drwxr-xr-x   3 laxian  staff    96B  3  9 21:16 gradle-4.1-all
drwxr-xr-x   3 laxian  staff    96B  4 12 21:45 gradle-5.2.1-bin
drwxr-xr-x   4 laxian  staff   128B  4 12 21:46 gradle-5.6.4-all
drwxr-xr-x   5 laxian  staff   160B  4 12 21:53 gradle-6.5-all
drwxr-xr-x   3 laxian  staff    96B  2 21 21:57 gradle-6.5-bin
drwxr-xr-x   3 laxian  staff    96B  4  3 21:58 gradle-6.7-all
drwxr-xr-x   3 laxian  staff    96B  4 13 21:59 gradle-7.0-all
drwxr-xr-x   3 laxian  staff    96B  4 13 21:59 gradle-7.0-bin
➜  dists pwd
/Users/laxian/.gradle/wrapper/dists
```

## 3. 怎么执行任务？

Android项目为我们做好了快捷脚本，我们只需通过Android项目根目录的`gradlew/gradlew.bat`去执行gradle命令就可以。

eg: `./gradlew assembleDebug`

## gradle-wrapper.jar 是什么？

gradlew/gradlew.bat 是一个脚本，最终执行的任务的，是gradle-wrapper.jar，gradlew assemble，本质上是在执行：

`java -classpath gradle-wrapper.jar org.gradle.wrapper.GradleWrapperMain assemble`，

当然还有一些附加参数省略了。
并且gradle-wrapper.jar检测到本地没有对应版本的gradle，会根据`gradle-wrapper.properties`配置的`distributionUrl`自动下载安装。

## gradle官方的distributionUrl下载缓慢怎么办？

- 1. 可以手动下载安装包。但是安装是有规则的，看如下所示路径，有一层类似hash的目录，稍后说。

```bash
➜  dists l gradle-7.0-bin
total 0
drwxr-xr-x   3 laxian  staff    96B  4 13 21:07 .
drwxr-xr-x  10 laxian  staff   320B  4 13 21:07 ..
drwxr-xr-x   5 laxian  staff   160B  4 13 21:07 2p9ebqfz6ilrfozi676ogco7n
➜  dists l gradle-7.0-bin/2p9ebqfz6ilrfozi676ogco7n
total 0
drwxr-xr-x  5 laxian  staff   160B  4 13 21:07 .
drwxr-xr-x  3 laxian  staff    96B  4 13 21:07 ..
drwxr-xr-x  8 laxian  staff   256B  2  1  1980 gradle-7.0
-rw-r--r--  1 laxian  staff     0B  4 13 21:07 gradle-7.0-bin.zip.lck
-rw-r--r--  1 laxian  staff     0B  4 13 21:07 gradle-7.0-bin.zip.ok
```

- 2. 可以使用国内镜像

如：`https://mirrors.cloud.tencent.com/gradle`

## 下载完，怎么安装的？

- 1. 使用file协议

将http地址改为
`distributionUrl=file\:///Users/laxian/Downloads/gradle-7.0-bin.zip`
借助gradle，自动部署。

缺点：前面提到的hash，和uri是对应的，不同的uri，会生成不同的hash。

- 2. 找到hash生成方法

hash是25位的，包含0-9a-z，看不出是什么规则。
但是有两个方法可以生成。

1. 借助gradle wrapper，自动生成，然后中断gradle任务，复制自动生成的目录hash
2. gradle是开源的，看源码分析。

规则就在这里：

[getHash](https://github.com/gradle/gradle/blob/124712713a/subprojects/wrapper/src/main/java/org/gradle/wrapper/PathAssembler.java#L63)

找到规则，一切就好说了。

## hash规则

uri的md5，转byte[]，然后转36进制

## 脚本实现

hash.py 实现了hash生成。

main.sh 实现了获取gradle版本，使用镜像下载并部署的整个流程

## 使用方法

`./main.sh /path/to/android/project`

## REF

[github/gradle](https://github.com/gradle/gradle)
