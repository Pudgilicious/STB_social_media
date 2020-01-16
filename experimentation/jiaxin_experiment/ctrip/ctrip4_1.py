#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 11:54:03 2020

@author: jia
"""

from selenium import webdriver
from scrapy import Selector
from scrapy.http import HtmlResponse
import pandas as pd
import csv
import re
from time import sleep
from datetime import date

driver = webdriver.Chrome('./chromedriver')

#url = "https://piao.ctrip.com/ticket/dest/t75830.html"
url="https://piao.ctrip.com/ticket/dest/t132782.html"

driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POIs', 'total_reviews','ratings', 'address','opening hours','attributes_crawled time'])

    
    #print("page" + str(i)) #counter to keep track at which page    
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
    #Forming selector path
sleep(1) 
sel = Selector(text=driver.page_source)
sleep(1)
      
    #select areas where we going to extract info
res = sel.xpath('.//div[@class="brief-box clearfix"]')    

xpath_total_reviews = '//a[@data-reactid="58"]/text()'    #passed
total_reviews =res.xpath(xpath_total_reviews).extract_first() 
    
xpath_name = '//h2[@data-reactid="38"]/text()'    #passed 
name=res.xpath(xpath_name).extract_first()   

xpath_rate = '//i[@class="num"]/text()'    #passed
ratings=res.xpath(xpath_rate).extract_first()  

xpath_add = '//span[@data-reactid="45"]/text()'    #passed
address=res.xpath(xpath_add).extract_first()  

xpath_openhr = '//span[@data-reactid="51"]/text()'    #passed
openhr=res.xpath(xpath_openhr).extract_first()  


today = date.today()
today_date = today.strftime("%Y%m%d")

poi_df.loc[poi_df.shape[0]] = [name]+[total_reviews]+[ratings]+[address]+[openhr]+[today_date]

driver.quit()


poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/trial4.1.csv")# changed storage position and name_jia

#Full path examples
#ATTR_ENTRY_2149128 > div > div > div > div.tracking_attraction_photo.photo_booking.non_generic > a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]        #filtered list
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]  #next node 
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[2]/a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[5]
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[3]
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[2]/a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[1]/div/div[1]/div[3]/a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[1]/div/div[1]/div[4]/div[2]/div/span[2]/a