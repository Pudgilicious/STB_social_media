#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 11:05:01 2020

@author: jia
"""

import pandas as pd
import numpy as np
import os
import string
from string import digits
#separa
import jieba
import jieba.posseg as pseg
import re
from os import path
import jieba.analyse as analyse
#wordcloud
from PIL import Image
import numpy as  np
import matplotlib.pyplot as plt
#词云生成工具
from wordcloud import WordCloud,ImageColorGenerator
#需要对中文进行处理
import matplotlib.font_manager as fm
jieba.enable_paddle() #启动paddle模式。 0.40版之后开始支持，早期版本不支持
os.getcwd()


#inout data and change to string
os.chdir('/home/jia/Desktop/git/STB_social_media_analytics/ctrip/200216_102752/reviews')
data=pd.read_csv('./1.csv')

#read all the review files
path = '/home/jia/Desktop/git/STB_social_media_analytics/ctrip/200216_102752/reviews'
for i in range(2,519):
    try:
        data=data.append(pd.read_csv(path+'/{}.csv'.format(i)))
    except:
        print(str(i)+' not exist')
        continue
    
    
data=data.drop(['REVIEW_INDEX','WEBSITE_INDEX','POI_INDEX','REVIEWER_NAME','REVIEW_RATING','REVIEW_DATE',
                'REVIEW_TIME','ATTRIBUTES_CRAWLED_TIME'],axis=1)
string1=list(map(lambda x: str(x),data['REVIEW_BODY']))

#inout data and change to string
os.chdir('/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/descriptive_stats')
stop=pd.read_csv('./stop_words.txt',header=None,index_col=False)
stop=list(stop.iloc[:,0])
#print(stop)
#remove stop words and separate text
def jiebaclearText(text,stoplist):
    mywordlist = []
    seg_list = pseg.cut(text, use_paddle=True)
    for word, flag in seg_list:
        if flag in ['v','nz','ns','LOC','ORG','vd','vn','n','LOC']:
            if word not in stoplist:
                mywordlist.append(word)
    #liststr="/ ".join(seg_list)
    #f_stop_seg_list=stop.split('\n')
    #for myword in liststr.split('/'):
     #   if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
      #      mywordlist.append(myword)
    return ' '.join(mywordlist)


pos=[]
for i in range(len(string1)):
    pos.append(jiebaclearText(string1[i],stop))

    
text1=' '.join(pos)


wc=WordCloud(scale=float,
    background_color="white",
    max_words=100,
    max_font_size=60,
    random_state=42,
    font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'   #allow system to output chinese
    ).generate(text1)

#plt.imshow(wc,interpolation="bilinear")
#plt.axis("off")
#plt.show()
#plt.axis("off")
#plt.show()

wc.to_file('./pic2.png')

