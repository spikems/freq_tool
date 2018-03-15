# -*- coding:utf-8 -*-
import re
import os
import xlrd
import xlsxwriter
from QA_Extract import QAExtractWord
from New_QA_Extract import NewQAExtractWord
project_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件夹的路径


def assemble_re_formula(word_str):
    '''
        通过（有#嘛）组装re表达式
    '''
    word_list = word_str.split('#')
    return re.compile(r'(%s).*?(%s)' % (word_list[0], word_list[1]))


def is_include(word, word_list):
    '''
        检验词是否有包含关系
    '''
    for other_word in word_list:
        if word in other_word:
            return True
    return False


def read_dm_data():
    '''
        读取数据库的数据
    '''
    dm_obj = WordsTrend()
    component_word_list = dm_obj.query_component()
    attribute_word_list, attribute_word_dict = dm_obj.query_attribute()
    return component_word_list, attribute_word_list, attribute_word_dict


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


def read_raw_data(path):
    '''
        读取文件的源数据
    '''
    read_data = xlrd.open_workbook(path)
    table = read_data.sheets()[0]
    raw_data = []
    for i in range(1, table.nrows):
        line = table.row_values(i)
        classes = line[0].encode('utf-8').strip().lower() if type(line[0]) == str or type(line[0]) == unicode else str(line[0])
        # first_floor_content = line[1]
        # praise_num = line[2]
        # second_floor_content = line[3]
        # title = line[4].encode('utf-8').strip().lower() if type(line[4]) == str or type(line[4]) == unicode else str(line[4])
        # raw_data.append([classes, first_floor_content, praise_num, second_floor_content, title])
        raw_data.append([classes])
    return raw_data


def filter_word(raw_data, component_word_list, attribute_word_list, attribute_word_dict):
    for data in raw_data:
        had_component_word_list = []  # 标题中包含的组件列表
        for word in component_word_list:
            if word in data[-1]:
                had_component_word_list.append(word)
        had_attribute_word_list = []  # 标题包含属性的列表
        for word in attribute_word_list:
            if word in data[-1]:
                had_attribute_word_list.append(attribute_word_dict[word])
        data.append(had_component_word_list)
        data.append(had_attribute_word_list)
    return raw_data


def filter_query_word(raw_data, common_word_list, re_word_list, query_word_type_dict):
    '''
        过滤疑问词
    '''
    for data in raw_data:
        query_word_list = []  # 标题中的疑问词
        for word in common_word_list:   # 判断普通的词
            if word in data[-1]:
                query_word_list.append(word)
        remove_index_list = []  # 移除包含关系的索引
        for i in range(len(query_word_list)):
            judge_result = is_include(query_word_list[i], query_word_list[0:i] + query_word_list[i+1:])
            if judge_result:
                remove_index_list.append(query_word_list[i])
        for word in remove_index_list:
            query_word_list.remove(word)

        for word in re_word_list:
            re_formula = assemble_re_formula(word)
            if re_formula.search(data[-1]):  # 如果存在  有#吗数据
                query_word_list.append(word)
        #data.append(query_word_list)  # 后面添加的是疑问词
        add_query_type_dict = {}   # 添加疑问词类型
        for word in query_word_list:
            type_word = query_word_type_dict[word][0]
            word_weight = query_word_type_dict[word][1]
            if type_word in add_query_type_dict:   # 如果有这个种类,选取最大值
                if add_query_type_dict[type_word] < word_weight:
                    add_query_type_dict[type_word] = word_weight
            else:  # 如果字典没有这种类型
                add_query_type_dict[type_word] = word_weight
        # 字典排序输出
        sorted_data = sorted(add_query_type_dict.items(), key=lambda item: item[1], reverse=True)
        final_add_list = []
        for s_data in sorted_data:
            result_str = s_data[0] + '(%s)' % (str(s_data[1]))
            final_add_list.append(result_str)
        data.append(final_add_list)  # 后面添加的是疑问词的类型
    return raw_data


def save_data(result_data, save_path):
    workbook = xlsxwriter.Workbook(save_path)
    sheet = workbook.add_worksheet('result')
    sheet.write(0, 0, u'classes')
    # sheet.write(0, 1, u'first_floor_content')
    # sheet.write(0, 2, u'praise_num')
    # sheet.write(0, 3, u'second_floor_content')
    # sheet.write(0, 4, u'title')
    sheet.write(0, 1, u'品牌')
    sheet.write(0, 2, u'车型')
    sheet.write(0, 3, u'组件')
    sheet.write(0, 4, u'属性')
    sheet.write(0, 5, u'评价词')
    sheet.write(0, 6, u'服务词')
    sheet.write(0, 7, u'疑问词')
    i_row = 1
    for data in result_data:
        try:
            sheet.write(i_row, 0, data[0].decode('utf-8') if type(data[0]) == str else data[0])
            sheet.write(i_row, 1, data[1].decode('utf-8') if type(data[1]) == str else data[1])
            sheet.write(i_row, 2, data[2].decode('utf-8') if type(data[2]) == str else data[2])
            sheet.write(i_row, 3, data[3].decode('utf-8') if type(data[3]) == str else data[3])
            sheet.write(i_row, 4, data[4].decode('utf-8') if type(data[4]) == str else data[4])
            sheet.write(i_row, 5, data[5].decode('utf-8') if type(data[5]) == str else data[5])
            sheet.write(i_row, 6, data[6].decode('utf-8') if type(data[6]) == str else data[6])
            sheet.write(i_row, 7, data[7].decode('utf-8') if type(data[7]) == str else data[7])

            i_row += 1
        except:
            print data
    workbook.close()


def save_query_data(result_data, save_path):
    workbook = xlsxwriter.Workbook(save_path)
    sheet = workbook.add_worksheet('result')
    sheet.write(0, 0, u'classes')
    sheet.write(0, 1, u'first_floor_content')
    sheet.write(0, 2, u'praise_num')
    sheet.write(0, 3, u'second_floor_content')
    sheet.write(0, 4, u'title')
    sheet.write(0, 5, u'疑问词')
    i_row = 1
    for data in result_data:
        try:
            sheet.write(i_row, 0, data[0])
            sheet.write(i_row, 1, data[1])
            sheet.write(i_row, 2, data[2])
            sheet.write(i_row, 3, data[3])
            sheet.write(i_row, 4, data[4].decode('utf-8') if type(data[4]) == str else data[4])
            if len(data[5]) > 0:
                sheet.write(i_row, 5, (data[5][0].decode('utf-8') if type(data[5][0]) == str else data[5][0]))
            # for i in range(len(data[5])):
            #     sheet.write(i_row, 5+i, (data[5][i].decode('utf-8') if type(data[5][i]) == str else data[5][i]))
            i_row += 1
        except Exception as e:
            print e
            raw_input('test')
            print data
    workbook.close()


def filter_one_str(data, common_word_list, re_word_list, query_word_type_dict):
    '''
        过滤疑问词
    '''
    query_word_list = []  # 标题中的疑问词
    for word in common_word_list:   # 判断普通的词
        if word in data:
            query_word_list.append(word)
    remove_index_list = []  # 移除包含关系的索引
    for i in range(len(query_word_list)):
        judge_result = is_include(query_word_list[i], query_word_list[0:i] + query_word_list[i+1:])
        if judge_result:
            remove_index_list.append(query_word_list[i])
    for word in remove_index_list:
        query_word_list.remove(word)

    for word in re_word_list:
        re_formula = assemble_re_formula(word)
        if re_formula.search(data):  # 如果存在  有#吗数据
            query_word_list.append(word)
    #data.append(query_word_list)  # 后面添加的是疑问
    for word in query_word_list:
        print word, query_word_type_dict[word][0]


def main():
    # data_path = project_path + '/问题提取的数据.xlsx'
    data_path = project_path + '/疑问词测试.xlsx'
    raw_data = read_raw_data(data_path)
    ext_obj = NewQAExtractWord()
    for data in raw_data:
        brand_word_list, product_word_list, component_word_list, attribute_word_list, evaluation_word_list, \
        service_word_list, query_word = ext_obj.extract_master(data[0], 1)
        data.append('#'.join(brand_word_list))
        data.append('#'.join(product_word_list))
        data.append('#'.join(component_word_list))
        data.append('#'.join(attribute_word_list))
        data.append('#'.join(evaluation_word_list))
        data.append('#'.join(service_word_list))
        data.append(query_word)
    save_path = project_path + '/测试结果.xlsx'
    save_data(raw_data, save_path)
if __name__ == '__main__':
    main()
    # #component_word_list, attribute_word_list, attribute_word_dict = read_dm_data()
    # data_path = project_path + '/qa_data.xlsx'
    # raw_data = read_raw_data(data_path)
    # #result_data = filter_word(raw_data, component_word_list, attribute_word_list, attribute_word_dict)
    # #save_path = project_path + '/result_qa_data.xlsx'
    # #save_data(result_data, save_path)
    # # 过滤疑问词
    # query_path = project_path + '/query_word.xlsx'
    # common_word_list, re_word_list, query_word_type_dict = read_query_data(query_path)
    # result_data = filter_query_word(raw_data, common_word_list, re_word_list, query_word_type_dict)
    # save_path = project_path + '/query_result_data.xlsx'
    # save_query_data(result_data, save_path)

    # # 判断一句话
    # query_path = project_path + '/query_word.xlsx'
    # str = '关于加装日间行车灯属于违法行为吗？'
    # common_word_list, re_word_list, query_word_type_dict = read_query_data(query_path)
    # result_data = filter_one_str(str, common_word_list, re_word_list, query_word_type_dict)