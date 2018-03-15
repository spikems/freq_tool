#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import os
import sys
import logging
from wcut.jieba import  suggest_freq,load_userdict
from wcut.jieba.norm import norm_seg, norm_cut, load_industrydict

# load_userdict('../data/freqresult.txt')
load_industrydict([0,2])
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

dir_path = os.path.dirname(os.path.abspath(__file__))
LTP_DATA_DIR = '/home/wangwei/model/ltp_data_v3.4.0'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')

class LtpAnalysis(object):

    def __init__(self):
        self.postagger = Postagger()
        self.parser = Parser()
        self.parser.load(par_model_path)
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(ner_model_path)
        self.labeller = SementicRoleLabeller()
        self.labeller.load(srl_model_path)
        self.postagger.load_with_lexicon(pos_model_path, '/home/wangwei/conf/posttags.txt')

    def LtpRecon(self,sents):
        """
        分词,词性,句法,命名实体识别,语义识别
        :param sents:
        :return:
        """
        #分词
        words = [i.encode('utf-8', 'ignore') for i in norm_cut(sents)]
        logger.info('\t'.join(words))
        #词性
        postags = self.postagger.postag(words)
        logger.info('\t'.join(postags))
        #句法
        arcs = self.parser.parse(words, postags)
        logger.info("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
        #实体识别
        netags = self.recognizer.recognize(words, postags)
        logger.info('\t'.join(netags))
        #语义标注
        roles = self.labeller.label(words, postags, arcs)
        for role in roles:
            print role.index, "".join(
                ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
            
        self.words, self.postags, self.arcs, self.netags, self.roles = \
            words, postags, arcs, netags, roles

    def deal_arc(self):
        drelation = {} #word_index:(arc.head,arc.relation)
        num =-1
        for arc in self.arcs:
            num +=1
            k = str(num) + '#' + (arc.head-1)
            drelation[k] = arc.relation
        return self.drelation

    def vob(self,index):
        num = -1
        for arc in self.arcs:
            num += 1
            if arc.relation in ['VOB'] and (arc.head-1) == index:
                return self.words[num]

    def att(self,att):
        num = -1

    def post(self, target):
        """
         评价对象的扩展 ,解决ATT
         :param num:
         :return:
         """
        obj = set()
        obj.add(target)
        num = 0
        for arc in self.arcs:
            if (arc.head-1) == target and arc.relation == 'ATT' :
                obj.add(arc.head-1)
                obj |= self.post(num)
            num += 1
        return obj

    def analysis(self,sents):
        self.LtpRecon(sents)
        # self.deal_arc()
        num = -1
        for arc in self.arcs:
            num += 1
            if arc.relation == 'SBV':
                vob_word = self.vob(arc.head-1)
                att = self.post(num)
                attword = ''.join([ self.words[i] for i in att if i != num])
                print  attword ,self.words[num],self.words[arc.head-1],vob_word

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info('task is start')
    ins = LtpAnalysis()
    line = sys.argv[1]
    ins.analysis(line)


