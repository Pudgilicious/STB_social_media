#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:31:31 2020

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
from selenium.common.exceptions import NoSuchElementException 
from random import random  


driver = webdriver.Chrome('./chromedriver')

#test out 2 cases, 2 different web structure
url = "https://www.mafengwo.cn/poi/5422487.html"   #MFW Gardens by the Bay
#url= "https://www.mafengwo.cn/poi/11057.html"     #MFW Orchard Road

driver.get(url)
driver.maximize_window()
# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['user_name'])

#good reviews
good_reviews= driver.find_elements_by_xpath('//li[@data-category="13"]/a')
driver.execute_script("arguments[0].click()",good_reviews[0])

for i in range(1,6):
    
    print("page" + str(i)) #counter to keep track at which page    
  
    driver.execute_script('window.scrollTo(0,4500)')  #To scroll down
    #Forming selector path
    sleep(1+random()*2)
    sel = Selector(text=driver.page_source)
    sleep(1+random()*2)
    
    #selecting review list
    res = sel.xpath('//div[@id="commentlist"]')    
    
      
    xpath_reviewer_url= './/a[@class="avatar"]/@href' #passed
    reviewer_url=res.xpath(xpath_reviewer_url).getall()   #a list containing all the user_url from 1st page of review
        
    xpath_rating= '//li[@class="rev-item comment-item clearfix"]/span/@class'   #passed
    rating_pre=res.xpath(xpath_rating).getall()   #a list containing all the rating from 1st page of review
    rating =list(map(lambda x :str(x)[-1], rating_pre ))
    
    xpath_review_time ='//div[@class="info clearfix"]/span[@class="time"]/text()'     #passed
    review_time1 =res.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review
    
    xpath_review_title='//span[@class="from"]/a/@href'    #passed
    if res.xpath(xpath_review_title).getall() != []:
        review_title = res.xpath(xpath_review_title).getall()
    else:
        review_title='NA'    #a list containing where the review is from
        
    xpath_review='//li/p[@class="rev-txt"]/text()'   #passed
    review=res.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review
  
    next_page_button = driver.find_elements_by_xpath('//a[@title="后一页"]')
    if next_page_button :
        sleep(random()*2)
        next_page_button[0].click()  
        sel = Selector(text=driver.page_source)
    else:
        print("Can't click or last page")
        date_range= datetime.datetime.strptime(review_time1[-1],"%Y-%m-%d %H:%M:%S")
                   
        
sleep(random()) 
sel = Selector(text=driver.page_source)

#avg_reviews
avg_reviews= driver.find_elements_by_xpath('//li[@data-category="12"]/a')
driver.execute_script("arguments[0].click()",avg_reviews[0])
for i in range(1,6):
    
    print("page" + str(i)) #counter to keep track at which page    
  
    driver.execute_script('window.scrollTo(0,4500)')  #To scroll down
    #Forming selector path
    sleep(1+random()*2)
    sel = Selector(text=driver.page_source)
    sleep(1+random()*2)
    
    #selecting review list
    res = sel.xpath('//div[@id="commentlist"]')    
    
      
    xpath_reviewer_url= './/a[@class="avatar"]/@href' #passed
    reviewer_url=res.xpath(xpath_reviewer_url).getall()   #a list containing all the user_url from 1st page of review
        
    xpath_rating= '//li[@class="rev-item comment-item clearfix"]/span/@class'   #passed
    rating_pre=res.xpath(xpath_rating).getall()   #a list containing all the rating from 1st page of review
    rating =list(map(lambda x :str(x)[-1], rating_pre ))
    
    
    xpath_review_title='//span[@class="from"]/a/@href'    #passed
    if res.xpath(xpath_review_title).getall() != []:
        review_title = res.xpath(xpath_review_title).getall()
    else:
        review_title='NA'    #a list containing where the review is from
        
    xpath_review='//li/p[@class="rev-txt"]/text()'   #passed
    review=res.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review

    xpath_review_time ='//div[@class="info clearfix"]/span[@class="time"]/text()'     #passed
    review_time2 =res.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review
    for i in range(len(review_time2)):
        test_date=datetime.datetime.strptime(review_time2[i],"%Y-%m-%d %H:%M:%S")
        if test_date<date_range:
            flag=1
        else:
            flag=0
            
    if flag==1:
        continue

  
    next_page_button = driver.find_elements_by_xpath('//a[@title="后一页"]')
    if next_page_button :
        sleep(random()*2)
        next_page_button[0].click()  
        sel = Selector(text=driver.page_source)
    else:
        print("Can't click or last page")
        


#bad_reviews
bad_reviews= driver.find_elements_by_xpath('//li[@data-category="11"]/a')
driver.execute_script("arguments[0].click()",avg_reviews[0])
for i in range(1,6):
    
    print("page" + str(i)) #counter to keep track at which page    
  
    driver.execute_script('window.scrollTo(0,4500)')  #To scroll down
    #Forming selector path
    sleep(1+random()*2)
    sel = Selector(text=driver.page_source)
    sleep(1+random()*2)
    
    #selecting review list
    res = sel.xpath('//div[@id="commentlist"]')    
    
      
    xpath_reviewer_url= './/a[@class="avatar"]/@href' #passed
    reviewer_url=res.xpath(xpath_reviewer_url).getall()   #a list containing all the user_url from 1st page of review
        
    xpath_rating= '//li[@class="rev-item comment-item clearfix"]/span/@class'   #passed
    rating_pre=res.xpath(xpath_rating).getall()   #a list containing all the rating from 1st page of review
    rating =list(map(lambda x :str(x)[-1], rating_pre ))
    
    
    xpath_review_title='//span[@class="from"]/a/@href'    #passed
    if res.xpath(xpath_review_title).getall() != []:
        review_title = res.xpath(xpath_review_title).getall()
    else:
        review_title='NA'    #a list containing where the review is from
        
    xpath_review='//li/p[@class="rev-txt"]/text()'   #passed
    review=res.xpath(xpath_review).getall() #a list containing all the reviews from 1st page of review

    xpath_review_time ='//div[@class="info clearfix"]/span[@class="time"]/text()'     #passed
    review_time3 =res.xpath(xpath_review_time).getall()   #a list containing all the times from 1st page of review
    for i in range(len(review_time3)):
        test_date=datetime.datetime.strptime(review_time3[i],"%Y-%m-%d %H:%M:%S")
        if test_date<date_range:
            flag=1
        else:
            flag=0
            
    if flag==1:
        continue

  
    next_page_button = driver.find_elements_by_xpath('//a[@title="后一页"]')
    if next_page_button :
        sleep(random()*2)
        next_page_button[0].click()  
        sel = Selector(text=driver.page_source)
    else:
        print("Can't click or last page")




        
driver.quit()

#Write out as data-frame with date

poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/good.csv")