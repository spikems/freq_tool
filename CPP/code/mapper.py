#!/usr/bin/env python
import sys
for line in sys.stdin:
    words = line.strip().split('\t')
    length = len(words)
    if length < 1:
        continue
    if length < 2:
        print "2_%s\t%s" % (words[0], 1)
        continue
    for i in range(length - 1):
        for j in range(i + 1, length):
            if words[i] > words[j]:
                out = '1_%s_%s' % (words[j], words[i])
            else:
                out = '1_%s_%s' % (words[i], words[j])
            print "%s\t%s" % (out, 1)

        print "2_%s\t%s" % (words[i], 1)
    print "2_%s\t%s" % (words[length - 1], 1)
            #print "%s\t%s" % (out, 1)
        


