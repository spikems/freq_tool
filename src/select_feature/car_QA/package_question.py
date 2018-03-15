# -*- coding:utf-8 -*-
import re
import os
import xlrd
import xlsxwriter
from read_data import WordsTrend
from conf.extract_word_conf import singleton
from conf.extract_word_conf import is_include
from conf.extract_word_conf import remove_include_words
project_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件夹的路径


# QA系统的提取关键词部分
@singleton
class PackQues(object):
    def __init__(self):
        self.brand_dict, self.product_dict, self.component_dict, self.attribute_dict = self.read_dm_data()  # 读取数据库数据
        # self.common_word_list, self.re_word_list, self.query_word_type_dict = self.read_query_data(path=(project_path + '/conf/query_word.xlsx'))
        # self.re_formula_dict = self.assemble_re_formula()

    @staticmethod
    def read_dm_data():
        '''
            读取数据库的数据
        '''
        dm_obj = WordsTrend()
        query_list = ['brand', 'product', 'component', 'attribute']  # 需要查询的表
        brand_dict, product_dict, component_dict, attribute_dict = dm_obj.master(query_list)
        return brand_dict, product_dict, component_dict, attribute_dict

    def add_component(self, str_com_list):
        save_data = []
        for str_com in str_com_list:
            for product in self.product_dict:
                pack_str = product + ', ' + str_com
                save_data.append(pack_str)
        return save_data

    def save_data(self, result_data, save_path):
        workbook = xlsxwriter.Workbook(save_path)
        sheet = workbook.add_worksheet('result')
        sheet.write(0, 0, u'问题组装')
        i_row = 1
        for data in result_data:
            try:
                sheet.write(i_row, 0, data.decode('utf-8') if type(data) == str else data)
                i_row += 1
            except:
                print data
        workbook.close()

    def extract_master(self, question, class_type):
        str_com_list = ['保养#什么', '保养#注意什么', '保养#怎么办', '保养#多久', '保养#多少钱', '保养#多少#机油', '保养#什么#机油',
                        '保养#多少#公里', '首保#什么', '首保#怎么办', '首保#多久', '首保#多少钱', '首保#多少#机油', '首保#什么#机油',
                        '首保#多少#公里', '二保#什么', '二保#怎么办', '二保#多久', '二保#多少钱', '二保#多少#机油', '二保#什么#机油',
                        '二保#多少#公里', '三保#什么', '三保#怎么办', '三保#多久', '三保#多少钱', '三保#多少#机油', '三保#什么#机油',
                        '三保#多少#公里']
        result_data = self.add_component(str_com_list)
        save_path = project_path + '/result_package_保养.xlsx'
        self.save_data(result_data, save_path)

if __name__ == '__main__':
    ext_obj = PackQues()
    question = '大众汽车为何总漏油?'
    ext_obj.extract_master(question, 1)
