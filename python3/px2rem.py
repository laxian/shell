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
print(outfile)
for line in open(file, 'r').readlines():
        # 0px不处理
        line=re.sub(r'\b0px', '0', line)
        line=re.sub(r'\b0.0px', '0', line)
        match=re.findall('((\d+)px)', line)
        if match:
                # 一行多匹配，分别处理
                for tub in match:
                        print(tub)
                        rem="%rrem" % (int(tub[1])*float(factor))
                        print(rem)
                        line=line.replace(tub[0], rem)
        outfile_w.write(line)