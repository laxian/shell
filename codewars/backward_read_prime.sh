#!/usr/bin/env bash

# ----------------------------
# https://www.codewars.com/kata/5539fecef69c483c5a000015/shell
# isPrime 效率太低参考
# https://www.oschina.net/question/2007041_2304001
# ----------------------------

sqrt() {
    awk -v x=$1 'BEGIN{print sqrt(x)}' | sed "s#\..*\$##g"
}

isPrime() {
    #   num=$1;
    if [ $1 -eq 2 -o $1 -eq 3 ]; then
        return 0
    fi

    mod6=$(($1 % 6))
    if [ $mod6 -ne 1 -a $mod6 -ne 5 ]; then
        return 1
    fi

    # temp=`echo "scale=0;sqrt($1)" | bc`;
    for ((j = 5; j * j <= $1; j += 6)); do
        let j2=j+2
        if [ $(($1 % $j)) -eq 0 -o $(($1 % $j2)) -eq 0 ]; then
            return 1
        fi
    done

    return 0
}

reverse() {
    echo $1 | rev
}

main() {
    start=$1
    end=$2
    couples=()
    for j in $(seq $start $end); do

        n=$j
        if isPrime $n; then
            rev=$(reverse $n)
            if [[ $rev != $n ]]; then
                if isPrime $rev; then
                    if [[ $n -ge $start && $n -le $end ]]; then
                        couples+="$n "
                    fi
                fi
            fi
        fi
    done
    echo $couples | tr ' ' '\n' | sort -n | tr '\n' ' '
}

hasReverse() {
    num=$1
    if [[ $num < 10 ]]; then
        return 1
    fi
    # rev=$(reverse $num)
    # if [[ $num -ge $rev ]]; then
    #     return 1
    # fi
    return 0
}

testIsPrime() {
    for i in $(seq $1 $2); do
        num=$i
        if isPrime $num; then
            echo "$num is prime"
        fi
    done
}

testHasReverse() {
    for i in $(seq 1 100); do
        if hasReverse "$i"; then
            echo "$i has backward"
        fi
    done
}


main $1 $2
