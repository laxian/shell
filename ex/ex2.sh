#!/bin/bash

#计算1-100的和
sum=0
for i in {1..100}
do
    let sum+=$i
done

echo sum is $sum
