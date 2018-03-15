import sys
import os
from wcut.jieba.norm import norm_cut,norm_seg,load_industrydict
from wcut.jieba import  suggest_freq
from exldeal import XLSDeal
load_industrydict([0,2,7])

class Prepare(object):

    def __init__(self,kword):
        self.kword = kword

    def cut_word(self,sent):
        return [i for i in norm_cut(sent)]

    def is_contain(self,words):
        if self.kword.decode('utf-8','ignore') in words:
            return 1
        else:
            return 0

    def run(self,infile,outfile):
        outf = open(outfile,'wb')
        ins = XLSDeal()
        lfile = ins.XlsToList(infile)
        num = 0
        for line in lfile:
            if line:
                num += 1
                sent = line.split('\t')[0].lower()
                words = self.cut_word(sent)
                print ' '.join(words)
                lab = self.is_contain(words)
                outline = str(lab) + ' ' + str(num) + ' ' + ' '.join(words)
                outf.write('%s\n'%outline.encode('utf-8','ignore'))
        outf.close()

if __name__ == '__main__':
    ins = Prepare(sys.argv[1])
    ins.run(sys.argv[2],sys.argv[3])





