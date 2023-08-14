#!/usr/bin/env python3

# This script is used to get the pose of the robot

def pos_of_num(num):
    with open('private/pos', 'r') as pos_file:
        lines = pos_file.readlines()
        return lines[num - 1].strip().split(',')[1]

def cmd_of_num(num):
    return "input tap " + pos_of_num(num)

def cmds(string):
    ret = ""
    for char in string:
        cmd = cmd_of_num(int(char))
        if ret == "":
            ret = cmd
        else:
            ret += ";" + cmd
    return ret

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <number_string>")
    else:
        number_string = sys.argv[1]
        translated_cmds = cmds(number_string)
        print(translated_cmds)
