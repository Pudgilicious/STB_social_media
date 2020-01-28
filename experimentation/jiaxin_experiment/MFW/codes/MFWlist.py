#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:55:44 2020

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

url= "https://www.mafengwo.cn/jd/10754/gonglve.html"
driver.get(url)
driver.maximize_window()

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI', 'link'])

# There are 20 pages of attractions in QY.
for i in range(1,3):
       

        print("page" + str(i)) #counter to keep track at which page    
        driver.execute_script('window.scrollTo(0, 2800)')  #To scroll down
    
         #Forming selector path
        sleep(randint(1,3)) 
        sel = Selector(text=driver.page_source)
        sleep(randint(1,3)) 
        
        res = sel.xpath('//div[@data-cs-p="全部景点"]')    
        end_link = '/a[@target="_blank"]/@href'     
        end_text = '/a[@target="_blank"]/h3/text()'
    
        #For each page, there are 20 attractions listed
        for a in range (1,16):
        
            #Forming a string
            xpath_link = '//div[@class="bd"]/ul/li[' + str(a) +']' + end_link   
            xpath_text = '//div[@class="bd"]/ul/li[' + str(a) +']' + end_text
           
        
            link = res.xpath(xpath_link).extract_first()     #eg. link = res.xpath('div[1]/div/div/div/div[2]/a[@target="_blank"]/@href').extract_first()       
            text = res.xpath(xpath_text).extract_first()  
        
        
        
            if link:     #If link exist   
                poi_df.loc[poi_df.shape[0]] = [text] + [link]                  
            else:
                print("can't write")
                
        next_page_button = driver.find_elements_by_xpath('//a[@title="后一页"]')
        if next_page_button:          
            sleep(randint(1,3)) 
            next_page_button[0].click()  
            sel = Selector(text=driver.page_source)
        else :
            print("Can't click or last page")
        
        sleep(randint(1,3)) 
        sel = Selector(text=driver.page_source)
            
 
driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/trialMFWlist.csv")