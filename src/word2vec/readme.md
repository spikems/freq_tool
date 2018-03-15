demo of word2vec train
=========================

Simple demo for training with cosmetic text.

```sh
cd work
sh ../bin/run.sh
```

### word cut
Word cut uses norm_seg interface which is based on jieba.0.39, with special word support.  
Loading user dictionary directly, no necessary to assign the freq value for each new word.  
For more details, refer to the cut.py.

### de-duplication
The cosmetic dataset is about 4.5GB, 1737744 lines, after deduplication only 753487 remains.

### sentence breaker
Simple heuristic rules to break at the sentence boundary, and remove the sentence too short and too long.

### train word2vec model
As a small file, this demo use gensim to train directly on a single machine.  
25GB RAM occupied during the training with 32 threads.

### parallel process and training
For processing in single node, a tool 'parallel' can be used to accelarate word cut, refer to parallel_cut.  
For larger dataset, Spark and DMTK can be used.

### dependency
similar to the requirements of the semeval project

module dependency as:

    simhash 
    gensim
    jieba   ; included

