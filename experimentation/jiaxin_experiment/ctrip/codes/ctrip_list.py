# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from scrapy import Selector

import pandas as pd
import csv
import re
from time import sleep
from datetime import date
from random import random

driver = webdriver.Chrome('./chromedriver')

url= "https://you.ctrip.com/shoppinglist/Singapore53.html"
driver.get(url)


# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI', 'link', 'num_reviews','address'])

def parse_reviews(text):
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0

# There are 240 pages of shopping areas in Ctrip.
for i in range(1,241):
       

        print("page" + str(i)) #counter to keep track at which page    
       # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
         #Forming selector path
        sel = Selector(text=driver.page_source)
        sleep(random())
        
        res = sel.xpath('//div[@class="list_wide_mod2"]')    
        end_link = './/div[2]/dl/dt/a/@href'     
        end_text = './/div[2]/dl/dt/a[@target="_blank"]/@title'
        end_reviews = './/div[2]/ul/li[3]/a[@target="_blank"]/text()'
        end_address='.//div[2]/dl/dd[@class="ellipsis"]/text()'
    
        #For each page, there are 15 attractions listed
        #for a in range (1,16):
        
            #Forming a string
         #   xpath_link = '//div[' + str(a) +']' + end_link   
          #  xpath_text = '//div[' + str(a) +']' + end_text
           # xpath_reviews = '//div[' + str(a) +']' + end_reviews
            #xpath_address = '//div[' + str(a) +']' + end_address
        
        link1 = res.xpath(end_link).getall()     
        text1= res.xpath(end_text).getall()  
        reviews1 = res.xpath(end_reviews).getall() 
        address1= res.xpath(end_address).getall() 
        
        
        for a in range(len(link1)):
            link="https://you.ctrip.com"+str(link1[a])
            text= text1[a]
            reviews=parse_reviews(str(reviews1[a]))
            address=address1[a]
  
            poi_df.loc[poi_df.shape[0]] = [text] + [link] + [reviews] + [address]
        
                
                
        url1= "https://you.ctrip.com/shoppinglist/singapore53/s0-p{}.html".format(i+1)   
        driver.get(url1) 
        

        
driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/aggregate list/{}_chinese_ctrip_list.csv".format(today_date))# changed storage position and name_jia