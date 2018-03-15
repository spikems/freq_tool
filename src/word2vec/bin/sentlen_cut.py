#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys

inf = open(sys.argv[1],'r')
outf = open(sys.argv[2], 'w')
cutf = open(sys.argv[2] + '.del', 'w')

for line in inf:
    sentlen = len(line)
    if sentlen<10 or sentlen>6000:
        cutf.write(line)
    else:
        outf.write(line)

inf.close()
outf.close()
cutf.close()
