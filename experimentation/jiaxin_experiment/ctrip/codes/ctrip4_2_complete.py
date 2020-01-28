#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:16:15 2020

@author: jia
"""

from selenium import webdriver
from scrapy import Selector
from scrapy.http import HtmlResponse
import pandas as pd
import csv
import re
from time import sleep
import datetime
from random import randint


#crawl out reviews for Gardens by the bay, Ctrip, 1st page 


driver = webdriver.Chrome('./chromedriver')

#url = "https://piao.ctrip.com/ticket/dest/t132782.html"
url="https://piao.ctrip.com/ticket/dest/t75830.html"

driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['user_name'])

# There are 302 pages of review in Ctrip.
for i in range(1,3):
    
    print("page" + str(i)) #counter to keep track at which page    
    #driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
    #Forming selector path
    sleep(randint(1,3))
    sel = Selector(text=driver.page_source)
    sleep(randint(1,3))
      
    #//*[@id="FILTERED_LIST"]
    res = sel.xpath('//div[@class="content-wrapper clearfix"]')    
    res1=sel.xpath('//div[@class="weibocombox"]')
    
    if res:
        xpath_user_name = './/li/div[@class="user-date"]/span/text()[1]'  
        user_name = res.xpath(xpath_user_name).getall()   #a list containing all the names from 1st page of review

        xpath_review_time ='.//li/div[@class="user-date"]/span/text()[3]'  
        review_time =res.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review
        def parse_review_date(time_string):
            return datetime.datetime.strptime(time_string[0:10],"%Y-%m-%d").strftime("%Y-%m-%d")
        review_date= list(map(parse_review_date,review_time))

        xpath_review='.//li/p/text()'
        review=res.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review
    
        xpath_rates='.//li/h4/span/text()[2]'
        rates=res.xpath(xpath_rates).getall() #a list containing all the rates from 1st page of review
        
    else:
        xpath_user_name = './/a[@itemprop="author"]/text()'  
        user_name = res1.xpath(xpath_user_name).getall()   #a list containing all the names from 1st page of review

        xpath_review_time ='.//em[@itemprop="datePublished"]/text()'  
        review_time =res1.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review
        

        xpath_review='.//span[@class="heightbox"]/text()'
        review=res1.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review
    
        xpath_rates='.//span[@class="starlist"]/span/@style'
        rates=res1.xpath(xpath_rates).getall()

    poi_df.loc[poi_df.shape[0]] = [rates]#for illustration only, changes the variables accordingly


    next_page_button = driver.find_elements_by_xpath('//a[@class="down  "]')
    if next_page_button :
        sleep(randint(1,3))
        next_page_button[0].click()  
        sel = Selector(text=driver.page_source)
    else:
        print("Can't click or last page")
        

        
                   
        
driver.quit()

#Write out as data-frame with date
#today = date.today()
#today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/trial3.csv")# changed storage position and name_jia

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