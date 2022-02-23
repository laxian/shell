#!/usr/bin/env python

import sys
import re

'''
将px替换成rem，并乘以转换系数。
例如，假设系数为0.01：100px -> 1rem
Usage: 
	python px2rem.py <*.css> <0.01>
	$1 file path
	$2 factor = 1px/1rem

Sample:
	./px2rem.py css/deliver.css 0.01
'''

if len(sys.argv) < 3:
        print("Usage: python px2rem.py <*.css> <0.01>")

file = sys.argv[1]
factor = sys.argv[2]

outfile=file.replace(".css", "") + "-rem.css"
outfile_w=open(outfile, "w")
for line in open(file, 'r').readlines():
        match=re.findall('((\d+)px)', line)
        if match:
                rem="%rrem" % (int(match[0][1])*float(factor))
                line.replace(match[0][0], rem)
        outfile_w.write(line)