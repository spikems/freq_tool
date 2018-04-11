# -*- coding:utf-8 -*-
import logging
from elasticsearch import Elasticsearch
import datetime
import sys
import re
import os
import traceback
from elasticsearch import helpers
reload(sys)
sys.setdefaultencoding('utf-8')
es = Elasticsearch(["http://192.168.241.35:9200", "http://192.168.241.46:9200", "192.168.241.50:9201",
                    "http://192.168.241.47:9201"], sniffer_timeout=200, timeout=100)

logging.basicConfig(level =logging.INFO)
def trim(words):
    if words:
        return words.replace('\r','').replace('\t','').replace('\n','')
    else :
        return ''

def es_query(word,day=30):
#搜索口红，必须包含品牌，或者是必须是推荐帖

    body = {
    "query": {"bool": {"must": [{"range": {
      "post_time": {
      "gte": "now-%sd/d"%day,
      "lte": "now/d"
      }
      }},{"multi_match": {
    "fields":["title","text"],
    "query": word,
    "type":"phrase",
    "minimum_should_match": "100%",
    "slop":0}}]}}}

# weibo contain   


    bodys ={"query":{"bool":{"must": [{"range": {
    "post_time": {
    "gt" : "2017-10-1 00:00:00",
    "lte": "2017-12-06 00:00:00" }
    }},{"term":{"brands":word}}
    ]}}}
    es_count = es.count(index="community2", body=body)
    if es_count['count']>0 :
    	return True
  #  elif  es_count['count'] == 0 and day <=90:
  #      day += 60 
  #      return es_query(word,day)
    else:
        return False
 #   logging.info('word:num == %s:%s'%(word,es_count['count']) )
 #   es_re = helpers.scan(es, query=body, index="community2")
   # es_re =es.search(index= "community2",body=bodys)
  #  return es_re
    
def main():
    text_list =set()
    es_re = es_query()
    for i in es_re:
        text = str(i['_source']['text'])
        re_format = re.findall(r'(@[^@]{0,20})',text)
        if re_format:
            for word in  re_format:
                text_list.add(word)    
    return text_list
        
if __name__ == "__main__":
    
   # outfile = open(sys.argv[1],'wb') 
    logging.basicConfig(level =logging.INFO)
    infile = open(sys.argv[1],'rb')
    outfile = open('%sresult'%sys.argv[1],'wb')
    num = 0 
    for word in infile:
        print num
        num+=1
        word = word.strip()
      #  logging.info(word)
        words = word.split('\t')
        if len(words) == 2:
    	    es_re = es_query(words[1].strip())
            if es_re > 0:
                line = '%s\t%s\n'%( words[0],words[1])
                logging.info(line)
                outfile.write(line)
        elif len(words) == 3:
            brand = words[0]
            product = words[1]
            synlist = [ i for i in words[2].split('|') if es_query(i.strip())]
            if es_query(product.strip()):
                line = '%s\t%s\t%s\n'%(brand,product,'|'.join(synlist))
                logging.info('2\t%s'%line)
                outfile.write(line)
            elif synlist:
                product = synlist[0]
                synword = '|'.join(synlist[1:])   
                line = '%s\t%s\t%s\n'%(brand,product,synword)
                logging.info('3\t%s'%line)
                outfile.write(line)

#       for i in es_re:
#            i = i['_source']
#            try:
#                line='%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n'%(word,i['author_id'],i['author_name'],' '.join(i.get('brands',[])),trim(i['title']),trim(i['text']),i['is_kol'],i['url'],i['post_time'],i['comment_num'],i['like_num'],i['repost_num'],i['site_name'],' '.join(i.get('ip_text',[])))
#               outfile.write(line)
#           except:
#              traceback.print_exc() 
     
# infile.close()
    outfile.close()
#    os.system('python txtToXls.py ')
#  os.system ('sz %s.xlsx'%word)
    infile.close()

    
#if __name__ == "__main__":
#    outfile = open('weibo_format','wb')
#    result = main()
#    for line in result:
#        outfile.write('%s\n'%line)          
#    outfile.close()        
