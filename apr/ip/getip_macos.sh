#!/bin/sh

# ifconfig | grep "inet " | grep -v 127 | awk '{print $2}'
ipconfig getifaddr en0