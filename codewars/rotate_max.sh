#!/usr/bin/env bash

# ----------------------------
# https://www.codewars.com/kata/56a4872cbb65f3a610000026/train/shell
# 56789 -> 67895 -> 68957 -> 68579 -> 68597
# ----------------------------

#!/bin/bash
max_rot ()
{
    local number="$1"
    local len="${#number}"
    
    # It's necessary to explicitly state the base of the number
    # or else we could end up with numbers starting with a zero
    # which would be interpreted as octal values.
    #
    # We can't just revert to string comparison because the string
    # "200" would be considered higher than the string "1000".
    local max="10#$number"

    for (( i=1; i < len; i++ )); do
        # Take out the base before rotating.
        number="${number#10#}"
        # Now use some sweet variable expansion to rotate the digits.
        number="10#${number:0:$((i - 1))}${number:$i}${number:$((i - 1)):1}"
        # And an even sweeter arithmetic comparison.
        if (( number > max )); then
            max="$number"
            echo $max
        fi
    done
    
    # Finally, print the number without the base.
    echo "${max#10#}"
}
max_rot "$1"