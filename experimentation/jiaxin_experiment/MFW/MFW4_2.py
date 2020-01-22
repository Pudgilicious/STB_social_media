#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:27:38 2020

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
from selenium.common.exceptions import NoSuchElementException 
from random import randint  
#crawl out reviews for Gardens by the bay, Ctrip, 1st page 


driver = webdriver.Chrome('./chromedriver')

#test out 2 cases, 2 different web structure
url = "https://www.mafengwo.cn/poi/5422487.html"   #MFW Gardens by the Bay
#url= "https://www.mafengwo.cn/poi/11057.html"     #MFW Orchard Road

driver.get(url)
driver.maximize_window()
# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['user_name'])

# There are 5 pages of review in MFW for gardens by the bay
for i in range(1,6):
    
    print("page" + str(i)) #counter to keep track at which page    
  
    driver.execute_script('window.scrollTo(0,4500)')  #To scroll down
    #Forming selector path
    sleep(randint(1,4)) 
    sel = Selector(text=driver.page_source)
    sleep(randint(1,3)) 
    
    #selecting review list
    res = sel.xpath('//div[@class="_j_commentlist"]')    
    
   
    xpath_reviewer_url= './/a[@class="avatar"]/@href' #passed
    reviewer_url=res.xpath(xpath_reviewer_url).getall()   #a list containing all the user_url from 1st page of review
        
    xpath_rating= '//li[@class="rev-item comment-item clearfix"]/span/@class'   #passed
    rating_pre=res.xpath(xpath_rating).getall()   #a list containing all the rating from 1st page of review
    rating =list(map(lambda x :str(x)[-1], rating_pre ))
    
    xpath_review_time ='//li/span[@class="time"]/text()'     #passed
    review_time =res.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review
    
    xpath_review_title='//span[@class="from"]/a/@href'    #passed
    if res.xpath(xpath_review_title).getall() != []:
        review_title = res.xpath(xpath_review_title).getall()
    else:
        review_title='NA'    #a list containing where the review is from
        
    xpath_review='//li/p[@class="rev-txt"]/text()'   #passed
    review=res.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review

   

    poi_df.loc[poi_df.shape[0]] = [review]  #for illustration only, changes the variables accordingly
  
    next_page_button = driver.find_elements_by_xpath('//a[@title="后一页"]')
    if next_page_button :
        sleep(randint(1,3)) 
        next_page_button[0].click()  
        sel = Selector(text=driver.page_source)
    else:
        print("Can't click or last page")
        
        
sleep(randint(1,3)) 
sel = Selector(text=driver.page_source)
        
                   
        
driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/MFW.csv")