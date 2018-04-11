#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import helpers
from elasticsearch import Elasticsearch
import datetime
import hashlib
import sys ,os
reload(sys)
sys.setdefaultencoding('utf-8')


es = Elasticsearch(["http://192.168.241.47:9201", "http://192.168.241.46:9200", "192.168.241.50:9201"],
                   sniffer_timeout=False)


class Saver(object):
    def __init__(self, cache_size=1000):
        self.actions = []
        self._cache_size = cache_size

    def pass_data(self,dic,es=es, my_index="relation2", my_type="relation2"):
        # read data
        """
        load to es
        :param dic:
        :param es:
        :param my_index:
        :param my_type:
        :return:
        """
        md5 = hashlib.md5()
        userid = dic['mainword'] + dic['relaword']
        md5.update(userid)
        doc = {
            # delete,index,create
            # "_op_type": 'update',
            "_index": my_index,
            "_type": my_type,
            "_id": md5.hexdigest(),
            "_source": {
                'main_word': dic['mainword'],
                'include_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'rela_word': dic['relaword'],
                'industry':  "汽车",
                'classfy': dic['classfy'],
                'coefficient':dic['coefficient'],
                'Acoefficient' : dic['Acoefficient'],
                'Bcoefficient' : dic['Bcoefficient'],
                'Ccoefficient' : dic['Ccoefficient'],
                'Dcoefficient': dic['Dcoefficient']
            }
        }
        # 单条写入的方式(
        # es.index(index=my_index,doc_type=my_type,body=doc)
        # 批量处理
        self.actions.append(doc)
        if len(self.actions) >= self._cache_size:
            self.flush()

    def flush(self):
        helpers.bulk(es, self.actions)
        self.actions = []


if __name__ == '__main__':
    #load_data('../data/all_data.xlsx')
    ins = Saver()
    dic = {"question":"求教大众的落地价格是多少","anwser":"15万","product":["大众"],\
           "qword":"多少","attribute":["价格","落地"],"industry":"汽车"}
    ins.pass_data(dic)
    self.flush()







