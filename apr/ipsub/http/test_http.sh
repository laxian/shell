#!/usr/bin/env sh -x



pingIp() {
    ping -c 1 $1 >/dev/null && echo $1 \\t\\t "\033[42;37m OK \033[0m" || echo $1 \\t\\t "\033[41;37m FAILED \033[0m"
}

head() {
    status=$(curl -s -m 5 -IL $1 | grep -E "HTTP.*?\s\d{3,}" | cut -d' ' -f2 | tr '\n' '-')
    if [ -z $status ]; then
        echo $1 \\t\\t "\033[41;37m FAILED \033[0m"
    else
        echo $1 \\t\\t "\033[42;37m $status \033[0m"
    fi
}

for l in $(cat http_new);do
echo $l
head $l
done

