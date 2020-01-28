#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:49:43 2020

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

url = 'https://place.qyer.com/poi/V2UJY1FlBzZTZFI3/'
#url = 'https://place.qyer.com/poi/V2YJalFkBzBTbA/'
#url = 'https://place.qyer.com/poi/V2EJZVFnBz9TYA/'
#url = 'https://place.qyer.com/poi/V2UJYVFnBzFTYVI9CmQ/'


driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI_CN'])

    
#driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
    #Forming selector path
sleep(randint(1,3))
sel = Selector(text=driver.page_source)
sleep(randint(1,3))
      
    #select areas where we going to extract info
res = sel.xpath('.//div[@class="poi-detail"]')    

    


xpath_summary = '//div[@class="poi-detail"]/div/p/text()'
if res.xpath(xpath_summary).extract_first() != None:
    about_summary=res.xpath(xpath_summary).extract_first() 
else: 
    about_summary='Not Available'
        
        
xpath_add1 = '//li[1]/div[@class="content"]/p/text()' 
xpath_add2 = '//ul[@class="poi-tips"]//div/p/text()'
if res.xpath(xpath_add1).extract_first() != None:
    address=res.xpath(xpath_add1).extract_first()  
else:
    address=res.xpath(xpath_add2).extract_first()

xpath_phone='.//li[./span[contains(text(),"            电话：")]]/div/p/text()'
if res.xpath(xpath_phone).extract_first() != None:
    phone=res.xpath(xpath_phone).extract_first()
else:
    phone='Not Available'

#//*[title="50"]/parent::*
#//li[./span[contains(text(),'Text1')]]

xpath_web = '//li[6]/div[@class="content"]/a/text()' 
if res.xpath(xpath_web).extract_first()!=None:
    website=res.xpath(xpath_web).extract_first() 
else:
    website='Not Available'

#need edit, share same xpath with phone case 2
xpath_trans = '//li[2]/div[@class="content"]/p/text()'   
if res.xpath(xpath_trans).extract_first() != None :
    transportation_mode=res.xpath(xpath_trans).extract_first() 
else:
    transportation='Not Available'
  

xpath_openhr = '//li[3]/div[@class="content"]/p/text()'
if res.xpath(xpath_openhr).extract_first() != None:
    opening_hours=res.xpath(xpath_openhr).extract_first()  
else:
    opening_hours='Not Available'

today = date.today()                                #passed
today_date = today.strftime("%Y%m%d")

poi_df.loc[poi_df.shape[0]] = [phone]

driver.quit()


poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/QY4.1.csv")