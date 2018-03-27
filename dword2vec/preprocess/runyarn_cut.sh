#!/bin/bash
node=10
thread=12
mem=64g

totaltask=`echo "$node * $thread" | bc`

if [ $# -ne "1" ]; then
    echo "runyarn_cut.sh <inputdir>"
    exit 1
fi


runid=`date +%m%d%H%M%S`
appname='autocut'


#
# for single big text file, set the totaltask to $node*$thread in order to make load balance
# or you can split the input by youself to fine tune it
#
echo "spark-submit  --master yarn  --num-executors $node --executor-cores $thread --executor-memory $mem autocut.py --input $1 --taskcnt $totaltask"
hadoop fs -rm -r -f /data/auto.cut
spark-submit  --master yarn  --num-executors $node --executor-cores $thread --executor-memory $mem autocut.py --input $1 --taskcnt $totaltask 2>&1 | tee the_"$appname"_T"$thread"_"$runid".info.log;
