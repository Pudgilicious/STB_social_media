#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:18:48 2020

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

url= "https://place.qyer.com/singapore/sight/"
driver.get(url)


# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI','eng_name', 'link', 'num_reviews'])

# There are 24 pages of attractions in QY.
for i in range(1,25):
       

        print("page" + str(i)) #counter to keep track at which page    
        sleep(randint(1,3))
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
         #Forming selector path
        sleep(randint(1,3))
        sel = Selector(text=driver.page_source)
        sleep(randint(1,3))
        
        res = sel.xpath('//div[@class="qyMain fl"]')    
        end_link = '/div/h3/a/@href'     
        end_text = '/div/h3/a[@target="_blank"]/text()'
        end_eng='/div/h3/a[@target="_blank"]/span/text()'
        end_reviews = '/div/div[1]/span[2]/a/text()'
    
        #For each page, there are 15 attractions listed
        for a in range (1,16):
        
            #Forming a string
            xpath_link = '//*[@id="poiLists"]/li[' + str(a) +']' + end_link   
            xpath_text = '//*[@id="poiLists"]/li[' + str(a) +']' + end_text
            xpath_eng = '//*[@id="poiLists"]/li[' + str(a) +']' + end_eng
            xpath_reviews = '//*[@id="poiLists"]/li[' + str(a) +']' + end_reviews
        
            link = res.xpath(xpath_link).extract_first()     #eg. link = res.xpath('div[1]/div/div/div/div[2]/a[@target="_blank"]/@href').extract_first()       
            text = res.xpath(xpath_text).extract_first()  
            eng = res.xpath(xpath_eng).extract_first()  
            reviews = res.xpath(xpath_reviews).extract_first() 
        
        
            poi_df.loc[poi_df.shape[0]] = [text] + [eng] + [link] + [reviews]
                
                
        next_page_button = driver.find_elements_by_xpath('//a[@title="下一页"]')
        if next_page_button:
            sleep(randint(1,3))    
            next_page_button[0].click()  
        else:
            print("Can't click or last page")
            
        sleep(randint(1,5))  
        sel = Selector(text=driver.page_source)
        
driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/aggregate list/{}_qy_list.csv"\
                  .format(today_date))