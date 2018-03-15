#coding:utf-8
from pyltp import Postagger
from pyltp import Parser
import sys
import os
import jieba
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
dir_path =  os.path.dirname(os.path.abspath(__file__))
LTP_DATA_DIR = '/home/wangwei/hotword/hotword/conf/ltp_data'
jieba.load_userdict("/home/wangwei/hotword/hotword/conf/jieba_lexicon")
postagger = Postagger()  # 初始化实例
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
postagger.load_with_lexicon(pos_model_path, '/home/wangwei/model/posttags.txt')
# tmplist =[]
# with open(sys.argv[2],'rb') as f:
#    for line in f:
#        if line:
#            tmplist.append(line.strip())



def cut_word(sents):
    """
    分词
    """
    words = [i.encode('utf-8', 'ignore') for i in jieba.cut(sents,HMM=False) ]  # HMM=False
#    print sents, '\t'.join(words)
    return words

def word_sex(words):
    """
    获取词性
    """
    postags = list(postagger.postag(words))  # 词性标注
    # print '词性', '\t'.join(postags)
    return postags

if __name__ == '__main__':
    outfile = open('meizhuang','w')
    with open(sys.argv[1],'rb') as f:
        for line in f:
            linestr = line.strip().split('\t') 
            if len(linestr) ==2:
                brand = linestr[0]
                product = linestr[1].replace(' ','')
                if len(cut_word(product))>1 :
                    # print chardet.detect(product)
                    outfile.write('%s 100\n'%product)
            elif len(linestr) == 3:
                brand = linestr[0]
                product = linestr[1].strip().replace(' ','')
                syn = linestr[2].split('|')
                if len(cut_word(product))>1 :
                    outfile.write('%s 100\n'%product)
                for i in syn:
                    i = i.strip().replace(' ','')
                    if len(cut_word(i))>1:
                        outfile.write('%s 100\n'%i)
    outfile.close()
            # opinion_word = ''
            # attword =''
            # for w in words:
            #     if w in tmplist:
            #         attword = w
            #     else:
            #         opinion_word += w
            # print attword,opinion_word,line.strip()

           # for i in words:
          #      print i
           # if len(words)>1 and len(linestr[0].split(' '))==1:
           #     print '%s 5'%linestr[0]
    #        postags=word_sex(words)
    #        if len(postags)>0:
    #            if postags[0] !='n'and len(postags)==1 :
    #                 print '%s n'%linestr[0],postags[0]
 #           for brand in tmplist:
 #               print '%s%s'%(brand.strip(),'好')
            # if postags==['a','n'] or ['n','n'] or ['nh','n'] :
            #     print words[-1]+words[0]
            # elif len(words) == 2:
            #     print ''.join(words)
