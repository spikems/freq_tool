curdir=`pwd`
srcdir=split.6/
srcfiles=(`ls $srcdir`)
srvs=(`cat cluster.ip`)

echo ${#srcfiles[*]}
len=$(( ${#srcfiles[*]} - 1 ))
echo $len

idxs=(`seq 0 $len`)


for idx in ${idxs[*]}; do
    file=${srcfiles[$idx]}
    echo $file
    
    #echo ssh ${srvs[$idx]} "cd `pwd`; ln -s $srcdir/$file train.txt"
    #ssh ${srvs[$idx]} "cd `pwd`; ln -s $srcdir/$file train.txt"
    
    echo "scp $srcdir/$file  ${srvs[$idx]}:/$curdir/train.txt"
    scp $srcdir/$file  ${srvs[$idx]}:/$curdir/train.txt
    
done
