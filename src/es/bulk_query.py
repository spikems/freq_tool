#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime,timedelta
import time
import sys
import re
import os
from optparse import OptionParser
import traceback
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from multiprocessing import Pool
reload(sys)
sys.setdefaultencoding('utf-8')
es = Elasticsearch(["http://192.168.241.35:9200", "http://192.168.241.46:9200", "192.168.241.50:9201",
                    "http://192.168.241.47:9201"], sniffer_timeout=False)

logging.basicConfig(level=logging.INFO)

def trim(words):
    if words:
        return words.replace('\r', '').replace('\t', '').replace('\n', '')
    else:
        return ''

def es_query(word,stime ,etime,outfile):
    # 搜索口红，必须包含品牌，或者是必须是推荐帖
    body = {
        "query": {"bool": {"must": [{"range": {
            "post_time": {
                "gte": "2017-11-20 00:00:00",
                "lte": "2017-12-9 00:00:00"
            }
        }}, {"multi_match": {
            "fields": ["title", "text"],
            "query": word,
            "type": "phrase",
            "minimum_should_match": "100%",
            "slop": 0}}]}}}

    # weibo contain
    bodys = {"query": {"bool": {"must": [{"term": {"site_name": word}},{"term":{"text_repeat":"F"}} ,{"range":{
        "post_time": {
            "gt": stime,
            'lte':etime}
    }}]}}}
    es_count = es.count(index="community2", body=bodys, request_timeout=600)
    logging.info('word:num == %s:%s' % (word, es_count['count']))
    es_re = helpers.scan(es, query=bodys, index="community2", request_timeout=600,size=10000)
    # es_re =es.search(index= "community2",body=bodys)
    write_file(es_re, outfile)
    return es_re

def split_time(stime,etime,day):
    """
    按月切割
    :param stime:输入一个起始时间
    :param etime: 结束时间
    :param day :间隔时间
    :return: 时间列表
    """
    ltime = []
    ltime.append(stime)
    trans_stime = datetime.strptime(stime,'%Y-%m-%d ')
    trans_etime = datetime.strptime(etime,'%Y-%m-%d ')
    while trans_stime+ timedelta(days=day) < trans_etime:
        plus_stime = trans_stime + timedelta(days=day)
        ltime.append(datetime.strftime(plus_stime,'%Y-%m-%d 00:00:00'))
        trans_stime = plus_stime
    ltime.append(etime)
    return ltime

def write_file(es_re ,outf):
    writer = open(outf,'wb')
    for i in es_re:
        i = i['_source']
        try:
            line = '%s。%s\n' % (trim(i['title']), trim(i['text']))
            writer.write(line)
        except:
            traceback.print_exc()
    writer.close()


def load_option():
    op = OptionParser()
    op.add_option("-w",
                  action="store", type=str, dest="word",default="汽车之家",
                  help="provide a question.")
    op.add_option("-s",
                  action="store", type=str, dest="stime", default="",
                  help="provide a way ,can be edit-distance or tfidf")
    op.add_option("-e",
                  action="store", type=str, dest="etime", default="",
                  help="provide a definite product")
    op.add_option("-o",
                  action="store", type=str, dest="outfile", default="",
                  help="provide a definite product")
    op.add_option("-d",
                  action="store", type=int, dest="day", default=10,
                  help="provide a time ")
    (opts, args) = op.parse_args()
    return opts

if __name__ == "__main__":
    opts = load_option()
    if not (opts.stime or opts.etime or opts.outfile):
        print 'parm is wrong'
        sys.exit(1)
    outfile = opts.outfile
    word = opts.word
    logging.info(word)
    # ltime = split_time(opts.stime, opts.etime,opts.day)
    startime = time.time()
    p = Pool(30)
    p.apply_async(es_query,args=(word,opts.stime,opts.etime,opts.outfile))
    # es_re = es_query(word,opts.stime,opts.etime,opts.outfile)
    p.close()
    p.join()
    all_time=time.time()-startime
    print 'spend how much time %s'%round(all_time,2)
    # print type(es_re)




