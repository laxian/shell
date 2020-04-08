# Android 反编译
## 步骤
* apk解压出classes.dex。一个或多个
* dex2jar工具，将.dex转换成.jar文件
* jd-gui工具，打开.jar文件

## apkviewer
Shell脚本，一键执行上面步骤


## jar_wrapper.sh

```shell
# before
java -jar helloworld.jar

# convert to shell
cat jar_wrapper.sh helloworld.jar > hello.run && chmod +x hello.run 

# after
./hello.run
```
[How to make a JAR file Linux executable](https://coderwall.com/p/ssuaxa/how-to-make-a-jar-file-linux-executable)

