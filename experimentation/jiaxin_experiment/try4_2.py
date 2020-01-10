#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:58:10 2020

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

#crawl out reviews for Gardens by the bay, Ctrip, 1st page 


driver = webdriver.Chrome('./chromedriver')

url = "https://piao.ctrip.com/ticket/dest/t132782.html"

driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['reviews'])

# There are 28 pages of attractions in Tripadvisor.

driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
    #Forming selector path
sleep(1) 
sel = Selector(text=driver.page_source)
sleep(1)
      
    #//*[@id="FILTERED_LIST"]
res = sel.xpath('//ul[@class="comments"]')    

    
xpath_user_name = './/li/div[@class="user-date"]/span/text()[1]'  
user_name = res.xpath(xpath_user_name).getall()   #a list containing all the names from 1st page of review

xpath_review_time ='.//li/div[@class="user-date"]/span/text()[3]'  
review_time =res.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review

xpath_review='.//li/p/text()'
review=res.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review

xpath_rates='.//li/h4/span/text()[2]'
rates=res.xpath(xpath_rates).getall() #a list containing all the rates from 1st page of review

poi_df.loc[poi_df.shape[0]] = [rates]#for illustration only, changes the variables accordingly
                   
        
driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/trial1.csv")# changed storage position and name_jia

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