#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 10:17:31 2020

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
import itertools as it
from random import randint

driver = webdriver.Chrome('./chromedriver')


url = "https://place.qyer.com/poi/V2MJYFFvBzZTZQ/"

driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['reviews'])

for i in range(1,5):
    print("page" + str(i)) #counter to keep track at which page   
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down


    #Forming selector path
    sleep(randint(1,3))
    sel = Selector(text=driver.page_source)
    sleep(randint(1,3))
    res = sel.xpath('//div[@class="compo-main compo-feed"]') 


    xpath_url = './/a[@class="largeavatar"]/@href'  #passed
    reviewer_urls = res.xpath(xpath_url).getall()   #a list containing all the user urls from 1st page of review




    xpath_rates = '//ul[@class="comment-list"]//li//span[@class="poi-stars"]'
    star = res.xpath(xpath_rates).getall()

    def regex_cnt(string,pattern):
        return len(re.findall(pattern,string))

    rates=list(map(lambda x:regex_cnt(x,"singlestar full"),star))     #return a list of ratings from 1st page of review
    #print(rates)




    #print(driver.find_elements_by_xpath('/li[1]//span[@class="poi-stars"]'))

    xpath_date = '//a[@class="date"]/text()'  #passed
    date = res.xpath(xpath_date).getall()   #a list containing all the dates from 1st page of review
    
    review_body_list=[]
    for i in range(1,11):
        xpath_body='//li[{}]//p[@class="content"]/text()'.format(i)
        reviews=res.xpath(xpath_body).getall()
        review_body_list.append(reviews)
        print(review_body_list)
    
    #xpath_body= '//p[@class="content"]/text()'  #passed
    #reviews = res.xpath(xpath_body).getall()   #a list containing all the reviews from 1st page of review

    for j in range(len(reviewer_urls)):
            reviewer_url = reviewer_urls[j]
            review_date =  date[j]
            review_rating = rates[j]
            review_body = review_body_list[j]


            poi_df.loc[poi_df.shape[0]] = [review_body]#for illustration only, changes the variables accordingly


    next_page_button = driver.find_elements_by_xpath('//a[@title="下一页"]')
    if next_page_button:
        sleep(randint(1,3))
        next_page_button[0].click()  
    else :
        print("Can't click or last page")
            
    sleep(randint(1,3))  
    sel = Selector(text=driver.page_source)
    
driver.quit()
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/QY4_2trial.csv")
