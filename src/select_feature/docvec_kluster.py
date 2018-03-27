#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from wcut.jieba.norm import norm_cut,load_industrydict,norm_seg
from wcut.jieba import add_word
import gensim
import sys
import os
import numpy as np
import requests
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import LatentDirichletAllocation
from exldeal import XLSDeal

load_industrydict([0,2,7])
class DocKluster(object):
    """
    跟短文本聚类
    """
    def __init__(self,infile,outfile='doc_result'):
        self.infile = infile    #输入一个excel ,格式:
        self.outfile = outfile  #输入一个txt ,

    def stop_word(self):
        """
        停用词 和 无意义的词
        :return:
        """
        stop_word = set([])
        with open('dict/stopword.dict','r') as inf:
            for line in inf:
                stop_word.add(line.strip())
        with open('dict/no_meaning_word.txt','rb') as inf:
            for line in inf:
                add_word(line.strip(),1)
                stop_word.add(line.strip())
        return stop_word

    def cut_word(self,):
        """
        读取文件并且分词

        :return:
        """
        xls_ins = XLSDeal()
        lfile = xls_ins.XlsToList(self.infile)
        lcut = []
        stopword = self.stop_word()
        self.input = [i for i in lfile if i ]
        # outf = open(self.outfile,'w')

        for line in self.input:
            sent = line.split('\t')[0].strip() #第一列句子
            oline = ' '.join([i.word for i in norm_seg(sent) if i.word.encode('utf-8','ignore') not in stopword ]) #
            feature = ' '.join('#'.join(line.split('\t')[1:]).split('#')).decode('utf-8','ignore')
            # print 'feature',feature
            lcut.append('%s %s'%(oline,feature))
            # outf.write('%s\n'%oline.encode('utf-8','ignore'))
        # outf.close()
        return lcut
    def train_doc(self,):
        sentences = gensim.models.doc2vec.TaggedLineDocument(self.outfile)
        model = gensim.models.Doc2Vec(min_count=1, window=10, size=400, sample=1e-3, negative=5, workers=3)
        model.build_vocab(sentences)
        model.train(sentences,total_examples=model.corpus_count,epochs=model.iter)
        model.save('doc_model.txt')
        self.model = model

    def get_sent_vec(self,):
        lcut = self.cut_word()
        data_vec = []
        for line in lcut:
            sent = line.strip()
            print 'sent', sent
            url = 'http://112.253.2.39:1107/sentvec/?sent=%s&is_seg=False' % (sent)
            r = requests.get(url)
            data_vec.append(np.array(r.json()))
        self.data_vec = data_vec


    def kluster(self,num_cluster=50):
        """
        :param num_cluster:  聚成多少类
        :return:
        """
        lresult = {}
        # km = KMeans(num_cluster)
        # result = km.fit_predict(self.data_vec)
        # lda = LatentDirichletAllocation(n_components=num_cluster,
        #                         max_iter=50,
        #                         learning_method='batch')
        # result = lda.fit_transform(self.data_vec)
        agg = AgglomerativeClustering(n_clusters = num_cluster)
        result = agg.fit_predict(self.data_vec)
        print result
        f2 = open('kluster_result.txt','w')
        for i in range(0,num_cluster-1):
            for num,eachline in enumerate(self.input):
                if num >= len(result):
                    break
                if result[num] == i:
                    if str(i) in lresult:
                        lresult[str(i)].append(eachline)
                    else:
                        lresult[str(i)] = []
                        lresult[str(i)].append(eachline)
        print 'length result',len(lresult)
        sort_result = sorted(lresult.items(),key=lambda x:len(x[1]),reverse=True)
        for line in sort_result:
            for content in line[1]:
                f2.write('%s\t%s\n'%(line[0],content))
        f2.close()

    # def agg_cluster(self,num_cluster=100):
    #     agg =

    def run(self):
        self.cut_word()
        self.train_doc()
        self.kluster()

    def run2(self):
        self.get_sent_vec()
        self.kluster()

if __name__ == '__main__':
    #输入格式参考need_train.xlsx
    inputfile = input('输入文件名:')
    print 'inputfile',inputfile
    ins = DocKluster(inputfile)
    ins.run2()










