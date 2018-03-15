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
import xlsxwriter
from optparse import OptionParser


def trim(line):
    """
        remove all \n\r\t in line
    """
    return line.replace('\n','').replace('\r','').replace('\t','')

class XLSDumper():
    """
    Dump data from definite columns in a xls/xlsx file.

    """
    def __init__(self):
        self.xl_workbook = None
        self.lines = []

    def loadbook(self, fname):
         reader = open(fname, 'rb')
         for line in reader:
             self.lines.append(line.strip().split("\t"))
            
    	 #self.lines.append(line.strip().split("\t") for line in reader)
    

    def dumpsheet(self, outfname):
        # output the .xls file
        
        # predictor.pred_prob, .pred, .dataset.data, .dataset.ids
        schema = [u'序号', u'预测分类', u'概率', u'标题与摘要']
        workbook = xlsxwriter.Workbook(outfname + '.xlsx',{'strings_to_urls': False})
        sheet = workbook.add_worksheet('predict')

        #write schema
        for col in range(len(self.lines[0])):
            sheet.write(0, col, self.lines[0][col].decode('utf-8'))
    
        #idx = [0,1,2]
        for row, indexval in enumerate(range(len(self.lines) -1 )):
            # row, indexval -> point to the original dataset
            for col in range(len(self.lines[row+1])):
                sheet.write(row + 1, col, self.lines[row + 1][col].decode('utf-8'))
                #sheet.write(row + 1, 1, predictor.dataset.target_names[pred[indexval]].decode('utf-8'))
        
        workbook.close()
if __name__=='__main__':
    filename = str(sys.argv[1])
    # Open the workbook
    workbook = XLSDumper()
    workbook.loadbook(filename)
    workbook.dumpsheet(filename)

# test
