#!/usr/bin/env bash -x

input=log_commits_line.txt
line_num=$(wc -l $input | awk '{print $1}')
OLD_IFS=$IFS
IFS=$'\n'
for l in $(cat $input); do
    # echo $l
    this_commit_line_num=$(echo $l | cut -d ':' -f 1)
    this_commit_id=$(echo $l | cut -d ' ' -f 2)
    # echo this: $this_commit_line_num
    # echo last: $last_commit_line_num
    gap=$((this_commit_line_num - last_commit_line_num))
    if [[ $gap -gt 10000 ]]; then
        echo $last_line:$gap
    fi
    last_commit_line_num=$this_commit_line_num
    last_line=$l
done > output.txt

IFS=$OLD_IFS
