#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:45:37 2019

@author: kevin
"""
import urllib.parse
import base64
import requests
from bs4 import BeautifulSoup

class PChomeCrawler(object):

    def __init__(self, keyword):
        self.kwd = keyword

    def _get_lang_type(self):
        if self.kwd.encode('utf-8').isalpha():
            return "Eng"
        else:
            return "Chi"

    def _transform_encoding(self):
        lang_type = self._get_lang_type()
        if lang_type == 'Chi':
            kwd_tmp = urllib.parse.quote(self.kwd)
            self.kwd_encode = str(base64.b64encode(bytes(kwd_tmp, 'big5')), 'utf-8')
        else:
            self.kwd_encode = str(base64.b64encode(bytes(self.kwd, 'utf-8')), 'utf-8')
        return self.kwd_encode

    def crawl(self):
        head = 'https://www.pcstore.com.tw/adm/psearch.htm'
        kwd_trans = self._transform_encoding()
        payload = {
                'store_k_word':kwd_trans,
                'slt_k_option':'1'
                }
        req = requests.get(head, params=payload)
        req.encoding = 'big5'
        soup = BeautifulSoup(req.text, 'html.parser')
        title_unparse_ls = soup.select('div.pic2t.pic2t_bg')
        title_ls = []
        for title in title_unparse_ls:
            title_ls.append(title.text)
        return title_ls

if __name__=='__main__':
    keyword = input('keyword :')
    a = PChomeCrawler(keyword)
    result = a.crawl()
    print(result)