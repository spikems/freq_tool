#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import sys
import os
from wcut.jieba.norm import norm_cut,norm_seg,load_industrydict
from wcut.jieba import  suggest_freq,load_userdict
from optparse import OptionParser

load_industrydict([0,2,7])
class JiebaFreq(object):

    def __init__(self):
        pass

    def FreqSug(self,word):
        if len(list(norm_cut(word,HMM=False)))>1:
            num = suggest_freq(word)
            line = '%s %s\n'%(word,num)
            return line
        return False

    def cut_word(self,sent):
      line = ' '.join([i for i  in norm_cut(sent)])
      print line

    def read_file(self,infile,outfile):
        outfile = open(outfile,'wb')
        with open(infile,'rb') as inf:
            for line in inf:
                out_line = self.FreqSug(line.strip().lower())
                print out_line
                if out_line:
                    outfile.write(out_line)
        outfile.close()

def load_option():
    op = OptionParser()
    op.add_option("-i",
                  action="store", type=str,dest="infile",
                  help="provide a question.")
    op.add_option("-o",
                  action="store", type=str, dest="outfile",
                  help="provide a way ,can be edit-distance or tfidf")
    (opts, args) = op.parse_args()

    return opts




if __name__ == '__main__':
    opt = load_option()
    ins = JiebaFreq()
    ins.read_file(opt.infile,opt.outfile)





