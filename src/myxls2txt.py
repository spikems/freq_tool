#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


from __future__ import print_function
from os.path import join, dirname, abspath
import os
import logging
import xlrd
import sys
import numpy as np
from optparse import OptionParser


def trim(line):
    """
        remove all \n\r\t in line
    """
    return line.replace('\n','').replace('\r','').replace('\t','')

SPERATE = '\t'

class XLSDumper():
    """
    Dump data from definite columns in a xls/xlsx file.

    """
    def __init__(self):
        self.xl_workbook = None

    def loadbook(self, fname, timecolid=2):
        self.xl_workbook = xlrd.open_workbook(fname, encoding_override="utf-8")
        self.timecolid = timecolid
        return self.xl_workbook

    def dumpsheet(self, outfname, index = 0):
        xl_sheet = self.xl_workbook.sheet_by_index(index)

        # all values, iterating through rows and columns
        isfirstline = True
        num_cols = xl_sheet.ncols   # Number of columns
        for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
            arow = []
            for col in range(xl_sheet.ncols): 
                cell_obj = xl_sheet.cell_value(row_idx, col)  # type
                if not isfirstline and col == int(self.timecolid):
                    print (xlrd.xldate.xldate_as_datetime(cell_obj, 1).replace('\n', '').replace(SPERATE, ''), end=SPERATE)
                    continue
                if type(cell_obj) == float or type(cell_obj) == int:
                    print (str(int(cell_obj)), end = SPERATE)
                else:
                    print(cell_obj.encode('utf-8').replace('\n', '').replace(SPERATE, ''), end=SPERATE)
            isfirstline = False
            print() 

if __name__=='__main__':
    filename = sys.argv[1]
   # timeColid = sys.argv[2] # 起始行默认1
   # index = int(sys.argv[3]) #表索引 默认0

    # Open the workbook
    workbook = XLSDumper()
    workbook.loadbook(filename)
    workbook.dumpsheet(filename + '.txt')
