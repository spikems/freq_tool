#!/usr/bin/env python
import sys
first = True
preword = ""
cnt = 0

for line in sys.stdin:
    fs = line.strip().split('\t')
    word = fs[0]
    
    if first:
        first = False
        preword = word
        cnt = 1
    else:
        if preword != word:
            print "%s\t%s" % (preword, cnt)
            cnt = 0
            preword = word
        cnt = cnt + 1

print "%s\t%s" % (preword, cnt)
