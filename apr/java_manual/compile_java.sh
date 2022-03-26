#!/usr/bin/env bash -x

PROJECT_DIR=$(
    cd ${1:-..} || exit 1
    pwd
)

CLASSPATH="/Users/leochou/Work/demo2/build/classes/java/main:/Users/leochou/Work/demo2/build/resources/main:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.graphics.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.fxml.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.base.jar:/Users/leochou/Downloads/javafx-sdk-18-x64/lib/javafx.controls.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.google.code.gson/gson/2.8.2/3edcfe49d2c6053a70a2a47e4e1c2f94998a49cf/gson-2.8.2.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.squareup.okhttp3/okhttp/3.10.0/7ef0f1d95bf4c0b3ba30bbae25e0e562b05cf75e/okhttp-3.10.0.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/org.bouncycastle/bcprov-jdk16/1.46/ce091790943599535cbb4de8ede84535b0c1260c/bcprov-jdk16-1.46.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/org.eclipse.paho/org.eclipse.paho.client.mqttv3/1.2.5/1546cfc794449c39ad569853843a930104fdc297/org.eclipse.paho.client.mqttv3-1.2.5.jar:/Users/leochou/.gradle/caches/modules-2/files-2.1/com.squareup.okio/okio/1.14.0/102d7be47241d781ef95f1581d414b0943053130/okio-1.14.0.jar-g"
CLASSES_DIR=$PROJECT_DIR/build/classes/java/main
SRC_DIR=$PROJECT_DIR/src

mkdir -p $CLASSES_DIR
find $SRC_DIR -name "*.java" > $CLASSES_DIR/sources.list
javac -d $CLASSES_DIR -encoding utf-8 -cp "$CLASSPATH" -sourcepath $SRC_DIR @$CLASSES_DIR/sources.list

# classes、resources路径和gradle保持一致，方便对比和测试
#cp -R $SRC_DIR/main/resources/* $PROJECT_DIR/build/resources/main/

# 和代码在一起
cp -R $SRC_DIR/main/resources/* $CLASSES_DIR

