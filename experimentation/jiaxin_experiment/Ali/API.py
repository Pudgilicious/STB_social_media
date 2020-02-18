#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:42:08 2020

@author: jia
"""

import pandas as pd
from scrapy import Selector
import os
import re
import utils
from time import sleep
import traceback
from selenium import webdriver
from datetime import datetime
from urllib.parse import unquote
import socket


df=pd.read_csv('./14.csv')

#get API URL
def API_URL(text):
    return 'http://161.117.205.162:8082/social/text?text=<'+str(text)+'>'        
url= list(map(lambda x: API_URL(x),df['REVIEW_BODY']))

index=list(range(len(df['REVIEW_BODY'])))
#input dataframe of reviews
review_df=pd.DataFrame({'REVIEW_INDEX':index,
                        'REVIEWS':df['REVIEW_BODY'], 
                        'API_URL':url})

#create output dataframe
sentiment_col_names=['REVIEW_INDEX',
                     'OVERALL',
                     'ASPECTS',
                     'ASPECTS_POLARITIES',
                     'POLARITY_DIST: CONSUMPTION',
                     'POLARITY_DIST: ENVIRONMENT',
                     'POLARITY_DIST: F&B',
                     'POLARITY_DIST: HYGIENE',
                     'POLARITY_DIST: SAFETY',
                     'POLARITY_DIST: SERVICE',
                     'POLARITY_DIST: SHOPPING',
                     'POLARITY_DIST: SIGHTSEEING',
                     'POLARITY_DIST: TRANSPORTATION',
                     'ASP_NEG_RIO',
                     'ASP_NEU_RIO',
                     'ASP_POS_RIO',
                     'REV_NEG_RIO',
                     'REV_NEU_RIO',
                     'REV_POS_RIO',
                     'TOTAL_ASPECTS'
                    ]
sentiment_df = pd.DataFrame(columns=sentiment_col_names)
datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
sentiment_df.to_csv('./{}_sentiment.csv'.format(datetime_string),mode='a', index=False)


socket.setdefaulttimeout(None) 
driver = webdriver.Chrome('./chromedriver')
#loop to get output of API
review_count=0
while len(review_df.index) > 0 :
    current_index=review_df.iloc[0][0]
    current_url=review_df.iloc[0][2]
    print('######################review {}###########################\n'.format(review_count))
    review_count+=1
    #get API output
    driver.get(current_url)

    sel = Selector(text=driver.page_source)
    code =driver.find_element_by_xpath('/html/body')
    
    #decoding
    decode = unquote(code.text)
    
    
    #parse decoded url
    review_index= current_index
    overall=decode[decode.find("overall")+11:decode.find("polarities")-4]
    aspects=decode[decode.find("aspects")+9:decode.find("overall")-2]
    aspect_polarities=decode[decode.find("polarities")+12:decode.find("sentence")-2]
    consumption=decode[decode.find("consumption")+13:decode.find("environment")-2]
    environment=decode[decode.find("environment")+13:decode.find("fB")-2]
    f_b=decode[decode.find("fB")+4:decode.find("hygiene")-2]
    hygiene=decode[decode.find("hygiene")+9:decode.find("safty")-2]
    safety=decode[decode.find("safty")+7:decode.find("service")-2]
    service=decode[decode.find("service")+9:decode.find("shopping")-2]
    shopping=decode[decode.find("shopping")+10:decode.find("sigtseeing")-2]
    sightseeing=decode[decode.find("sigtseeing")+13:decode.find("transportation")-2]
    transportation=decode[decode.find("transportation")+16:decode.find("detail")-3]
    asp_neg_rio=decode[decode.find("asp_neg_rio")+14:decode.find("asp_neu_rio")-3]
    asp_neu_rio=decode[decode.find("asp_neu_rio")+14:decode.find("asp_pos_rio")-3]
    asp_pos_rio=decode[decode.find("asp_pos_rio")+14:decode.find("rev_neg_rio")-3]
    rev_neg_rio=decode[decode.find("rev_neg_rio")+14:decode.find("rev_neu_rio")-3]
    rev_neu_rio=decode[decode.find("rev_neu_rio")+14:decode.find("rev_pos_rio")-3]
    rev_pos_rio=decode[decode.find("rev_pos_rio")+14:decode.find("total_asp")-3]
    total_aspects=decode[decode.find("total_asp")+12:decode.find("total_rev")-3]
    
    sentiment_output=[review_index,
                      overall,
                      aspects,
                      aspect_polarities,
                      consumption,
                      environment,
                      f_b,
                      hygiene,
                      safety,
                      service,
                      shopping,
                      sightseeing,
                      transportation,
                      asp_neg_rio,
                      asp_neu_rio,
                      asp_pos_rio,
                      rev_neg_rio,
                      rev_neu_rio,
                      rev_pos_rio,
                      total_aspects
                      ]
    
    sentiment_dict = dict(zip(sentiment_col_names,sentiment_output))
    sentiment_df = sentiment_df.append(sentiment_dict, ignore_index=True)
    review_df = review_df.iloc[1:]

sentiment_df.to_csv('./{}_sentiment.csv'.format(datetime_string),
                    mode='a', 
                    header=False,
                    index=False)
driver.quit()

