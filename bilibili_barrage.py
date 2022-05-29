#!/usr/bin/env python

# -*- coding: utf-8 -*- 

"""
@File: bilibili_barrage.py

Created on 02 07 23:27 2020

@Authr: zhf12341 from Mr.Zhao

"""

import json
import parsel
import requests
from lxml import html
import word_to_cloud
from bs4 import BeautifulSoup
import re


class bilibili:

    @classmethod
    def get_aid(cls, bv, headers):
        page_url = f'https://www.bilibili.com/video/{bv}'
        response = requests.get(url=page_url, headers=headers).text
        pattern = re.compile(f'"aid":(\d+?),"bvid":"{bv}"')  # 查找数字
        av = pattern.findall(response)
        if len(av) == 0:
            raise ValueError("没找到对应的AV")
        return av[0]

    # 从pagelist里面找到该视频的弹幕文件cid编号，其中pagelist根据视频av号来定位
    @classmethod
    def get_cid(cls, av, headers):
        page_url = 'https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp'.format(av)
        response = requests.get(url=page_url, headers=headers).content
        html = json.loads(response)
        cid = html['data'][0]['cid']
        return cid

    @classmethod
    # 根据cid编号找到弹幕文件
    def get_barrage(cls, cid, headers):
        barrage_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
        response = requests.get(url=barrage_url, headers=headers)
        xml = parsel.Selector(response.content.decode('utf-8'))
        barrage_list = xml.xpath('//d').re('<d.*> *(.*)</d>')

        return barrage_list

    @classmethod
    # 把弹幕写入到文件中
    def save_file(cls, barrage_list, filename):
        with open(filename, mode='a', encoding='utf-8') as f:
            for barrage in barrage_list:
                f.write(barrage)
                f.write('\n')

    @classmethod
    def crawler(cls, bid, headers):
        aid = cls.get_aid(bid, headers)
        cid = cls.get_cid(aid, headers)
        barrage_list = cls.get_barrage(cid, headers)
        cls.save_file(barrage_list, '{}.txt'.format(bid))


if __name__ == '__main__':
    bv = 'BV1hE411V77S'  # input('请输入您想爬取视频的av号，例如86803884等： ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    bilibili.crawler(bv, headers)
    word_to_cloud.main(bv)
