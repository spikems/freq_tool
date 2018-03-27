#!/bin/bash

inputfile=$1
number=$2
bname=`basename $inputfile`

#linecnt=`wc -l $inputfile | gawk '{print $1}'`
#echo $linecnt
bytesize=`ls -l $inputfile |gawk '{print $5}'`
echo $bytesize

#partlines=`echo $linecnt/$number + 1 |bc`
partsize=`echo $bytesize/$number + 512000 |bc`

echo split -C $partsize --additional-suffix=-$bname $inputfile
#split -C $partsize --additional-suffix=-$bname $inputfile
split -C $partsize $inputfile

