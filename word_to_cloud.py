#!/usr/bin/env python


# -*- coding: utf-8 -*- 

"""
@File: jieba.py

Created on 02 07 18:37 2020

@Authr: zhf12341 from Mr.Zhao

"""


import jieba
import numpy as np
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image
import string
import zhon.hanzi
import jieba.posseg as pseg



"""读取txt文件"""
def open_file(filename):
    with open(filename,"r",encoding = "utf-8") as f:
        content = f.read()
    return content


"""分词"""
def word_split(content, txt):
    #通过词性筛选掉一些无用词
    anword = [x.word for x in pseg.cut(content) if (x.flag.startswith('a') or x.flag.startswith('n')) and x.word not in txt]
    return(str(anword))


"""词云"""
def word_cloud(wordlist,pic):#pic是图片名称
    ground = np.array(Image.open("1.jpg"))
    image_colors = ImageColorGenerator(ground)
    wc = WordCloud(width = 1600,background_color = "white",max_words = 50,mask = ground,scale = 10,max_font_size = 500,random_state = 42,font_path = "msyh.ttc")
    wc.generate(wordlist)
    wc.to_file(pic)
    #plt.imshow(wc,interpolation = "bilinear")
    #plt.axis("off")
    #plt.figure(figsize = (100,100))
    #plt.show()


"""数据清洗"""
def word_clean(wl,txt):
    wl = wl.split()
    for i in wl:
        if i.isdigit() or i in txt or i in zhon.hanzi.punctuation or i in string.punctuation:
            wl.remove(i)
    wl = str(wl).replace("'","")
    wl = wl.replace(",","")
    return wl


"""主程序"""
def main(av):
    filename = "{}.txt".format(av)
    content = open_file(filename)
    word_cloud(word_clean(word_split(content, ""),""),"{}.jpg".format(filename))

if __name__ == "__main__":
    av = 86803884
    main(av)