#!/bin/bash

ifconfig | grep -E "inet (addr|地址)" | grep -v 127.0.0.1 | awk '{print $2}' | awk -F: '{print $2}'