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
import word_to_cloud


# 从pagelist里面找到该视频的弹幕文件cid编号，其中pagelist根据视频av号来定位
def get_cid(av, headers):
    page_url = 'https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp'.format(av)
    response = requests.get(url=page_url, headers=headers).content
    html = json.loads(response)
    cid = html['data'][0]['cid']
    return cid


# 根据cid编号找到弹幕文件
def get_barrage(cid, headers):
    barrage_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
    response = requests.get(url=barrage_url, headers=headers)
    xml = parsel.Selector(response.content.decode('utf-8'))
    barrage_list = xml.xpath('//d').re('<d.*> *(.*)</d>')

    return barrage_list


# 把弹幕写入到文件中
def save_file(barrage_list, filename):
    with open(filename, mode='a', encoding='utf-8') as f:
        for barrage in barrage_list:
            f.write(barrage)
            f.write('\n')


def main(av, headers):
    cid = get_cid(av, headers)
    barrage_list = get_barrage(cid, headers)
    save_file(barrage_list, '{}.txt'.format(av))


if __name__ == '__main__':
    av = input('请输入您想爬取视频的av号，例如86803884等： ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    main(av, headers)
    word_to_cloud.main(av)
