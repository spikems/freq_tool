#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import sys
from exldeal import XLSDeal

exist_num = [666,1532,268,185,979,302,1185,413,1030,566,1031,949,59,205,780,860,368,
             1229,1053,618,748,121,838,1972,1155,935,940,707,218,1880,551,1011,132,1386,157,1926,62,488,1263,30,1707,381,1372,229,1605]

xls_ins = XLSDeal()
lfile = xls_ins.XlsToList(sys.argv[1])

already_file = open('cluster0307','wb')
need_train_file = open('need_train','wb')

for line in lfile :
    sent = line.strip().split('\t')
    num = int(sent[0].strip())
    if num not in exist_num:
        need_train_file.write('%s\n'%'\t'.join(sent[1:]))
    else:
        already_file.write('%s\n'%line)
already_file.close()
need_train_file.close()

