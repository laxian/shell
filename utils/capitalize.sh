#!/usr/bin/env bash 

# ----------------------------
# see: https://my.oschina.net/sfshine/blog/2874104
# foo=bar
# echo foo | sed -e "s/\b\(.\)/\u\1/g"
# ./capitalize.sh foo
# output: Foo
# ----------------------------

echo $1 | sed -e "s/\b\(.\)/\u\1/g"
