from __future__ import print_function
from os.path import join, dirname, abspath
import os
import logging
import sys
from datetime import datetime
from pyspark import SparkContext

# Open the workbook
sc = SparkContext(appName="wordcount")  # SparkContext

# Load and parse the data
if len(sys.argv) > 1:
    data = sc.textFile(sys.argv[1] + "/*")
else:
    data = sc.textFile("/data/auto.cut/*")

counts = data.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)

output = counts.map(lambda a:'%s %s'%(a[0],a[1]))
#counts.saveAsTextFile("/data/xpost.wordcount/")
output.saveAsTextFile("/data/auto.wordcount/")

sc.stop()



