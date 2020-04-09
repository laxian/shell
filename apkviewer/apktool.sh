#!/bin/bash

path=$1

apktool=tools/apktool_2.4.1.jar
java -jar $apktool d $path
