#!/bin/bash

#求两个数之和,从键盘读取输入

echo please input a integer:
read num1
if [[ $num1 =~ ^-?[0-9]+$ ]]
then
	echo the first num is $num1
fi


echo please input a integer:
read num2
if [[ $num2 =~ ^-?[0-9]+$ ]]
then
	echo the first num is $num2
fi

let sum=$num1+$num2
echo sum is $sum
