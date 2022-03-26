#!/usr/bin/env bash -x

PROJECT_DIR=$(
    cd ${1:-..} || exit 1
    pwd
)

$PROJECT_DIR/gradlew clean -p $PROJECT_DIR
