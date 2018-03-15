# -*- coding:utf-8 -*-
import os
import xlrd
import xlsxwriter

current_project_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件夹路径
path = current_project_path + '/测试结果.xlsx'
raw_data = xlrd.open_workbook(path)
table = raw_data.sheets()[0]
all_data_list = []      # 存放所有数据的关键词数据
for i in range(1, table.nrows):
    line = table.row_values(i)
    one_key_words_list = []   # 存放单条数据的关键词
    component_word_list = line[3].strip().split('#')
    attribute_word_list = line[4].strip().split('#')
    evaluation_word_list = line[5].strip().split('#')
    service_word_list = line[6].strip().split('#')
    query_word = line[7].strip()
    for data_list in [component_word_list, attribute_word_list, evaluation_word_list]:
        for word in data_list:
            if word.strip():
                one_key_words_list.append(word.strip())
    for word in service_word_list:
        if word.strip():
            if word.strip() in [u'首保', u'二保', u'三保', u'四保']:
                one_key_words_list.append(u'保养')
            else:
                one_key_words_list.append(word.strip())
    if query_word.strip():
        one_key_words_list.append(query_word.strip())
    one_key_words_list = list(set(one_key_words_list))  # 将关键词去重
    one_key_words_list.sort()   # 将关键词排序
    if one_key_words_list:   # 有可能某条数据什么也提取不出来
        all_data_list.append(one_key_words_list)
data_times_dict = {}  # 统计每条数据的出现次数
for data in all_data_list:
    str_data = u'、'.join(data)
    data_times_dict[str_data] = data_times_dict.get(str_data, 0) + 1
sort_data_times = sorted(data_times_dict.items(), key=lambda x: x[1], reverse=True)

# 输出到excel中
save_path = current_project_path + '/TOP_N统计.xlsx'
workbook = xlsxwriter.Workbook(save_path)
sheet = workbook.add_worksheet('TOP_N')
sheet.write(0, 0, u'关键词组合')
sheet.write(0, 1, u'统计次数')
row = 1
for data, num in sort_data_times:
    sheet.write(row, 0, data)
    sheet.write(row, 1, num)
    row += 1
workbook.close()
