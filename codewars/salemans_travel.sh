#!/bin/bash

# ----------------------------
# Saleman's travel
# https://www.codewars.com/kata/56af1a20509ce5b9b000001e/solutions/shell
# ----------------------------

travel() {
    ad="$1"
    zip="$2"
    lines=$(echo "$ad" | tr -d '\n' | tr ',' '\n')
    filter=$(echo "$lines" | grep -w "$zip$" | while read line; do
        echo $line | awk -F" $zip" '{print $1}'
    done)
    filter=$(echo "$filter" | tr '\n' ';')
    OLD_IFS=$IFS IFS=';'
    for line in $filter; do
        if [ $miles ]; then
            mile=$(echo $line | cut -d' ' -f1)
            miles="$miles,$mile"
            ads="$ads,${line#*$mile }"
        else
            miles=$(echo $line | cut -d' ' -f1)
            ads=${line#*$miles }
        fi
    done
    IFS=$OLD_IFS
    echo "$zip:$ads/$miles"
}

travel "$1" "$2"
