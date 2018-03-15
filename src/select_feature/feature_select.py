#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
select feature from a file
"""
import sys
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn.feature_selection import SelectKBest,chi2
from wcut.jieba.norm import norm_cut,load_industrydict
from collections import Counter
load_industrydict([0,2,7])


class FeatureSelect(object):
    """
    1.load data
    2.cut word
    3.load vocabulary
    4,init_vectorizer
    """

    def __init__(self):
        self.vectorizer=None
        self.vocabulary = None

    def load_data(self,infile):
        self.data = []
        with open(infile,'rb') as inf:
            for line in inf :
                self.data.append(self.cut_word(line))
        return self.data

    def init_vocabulary(self, fname):
        """
        Load Vocabulary from a file, one word each line.
        This was materialized by mannual feature selection.
        Return an iterable over terms. If not given, a vocabulary is determined from the input documents.
        """
        #check first
        if not (fname and os.path.exists(fname)):
            self.vocabulary = None
            return None

        vocab = []
        with open(fname, 'r') as inf:
            for line in inf:
                # raw presentation can be different to feature's
                # such as a 2-gram example
                # 不 需要   --> 　不需要
                # TODO: save the mapping of raw presentation from the vocabulary file, which will be used for future annotation step
                # bugfix, convert to unicode because vectorizer.analyzer output unicode by default
                vocab.append(line.strip().replace(' ','').decode('utf-8'))
            self.vocabulary = vocab
        logger.info('init vocabulary, size = %d', len(self.vocabulary))
        return self.vocabulary

    def init_stopword(self):
        self.stopword = []
        with open('dict/stopword.dict','rb') as inf:
            for line in inf:
                self.stopword.append(line.strip())


    def init_vectorizer(self,vectype='tfidf',ngram_range=(1,1), max_df=0.9):
        """
        {tfidf,count}
        :param vectype:
        :return:
        """
        if vectype == 'tfidf':
            self.vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=max_df, ngram_range=ngram_range, vocabulary = self.vocabulary, token_pattern=r'[^ ]+')

        elif vectype == 'count':
            self.vectorizer = CountVectorizer(binary = True, max_df=max_df, ngram_range=ngram_range, vocabulary = self.vocabulary, token_pattern=r'[^ ]+')

        return self.vectorizer

    def cut_word(self,line):
        return ' '.join([i for i in norm_cut(line) if i.encode('utf-8','ignore') not in self.stopword ])


    def transform(self):
        if self.vectorizer == None:
            return ' '
        result = set([])
        dupword = set([])
        count = self.vectorizer.fit_transform(self.data)
        feature_names = self.vectorizer.get_feature_names()#返回所有关键词
        transformer = TfidfTransformer()

        tfidf = transformer.fit_transform(count) #转化成tfidf
        weight = tfidf.toarray() #权重
        for i in range(len(weight)):
            for j in range(len(feature_names)):
                if weight[i][j] > 0.02 and feature_names[j] not in dupword:
                    result.add((feature_names[j],weight[i][j]))
                    dupword.add(feature_names[j])
        return sorted(result,key=lambda x:x[1],reverse=True)


    def count_word(self):
        lword = []
        for line in self.data:
            lword.extend(line.strip().split(' '))

        cword = Counter(lword)
        sort_word = sorted(cword.items(),key=lambda x:x[1],reverse=True)
        return sort_word


    def run(self,infile,outfile ,vtype='tfidf'):
        outf = open(outfile,'w')
        self.init_stopword()
        # print self.stopword
        self.load_data(infile)
        if vtype=='tfidf':
            self.init_vectorizer()
            for sub in self.transform():
                outf.write('%s\t%s\n'%(sub[0].encode('utf-8','ignore'),sub[1]))
            outf.close()
        else:
            cword = self.count_word()
            for sub in cword:
                outf.write('%s\t%s\n' % (sub[0].encode('utf-8', 'ignore'), sub[1]))
            outf.close()




if __name__ == '__main__':
    ins = FeatureSelect()
    ins.run(sys.argv[1],'count.txt','count')
    # for sub in result:
    #     print sub[0].encode('utf-8','ignore'),sub[1]





