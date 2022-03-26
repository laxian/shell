# Java 手动编译

## javac

```Bash
javac -d $CLASSES_DIR -encoding utf-8 -cp "$CLASSPATH" -sourcepath $SRC_DIR @$CLASSES_DIR/sources.list

-d $CLASSES_DIR # class文件输出目录
-encoding utf-8 # 编码
-cp "$CLASSPATH" # classpath，路径或jar文件，以”:“连接
-sourcepath $SRC_DIR # 源码目录，src目录
@$CLASSES_DIR/sources.list # java文件列表，绝对路径，一行一个文件
```

## jar

```Bash
# 解压jar
jar xf $l

# 生成
jar -cvfm $OUTPUT_DIR/$JAR_NAME.jar ${PROJECT_DIR}/script/MANIFEST.MF *
    -c  创建新档案
    -v  在标准输出中生成详细输出
    -f  指定档案文件名
    -m  包含指定清单文件中的清单信息
    -x  从档案中提取指定的 (或所有) 文件
```

jar包含文件：

1. 项目class文件
2. 引用库class文件
3. 资源文件
4. MANIFEST.MF文件

## 运行jar

```Bash
java -jar \
--module-path /Users/leochou/Downloads/javafx-sdk-18-x64/lib \
--add-modules javafx.controls,javafx.fxml \
$OUTPUT_DIR/$JAR_NAME.jar
```

注意顺序，jar文件在最后

## 通过class运行

```Bash
/Library/Java/JavaVirtualMachines/jdk-15.0.1.jdk/Contents/Home/bin/java \
--module-path /Users/leochou/Downloads/javafx-sdk-18-x64/lib \
--add-modules javafx.controls,javafx.fxml \
-Dfile.encoding=UTF-8 \
-Duser.country=CN \
-Duser.language=zh \
-Duser.variant \
-cp /Users/leochou/Work/demo2/build/classes/java/main:/Users/leochou/Work/demo2/build/resources/main:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.graphics.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.fxml.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.base.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.controls.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.google.code.gson/gson/2.8.2/3edcfe49d2c6053a70a2a47e4e1c2f94998a49cf/gson-2.8.2.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.squareup.okhttp3/okhttp/3.10.0/7ef0f1d95bf4c0b3ba30bbae25e0e562b05cf75e/okhttp-3.10.0.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/org.bouncycastle/bcprov-jdk16/1.46/ce091790943599535cbb4de8ede84535b0c1260c/bcprov-jdk16-1.46.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/org.eclipse.paho/org.eclipse.paho.client.mqttv3/1.2.5/1546cfc794449c39ad569853843a930104fdc297/org.eclipse.paho.client.mqttv3-1.2.5.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.squareup.okio/okio/1.14.0/102d7be47241d781ef95f1581d414b0943053130/okio-1.14.0.jar com.segway.cmd_sender.Main
```
