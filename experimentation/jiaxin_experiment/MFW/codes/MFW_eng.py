# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import mysql.connector
from scrapy import Selector
import re
import yaml
import csv
from random import random
from selenium import webdriver
from datetime import datetime, date, timedelta
from time import sleep
from random import randint,random

driver = webdriver.Chrome('./chromedriver')
poi_df = pd.DataFrame(columns=['url','eng_name','cn_names','num_reviews'])



poi=pd.read_csv('/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/MFW/trialMFWlist.csv')
poi_list=poi.values.tolist()


for i in range(181,184):
    url = "https://www.mafengwo.cn"+str(poi_list[i][2]) 
    driver.get(url)
    sleep(1+random()*2)
    sel = Selector(text=driver.page_source)
    res = sel.xpath('//div[@class="row row-top"]') 
     
    xpath_eng='//div[@class="en"]/text()'
    eng=res.xpath(xpath_eng).extract_first()
    
    if xpath_eng != None:
        xpath_cn='//div[@class="title"]/h1/text()'
        cn=res.xpath(xpath_cn).extract_first()

        xpath_num='//li[@data-scroll="commentlist"]/a/span/text()'
        num_of_reviews=res.xpath(xpath_num).extract_first()
    
    else:
        sleep(1+random()*2)
        sel = Selector(text=driver.page_source)
        res1=  sel.xpath('//div[@class="m-box m-details clearfix"]')
        
        xpath_eng='//div[@class="t"]/text()'
        eng=res1.xpath(xpath_eng).extract_first()
    
        xpath_cn='//div[@class="title"]/h1/text()'
        cn=res1.xpath(xpath_cn).extract_first()

        xpath_num='//p[@class="ranking"]/em/text()'
        num_of_reviews=res1.xpath(xpath_num).extract_first()
    
    poi_df.loc[poi_df.shape[0]] = [url]+[eng]+[cn]+[num_of_reviews]

driver.quit()
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/test1.csv")


