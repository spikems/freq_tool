#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
# import gensim
import json
import numpy as np
import os
import requests
# import urllib
from scipy import spatial
# from gensim.models import KeyedVectors
# from gensim.models.word2vec import Word2Vec
# from wcut.jieba.norm import norm_cut,norm_seg,load_industrydict
# load_industrydict([0,2,7])
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# # 单例模式
# def singleton(cls, *args, **kw):
#     instances = {}
#     def _singleton():
#         if cls not in instances:
#             instances[cls] = cls(*args, **kw)
#         return instances[cls]
#     return _singleton

# @singleton
class sent2similarity():
    def __init__(self):
        # url = 'http://112.253.2.39:1107/sentvec/?sent=%s&is_seg=%s' % (sent,is_seg)
        pass
        # self.model = KeyedVectors.load_word2vec_format(
        #     '/home/wangwei/program/word2vec/data/full_300_cbow_min40.bin',
        #                                                   binary=True)
        # self.index2word_set = set(self.model.index2word)
        # def cut_word(self,sent):
        #     return [i for i in norm_cut(sent)]
    def sent_vec(self,sent,is_seg=True):
        print sent
        url = 'http://112.253.2.39:1107/sentvec/?sent=%s&is_seg=%s'%(sent, is_seg)
        r = requests.get(url)
        return  np.array(r.json())

    def compute_similarity(self,sent1,sent2):

        s1_afv = self.sent_vec(sent1)
        s2_afv = self.sent_vec(sent2)
        sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
        print 'simi_one', sim
        return sim
        # print 'sime_two', synonyms.compare(sent1,sent2)

if __name__ == '__main__':
    sent1 = '大众车价格是多少'
    sent2 = '大众车价格怎么样'
    ins = sent2similarity()
    ins.compute_similarity(sent1,sent2)














