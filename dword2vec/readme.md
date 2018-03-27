Word2vec Distributed Training
==================================

### Dependeny

software  |   description
--------  | ---------------------
C3        |  [Cluster Command & Control (C3) tool suite](http://www.softpanorama.org/HPC/Management_software/c3_tools.shtml)
cmake     |  [CMake](https://cmake.org/)
MPICH2    |  [mpi library](http://www.mpich.org/downloads/)

First, configure the cluster. One is the hostfile for mpi enviroment, the other is the c3 config file for c3 tool.

For mpi hostfile, please refer to wordembedding/cluster.ip. c3 need to setup the configure file for the cluster, and set env C3_CONF to point to your config file. Please refer wordembedding/juliet.c3conf for your reference.  

Secondly, install these software on the cluster. Tar files in the soft sub-directory for your reference.

```
#
# test c3 tool
# if correctly configured, you can see the hostname of all the nodes of your cluster.
cexec hostname
```

### Compile DMTK Multiverso wordembedding

Refer to the README in the directory

```
cd Multiverso
mkdir -p build
cd build
cmake ..
make -j8
```

If no error occurs, two files under 'build' are the target executable application.


* Applications/WordEmbedding/wordembedding
* src/libmultiverso.so

### Data Preprocess

word cut and create the vocabulary

these codes work on hdfs+yarn+spark, first you should have a hadoop cluster installed.

input file by default is put under hdfs://data/auto/

```
cd preprocess

#
#check the runyarn_cut.sh
#change the settings if in necessary, such as nodes, threads, mem; and the directories
#
./runyarn_cut.sh

#get cut files
hadoop fs -get /data/auto.cut

./runyarn_wordcount.sh

#get vocabulary 
hadoop fs -get /data/auto.wordcount
cat auto.wordcount/* |sort -nr -k 2 >auto.vocab

```

### Run wordembedding training


```
#
# distribute the execute program
#

cd Multiverso
cexec mkdir -p `pwd`/Applications/WordEmbedding/wordembedding
cexec mkdir -p `pwd`/src/

cpush `pwd`/Applications/WordEmbedding/wordembedding `pwd`/Applications/WordEmbedding/
cpush `pwd`/src/libmultiverso.so `pwd`/src/

cd wordembedding
cp ../Multiverso/Applications/WordEmbedding/wordembedding bin/

cpush auto.vocab `pwd
cpush stopwords.txt `pwd`


#
# distribute the auto.cut to all the nodes
#
cat auto.cut/* >auto_cut.txt
mkdir split
cd split
sh ../split2c.sh ../auto_cut.txt #nodenum#
cd ..
sh initdata.sh

#
# set the parameter as you need
# by default, input is train.txt and train.vocab, stopwords.txt
# cluster.ip for the nodes list
#
sh train-sgram.sh

```




