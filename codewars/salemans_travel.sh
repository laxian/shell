#!/bin/bash

# ----------------------------
# Saleman's travel
# https://www.codewars.com/kata/56af1a20509ce5b9b000001e/solutions/shell
# ----------------------------

travel() {
    ad="$1"
    zip="$2"
    lines=$(echo "$ad" | tr -d '\n' | tr ',' '\n')
    result=$(echo "$lines" | grep "$zip$" | while read line; do
        echo $line | awk -F" $zip" '{print $1}'
    done)
    result=$(echo "$result" |tr '\n' ';')
    IFS_OLD=$IFS
    IFS=';'
    for line in $result; do
        if [ $miles ]; then
            mile=$(echo $line | cut -d' ' -f1)
            miles="$miles,$mile"
            ads="$ads,${line#*$mile }"
        else
            miles=$(echo $line | cut -d' ' -f1)
            ads=${line#*$miles }
        fi
    done
    IFS=$IFS_OLD
    echo "$zip:$ads/$miles"
}

travel "$1" "$2"
