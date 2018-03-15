#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys

inf = open(sys.argv[1],'r')
outf = open(sys.argv[2], 'w')
endchar=['�','。','？','！！！','！','...','?','!!!','!']
for line in inf:
    outf.write('%s %s'%(len(line), line))

inf.close()
outf.close()
