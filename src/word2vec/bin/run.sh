inputfile=../data/test.txt
bin=../bin/
dict=../dict/

#1. word cut
ln -s $inputfile input.txt
python $bin/cut.py -f input.txt --userdict $dict/car.dict

#2. dedup
python $bin/dedup.py -i input.cut -o all-dedup.cut -k3

#3.sentence breaker
python $bin/sentsplit.py all-dedup.cut all-dedup.sent
python $bin/sentlen_cut.py all-dedup.sent all-dedup-sent.txt

#4. train model
python $bin/word2vec.py all-dedup-sent.txt
