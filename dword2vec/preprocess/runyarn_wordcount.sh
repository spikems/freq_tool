#!/bin/bash
node=10
thread=12
mem=64g

if [ $# -ne "1" ]; then
    echo "runyarn_wordcount.sh <inputdir>"
    exit 1
fi

runid=`date +%m%d%H%M%S`
appname=auto.wordcount
echo "spark-submit  --master yarn  --num-executors $node --executor-cores $thread --executor-memory $mem wordcount.py $1"
hadoop fs -rm -r -f /data/auto.wordcount
spark-submit  --master yarn  --num-executors $node --executor-cores $thread --executor-memory $mem wordcount.py $1 2>&1 | tee the_"$appname"_T"$thread"_"$runid".info.log;
