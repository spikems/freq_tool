#-*- coding:utf-8 -*-
import sys

infile = sys.argv[1]
reader = open(infile,'rb')
writer = open(sys.argv[2],'wb')
for line in reader:
    sline = line.strip().split('\t')[:-1]
    writer.write('%s\n'%'\t'.join(sline))
reader.close()
writer.close()
