# -*- coding:utf-8 -*-
import logging
import datetime
import sys
import re
import os
import traceback
from elasticsearch import Elasticsearch
from elasticsearch import helpers
reload(sys)
sys.setdefaultencoding('utf-8')
es = Elasticsearch(["http://192.168.241.35:9200", "http://192.168.241.46:9200", "192.168.241.50:9201",
                    "http://192.168.241.47:9201"], sniffer_timeout=False)

logging.basicConfig(level =logging.INFO)
def trim(words):
    if words:
        return words.replace('\r','').replace('\t','').replace('\n','')
    else :
        return ''

def es_query(word):
#搜索口红，必须包含品牌，或者是必须是推荐帖
    body = {
    "query": {"bool": {"must": [{"range": {
      "post_time": {
      "gte": "2017-11-20 00:00:00",
      "lte": "2017-12-9 00:00:00"
      }
      }},{"multi_match": {
    "fields":["title","text"],
    "query": word,
    "type":"phrase",
    "minimum_should_match": "100%",
    "slop":0}}]}}}

# weibo contain   
    bodys ={"query":{"bool":{"must": [{"term":{"site_name":word}},{"range": {
    "post_time": {
    "gt" : "2017-1-1 00:00:00",
    "lte": "2018-3-14 00:00:00" }
    }}]}}}
    es_count = es.count(index="community2", body=bodys,request_timeout = 600)
    logging.info('word:num == %s:%s'%(word,es_count['count']))
    es_re = helpers.scan(es, query=bodys, index="community2",request_timeout = 600)
   # es_re =es.search(index= "community2",body=bodys)
    return es_re
    
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
    infile = open(sys.argv[1],'rb')
    outfile = open('%sresult'%sys.argv[1],'wb')
    # line = 'word\tauthor_id\tauthor_name\tbrands\ttitle\ttext\tis_kol\turl\tpost_time\tcomment_num\tlike_num\trepost_num\tsite_name\tip_text\tmarketing_trend' \
    #        '\tdata_type\n'
    # line = 'qword\tproduct\tincludetime\tquestion\tis_contrast\tattribute\tbrand\tcomponent\tanwser\n'
    # outfile.write(line)
    for word in infile:
        word = word.strip()
        logging.info(word)
    	es_re = es_query(word.strip())
        for i in es_re:
            i = i['_source']
            try:
                line = '%s\t%s\%s\n'%(trim(i['title']),trim(i['text']),i['site_name'])
                # line='%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'\
                #      %(word,i['author_id'],i['author_name'],' '.join(i.get('brands',[])),trim(i['title']),trim(i['text']),
                #        i['is_kol'],i['url'],i['post_time'],i['comment_num'],i['like_num'],i['repost_num'],i['site_name']
                #        ,' '.join(i.get('ip_text',[])),i['marketing_trend'],i['data_type'])
                # line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(i['qword'],'#'.join(i['product']),i['include_time']
                #         ,i['title'],i['is_contrast'],'#'.join(i['attribute']),'#'.join(i['brand']),'#'.join(i['component']),
                #         i['anwser'])
                outfile.write(line)
            except:
                traceback.print_exc() 
     
    outfile.close()
    infile.close()

    
#if __name__ == "__main__":
#    outfile = open('weibo_format','wb')
#    result = main()
#    for line in result:
#        outfile.write('%s\n'%line)          
#    outfile.close()        
