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


url= "https://you.ctrip.com/sight/Singapore53.html"
driver.get(url)


# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI', 'link', 'num_reviews'])

def parse_reviews(text):
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0


# There are 112 pages of attractions in Ctrip.
for i in range(1,21):


        print("page" + str(i)) #counter to keep track at which page
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down

         #Forming selector path
        sel = Selector(text=driver.page_source)

        sleep(3)

        res = sel.xpath('//div[/html/body/div[4]/div/div[2]/div/div[3]]')
        end_link = '/div[2]/dl/dt/a/@href'
        end_text = '/div[2]/dl/dt/a[@target="_blank"]/@title'
        end_reviews = '/div[2]/ul/li[3]/a[@target="_blank"]/text()'

        #For each page, there are 15 attractions listed
        for a in range (1,20):

            #Forming a string
            xpath_link = 'div[' + str(a) +']' + end_link
            xpath_text = 'div[' + str(a) +']' + end_text
            xpath_reviews = 'div[' + str(a) +']' + end_reviews

            link = res.xpath(xpath_link).extract_first()
            text = res.xpath(xpath_text).extract_first()
            reviews = res.xpath(xpath_reviews).extract_first()
        
            
            poi_df.loc[poi_df.shape[0]] = [text] + [link] + [reviews]



        url1= "https://you.ctrip.com/sight/singapore53/s0-p{}.html?ordertype=11".format(i+1)
        driver.get(url1)


driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("./ctrip/data_output/{}_chinese_ctrip_list.csv".format(today_date))# changed storage position and name_jia
