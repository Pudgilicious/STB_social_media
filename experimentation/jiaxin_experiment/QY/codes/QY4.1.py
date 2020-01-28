#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 09:06:51 2020

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
from random import randint

driver = webdriver.Chrome('./chromedriver')

url = ""


driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI_CN', 'POI_ENG', 'total_reviews','about_summary','ranking','ticket-info','ratings', 
                               'address','phone','website','transportations_mode','opening_hours',
                               'attributes_crawled_time'])

    
#driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
    #Forming selector path
sleep(randint(1,3))
sel = Selector(text=driver.page_source)
sleep(randint(1,3))
      
    #select areas where we going to extract info
res = sel.xpath('.//div[@class="poi-detail"]')    

    
xpath_name_eng = '//h1[@class="en"]/a/text()'      #passed
name_eng =res.xpath(xpath_name_eng).extract_first()   

xpath_name_cn = '//h1[@class="cn"]/a[@class="fontYaHei"]/text()'   #passed
name_cn =res.xpath(xpath_name_cn).extract_first()

xpath_tot_reviews = '//a[@data-bn-ipg="place-poi-detail-viewAllReviews"]/text()'     #passed
total_reviews=res.xpath(xpath_tot_reviews).extract_first() 

xpath_summary = '//div[@class="poi-detail"]/div/p/text()'     #passed
about_summary=res.xpath(xpath_summary).extract_first() 

xpath_ranking = '//li[@class="rank"]/span/text()'     #passed
ranking=res.xpath(xpath_ranking).extract_first() 

xpath_ticket = '//li/a/div/span[@class="price fontYaHei"]/em/text()' 
if res.xpath(xpath_ticket).extract_first() != None:
    ticket_info=int(res.xpath(xpath_ticket).extract_first() )
else:
    ticket_info = str(None)


xpath_rate = '//span[@class="number"]/text()'    #passed
ratings=res.xpath(xpath_rate).extract_first()
 def parse_rate(rate_string):
        return int(rate_string.replace(' ', ''))
rating=    

xpath_add = '//li[1]/div[@class="content"]/p/text()'   #passed
address=res.xpath(xpath_add).extract_first()  

xpath_phone = '//li[5]/div[@class="content"]/p/text()'    #passed 
phone=res.xpath(xpath_phone).extract_first() 


xpath_web = '//li[6]/div[@class="content"]/a/text()'     
website=res.xpath(xpath_web).extract_first() 

xpath_trans = '//li[2]/div[@class="content"]/p/text()'     
transportation_mode=res.xpath(xpath_trans).extract_first() 
  

xpath_openhr = '//li[3]/div[@class="content"]/p/text()'   #passed
openhr=res.xpath(xpath_openhr).extract_first()  

today = date.today()                                #passed
today_date = today.strftime("%Y%m%d")

poi_df.loc[poi_df.shape[0]] = [name_cn]+[name_eng]+[total_reviews]+[about_summary]+[ranking]+[ticket_info]+[ratings]\
                              +[address]+[phone]+[website]+[transportation_mode]+[openhr]+[today_date]

driver.quit()


poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/QY4.1.csv")