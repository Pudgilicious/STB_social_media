#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 18:05:35 2020

@author: jia
"""
import pandas as pd
import mysql.connector
from scrapy import Selector
import os
import re
import yaml
from time import sleep
import traceback
from random import random
from selenium import webdriver
from datetime import datetime, date, timedelta
from random import random
from scrapy.linkextractors import LinkExtractor


poi_index = [1,2, 3]
poi_name = ['Orchard Road',
                '千灯寺',
                'Universal Studio Singapore'
               ]
poi_url = ['https://you.ctrip.com/sight/singapore53/108118.html',
               'https://you.ctrip.com/sight/singapore53/4897030.html',
               'https://piao.ctrip.com/ticket/dest/t75830.html']
poi_df = pd.DataFrame({'poi_index':poi_index, 
                           'poi_name':poi_name, 
                           'poi_url':poi_url})
    
driver = webdriver.Chrome('./chromedriver')



for _, row in poi_df.iterrows():
        print('########## {} ##########'.format(row['poi_name']))
        # Create <POI_INDEX>.csv in reviews and reviewers folders.
        current_poi_index = row['poi_index']       
        driver.get(row['poi_url'])
        sel = Selector(text=driver.page_source)
        sleep(1+random()*2)
        current_url= driver.current_url
        print(current_url)
        if current_url == 'https://you.ctrip.com/':
            print('excuting')
            log_file = open('./ctrip/log.txt', 'a+')
            log_file.write('{}, {}, {}\n, {}'.format(row['poi_index'],
                                                               row['poi_name'],
                                                               datetime.now(),
                                                               'current POI does not exist'))
            continue
        
            print('trailtrialtrial!!!!')
        
        
        
        ####################################################################################################
print(current_url.dtype)