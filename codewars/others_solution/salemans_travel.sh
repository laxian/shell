#!/bin/bash -x
travel() {
    zipcode=$2
    s=$(echo $1 | tr '\n' ',')
    IFS=',' read -ra NAMES <<< "$s"
    for i in "${NAMES[@]}"; do
        r=$(echo "$i" | grep -w "$zipcode")
        if [ -n "$r" ]; then
            r=$(echo $r | sed -e "s/$zipcode//")
            nb=$(echo $r | sed 's/[^0-9]//g')
            strTwn=$(echo $r | sed -e "s/$nb//")
            strTwn=$(echo $strTwn | sed -e "s/^[[:space:]]//")
            result1="${result1},$nb"
            result2="${result2},$strTwn"
       fi
    done
    result="$zipcode:${result2:1}/${result1:1}"
    echo $result
}
travel "$1" "$2"