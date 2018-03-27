size=300
text=train
read_vocab=${text}.vocab
train_file=${text}.txt
binary=1
cbow=0
alpha=0.05
epoch=20
window=10
sample=0.001
hs=0
negative=5
threads=20
mincount=5
sw_file=stopwords.txt
stopwords=5
data_block_size=100000000
max_preload_data_size=300000000
use_adagrad=0
output=auto_sgram_${size}.bin
is_pipeline=1
hostfile=cluster.ip
runid=`date +%m%d%H%M%S`
log_file=${text}_${size}_${runid}.log

#mpiexec.exe -machinefile machine_file.txt WordEmbedding.exe -is_pipeline ${is_pipeline} -max_preload_data_size ${max_preload_data_size} -alpha ${alpha} -data_block_size ${data_block_size} -train_file ${train_file} -output ${output} -threads ${threads} -size ${size} -binary ${binary} -cbow ${cbow} -epoch ${epoch} -negative ${negative} -hs ${hs} -sample ${sample} -min_count ${mincount} -window ${window} -stopwords ${stopwords} -sw_file ${sw_file} -read_vocab ${read_vocab} -use_adagrad ${use_adagrad}  2>&1 |tee $log_file
#bin/wordembedding -is_pipeline ${is_pipeline} -max_preload_data_size ${max_preload_data_size} -alpha ${alpha} -data_block_size ${data_block_size} -train_file ${train_file} -output ${output} -threads ${threads} -size ${size} -binary ${binary} -cbow ${cbow} -epoch ${epoch} -negative ${negative} -hs ${hs} -sample ${sample} -min_count ${mincount} -window ${window} -stopwords ${stopwords} -sw_file ${sw_file} -read_vocab ${read_vocab} -use_adagrad ${use_adagrad}  2>&1 |tee $log_file
mpirun --hostfile $hostfile --bind-to none bin/wordembedding -is_pipeline ${is_pipeline} -max_preload_data_size ${max_preload_data_size} -alpha ${alpha} -data_block_size ${data_block_size} -train_file ${train_file} -output ${output} -threads ${threads} -size ${size} -binary ${binary} -cbow ${cbow} -epoch ${epoch} -negative ${negative} -hs ${hs} -sample ${sample} -min_count ${mincount} -window ${window} -stopwords ${stopwords} -sw_file ${sw_file} -read_vocab ${read_vocab} -use_adagrad ${use_adagrad}  2>&1 |tee $log_file


