#coding:utf-8
datadir=/home/wangwei/mapreduce/data/

echo 'Seconde get hdfs'
date
hadoop fs -rm -r  /user/wangwei/chi2_val/format.txt
hadoop fs -put $datadir/format.txt /user/wangwei/chi2_val/
echo 'Third run mapreduce'
date
hadoop fs -rm -r /user/wangwei/chi2_val/chi2_result2018
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar -files mapper.py,reducer.py  -mapper mapper.py -reducer reducer.py -input /user/wangwei/chi2_val/format.txt -output /user/wangwei/chi2_val/chi2_result2018

echo 'Forth compute chi2'
date
rm -rf $datadir/part-00000
hadoop fs -get /user/wangwei/chi2_val/chi2_result2018/part-00000 $datadir/part-00000
allnum=`awk '{print NR}' $datadir/format.txt|tail -n1`
python compute.py $datadir/part-00000 $allnum $datadir/chiresult.txt

echo 'Firth scp b6'
#scp -r -P 17717 $datadir/chiresult.txt wangwei@b6:/disk2/wangwei/data/
date
echo 'finish'
