# -*- coding: utf-8 -*-
# @Author: lancer
# @Date:   2016-08-19 16:20:58
# @Last Modified by:   leven-ls
# @Last Modified time: 2016-08-20 16:32:11
import re
import time
import random
from collections import Counter

from bs4 import BeautifulSoup
import requests
import jieba.analyse

"""
reload sys is always a dangerous chioce
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
TO-DO：
        1. 微博存在反爬虫机制的斗争  1.0. 接入开源IP代理库
                                  1.1. 设置header, UG 

"""


cnt = Counter()

"""
中文分词出来的一些，并不想抓取的词。比如： 不要，的，了 

"""
fuck_off = set([u'\uff0c', u'\u4f60', u'\u7684', u'\uff01', u' ', u'\u4e86', u'\u3002',
                u'\u2550', u'\u662f', u'\u6211', u'\u5bf9', u'\u90fd', u'\u5979', u':',
                u'\uff1f', u'\u4e0d', u'\u5728', u'\u4e5f', u'\u4e5f', u'\u66f0', u'\uff1a',
                u'\u6211\u4eec', u'\u4e00\u4e2a', u'\u4e0d\u8981', u'\u6c38\u8fdc', u'\u4ec0\u4e48',
                u'\u4e0d\u662f', u'\u4e00\u5b9a', u'\u8fd9\u4e2a', u'\u8fd9\u4e48', u'\u76f8\u4fe1',
                u'\u6ca1\u6709', u'\u73b0\u5728', u'\u600e\u4e48'
                ])

"""
过滤：
    1.评论中回复他人部分的代码
    2.评论中的超链接代码
    3.微博表情代码

"""
pattern_list = [re.compile(u'回复<a(.*)</a>'),
                re.compile(u'<a(.*)</a>'),
                re.compile(u'<i(.*)</i>')]


def update_result(comment_item, cnt):
    seg_list = jieba.analyse.extract_tags(comment_item)
    for i in seg_list:
        if i not in fuck_off:
            cnt[i] += 1


def data_cleaning(s, pattern_list):
    pattern_list = pattern_list
    cleanedStr = s
    for p in pattern_list:
        cleanedStr = re.sub(p, '', cleanedStr)
    return cleanedStr



if __name__ = '__main__':

    # 王宝强最后一条微博的评论
    url = "http://m.weibo.cn/single/rcList?format=cards&id=4008168466150722&type=comment&hot=0&page="
    s = requests.Session()

    """
    xrange（ 起始页数， 终止页数）

    """
    for i in xrange(2, 50):
        print 'Now I am digging Page: ',i
        r = s.get(url + str(i))
        try:
            testLst = r.json()[0]["card_group"]
            for i in testLst:
                item = data_cleaning(i["text"], pattern_list)
                update_result(item, cnt)
                print '正在分析句子:',item
        except Exception, e:
            print e
            print r.status_code
            print r.content
            continue

    """
    TO-DO: set up echart to show Data.
    据说word cloud用来展示这类数据不错。

    """
    print cnt.most_common(30)
    for i in cnt.most_common(30):
        print '关键词: ', i[0].encode('utf-8'), '共出现 ', i[1], ' 次'

