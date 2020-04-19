#!/bin/sh

url=http://localhost:8081/repository/rawrepo
path=com/segway/robot/app

file=$1

curl -v -u admin:admin --upload-file $file $url/$path/$file