#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys

inf = open(sys.argv[1],'r')
outf = open(sys.argv[2], 'w')
endchar=['�','。','？','！！！','！','...','?','!!!','!']
for line in inf:
    for ch in endchar:
        line = line.replace(ch,ch + '\n')
    outf.write(line)

inf.close()
outf.close()
