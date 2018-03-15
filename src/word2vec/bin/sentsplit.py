#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import re

inf = open(sys.argv[1],'r')
outf = open(sys.argv[2], 'w')
#endchar=['▼','�','{','}','<','>','。','？','！！！','！','...','?','!!!','!']
endchar=['…','◆','▼','�','😭','�','▲', '~', '～','{','}','<','>','；','。','？','！！！','！','...','?','!!!','!']
for line in inf:
    #remove html tags
    line = re.sub('<.*?>', '', line)
    line = re.sub('{.*?}', '', line)

    #replace
    for ch in endchar:
        line = line.replace(ch,ch + '\n')
    outf.write(line)

inf.close()
outf.close()
