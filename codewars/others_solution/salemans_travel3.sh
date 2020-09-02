#!/bin/bash -x
#echo "$1" >&2; echo "$2" >&2
<<<"$1" tr , '\n' | sed -n '/ '"$2"'$/s/ '"$2"'$//p' | { 
  printf "%s:" "$2"
  tmp=$(mktemp)
  tee >(cut -d' ' -f1 >"$tmp") | cut -d' ' -f2- | tr '\n' , | sed 's/,$//';
  printf "/"
  <"$tmp" tr '\n' , | sed 's/,$//';
  rm "$tmp"
}