#!/usr/bin/env bash -x

PROJECT_DIR=$(
    cd ${1:-..} || exit 1
    pwd
)

JAR_NAME=MakeJar
OUTPUT_DIR=$PROJECT_DIR/build/jars

java -jar --module-path /Users/leochou/Downloads/javafx-sdk-18-x64/lib --add-modules javafx.controls,javafx.fxml $OUTPUT_DIR/$JAR_NAME.jar
