#!/usr/bin/env bash -x

PROJECT_DIR=$(
    cd ${1:-..} || exit 1
    pwd
)

JAR_NAME=MakeJar
CLASSPATH=/Users/leochou/Work/demo2/build/classes/java/main:/Users/leochou/Work/demo2/build/resources/main:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.graphics.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.fxml.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.base.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.controls.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.google.code.gson/gson/2.8.2/3edcfe49d2c6053a70a2a47e4e1c2f94998a49cf/gson-2.8.2.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.squareup.okhttp3/okhttp/3.10.0/7ef0f1d95bf4c0b3ba30bbae25e0e562b05cf75e/okhttp-3.10.0.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/org.bouncycastle/bcprov-jdk16/1.46/ce091790943599535cbb4de8ede84535b0c1260c/bcprov-jdk16-1.46.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/org.eclipse.paho/org.eclipse.paho.client.mqttv3/1.2.5/1546cfc794449c39ad569853843a930104fdc297/org.eclipse.paho.client.mqttv3-1.2.5.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.squareup.okio/okio/1.14.0/102d7be47241d781ef95f1581d414b0943053130/okio-1.14.0.jar
CLASSES_DIR=$PROJECT_DIR/build/classes/java/main

OLDIFS=$IFS
IFS=":"
cd "$CLASSES_DIR" || exit 1

# 判断classpath中的路径，如果是jar，则解压到classes目录
for l in $CLASSPATH;do
  echo $l
  if [ "${file##*.}" = jar ]; then
    jar xf $l
  fi
done

# 将资源复制到classes目录
cp -R "${PROJECT_DIR}"/src/main/resources/* "$CLASSES_DIR"

# 删除签名jar的证书
find . -name "*.SF" -print0 | xargs rm
find . -name "*.RSA" -print0 | xargs rm
find . -name "*.DSA" -print0 | xargs rm

OUTPUT_DIR=$PROJECT_DIR/build/jars/
mkdir -p $OUTPUT_DIR

# 生成jar文件
jar -cvfm $OUTPUT_DIR/$JAR_NAME.jar ${PROJECT_DIR}/script/MANIFEST.MF *

IFS=$OLDIFS
unset $OLDIFS
