# -*- coding:utf-8 -*-
import os
import xlrd
from read_data import WordsTrend
project_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件夹的路径


def read_dm_data():
    '''
        读取数据库的数据
    '''
    dm_obj = WordsTrend()
    query_list = ['brand', 'product', 'component', 'attribute', 'evaluation', 'service']  # 需要查询的表
    brand_dict, product_dict, component_dict, attribute_dict, evaluation_dict, service_dict = dm_obj.master(query_list)
    return brand_dict, product_dict, component_dict, attribute_dict, evaluation_dict, service_dict


def read_query_data(path):
    '''
        读取疑问词数据
    '''
    read_data = xlrd.open_workbook(path)
    table = read_data.sheets()[0]
    common_word_list = []   # 普通词的列表
    re_word_list = []   # 需要通过正则匹配的数据
    query_word_type_dict = {}  # 格式：   query_word:所属类型
    for i in range(1, table.nrows):
        line = table.row_values(i)
        word = line[0].encode('utf-8').strip().lower() if type(line[0]) == str or type(line[0]) == unicode else \
            str(line[0])
        word_type = line[1].encode('utf-8').strip().lower() if type(line[1]) == str or type(line[1]) == unicode else \
            str(line[1])
        word_weight = int(line[2])
        if '#' in word:
            re_word_list.append(word)
        else:
            common_word_list.append(word)
        query_word_type_dict[word] = [word_type,word_weight]
    return common_word_list, re_word_list, query_word_type_dict

if __name__ == '__main__':
    path = (project_path + '/conf/query_word.xlsx')
    common_word_list, re_word_list, query_word_type_dict = read_query_data(path)
    brand_dict, product_dict, component_dict, attribute_dict, evaluation_dict, service_dict = read_dm_data()
    result_list = []
    result_list.extend(common_word_list)
    result_list.extend(brand_dict.keys())
    result_list.extend(product_dict.keys())
    result_list.extend(component_dict.keys())
    result_list.extend(attribute_dict.keys())
    result_list.extend(evaluation_dict.keys())
    result_list.extend(service_dict.keys())
    result_list = list(set(result_list))
    with open('words_dict.txt','w') as f:
        for word in result_list:
            f.write(word)
            f.write('\n')
