# coding:utf-8
import pymysql as mdb
import datetime
import sys
import traceback
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf8')
# conn = mdb.connect(host='192.168.241.45', port=3306, user='dm_base', passwd='dm_base#478UUU', db='dm_base',charset='utf8')
conn = mdb.connect(host='192.168.241.45', port=3306, user='oopin', passwd='OOpin2007Group', db='cognitive_phrases',
                   charset='utf8')
cur = conn.cursor()

# topic_date = (datetime.datetime.now() + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def all_use(value1,value2,value3):
    sql = 'insert into QuestionWord(question_word,type,weight) values(%s,%s,%s)'
    print sql
    try:
        cur.execute(sql,(value1,value2,value3))
        conn.commit()
    except mdb.IntegrityError, e:
        print 'dup'

def read_file(filename):
    with open(sys.argv[1], 'rb') as inf:
        for line in inf:
            linef = line.strip().split('：')
            if line.strip():
                type = linef[0].strip().encode('utf-8', 'ignore')
                words = linef[1].strip().split('、')
                for word in words:
                    all_use(word,type)

def read_excel(filename):
    df = pd.read_excel(filename)
    num = -1
    for question in df[u'疑问词']:
        num+=1
        all_use(df[u'疑问词'][num],df[u'词类别'][num],int(df[u'权重'][num]))

if __name__ == '__main__':
    read_excel(sys.argv[1])
    conn.close()
