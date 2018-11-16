#!/bin/bash

path=$1

apktool=$JD_HOME/apktool
java -jar $apktool d $path
