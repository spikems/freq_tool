#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
wordcut the text files on spark platform

input:
    #auto data
    text a line
output: 
    cut file

usage: autocut.py <inputdir> <totaltask#>

"""

from __future__ import print_function
from os.path import join, dirname, abspath
import os
import logging
import csv
import sys
import numpy as np
import gzip
from datetime import datetime
from optparse import OptionParser
import simhash
from pyspark import SparkContext
from wcut.jieba import suggest_freq
from wcut.jieba.norm import norm_seg,load_industrydict

#test 2
load_industrydict([2,7])

#
#
#
def cutline(input):
    '''
    cut a input string, return utf-8 string
    '''
    result = norm_seg(input)
    wordsList = []
    for w in result:
        if w.word.strip() == '' or w.flag.strip() == '':
            continue
        wordsList.append(w.word)
    words = " ".join(wordsList)

    return words.encode('utf-8')

#
#
#
def computehash(text):
    """
        compute hash for a document by shingles
    """
    if len(text) < 3:
        return 0
    #tokens = re.split(r'\W+', text)
    tokens = text.split()

    #logger.debug('%s', ''.join(tokens[:5]))

    phrases = (' '.join(phrase) for phrase in simhash.shingle(tokens, 4))
    #logger.debug('%s', [x for x in phrases])

    hashes = map(simhash.unsigned_hash, phrases)
    return simhash.compute(hashes)


def load_option():
    op = OptionParser()
    op.add_option("--input",
                  action="store", type=str, dest="inputdir", default='/data/auto/',
                  help="Define the input files.")
    op.add_option("--output",
                  action="store", type=str, dest="outputdir", default='/data/auto.cut/',
                  help="define output dir.")
    op.add_option("--taskcnt",
                  action="store", type=int, default=0,
                  help="set the total tasks number.")
    op.add_option("--h",
                  action="store_true", dest="print_help",
                  help="Show help info.")
 
    (opts, args) = op.parse_args()

    #if len(args) == 0 or opts.print_help:
    #    print(__doc__)
    #    op.print_help()
    #    print()
    #    sys.exit(0)
    #else:
    #    opts.infile = args[0]

    return opts, args



if __name__=='__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # cmd argument parser
    opts, args = load_option()
    
    # Open the workbook
    sc = SparkContext(appName="WordCutExample")  # SparkContext

    # Load and parse the data
    if opts.taskcnt > 0:
        data = sc.textFile(opts.inputdir + "/*", opts.taskcnt)
    else:
        data = sc.textFile(opts.inputdir + "/*")


    #dumpdata = data.map(dumpline)
    #cutdata = dumpdata.map(cutline)
    #hashdata = cutdata.map(computehash)
    cutdata = data.map(cutline)

    cutdata.saveAsTextFile(opts.outputdir)
    #hashdata.saveAsTextFile("/data/auto.hash")

    sc.stop()

