# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

#url = "https://www.mafengwo.cn/poi/5422487.html"
#url = "https://www.mafengwo.cn/poi/11057.html"
url = "https://www.mafengwo.cn/poi/10962.html"
driver.get(url)


poi_df = pd.DataFrame(columns=['POI','eng', 'total_reviews','good_reviews',\
                               'avg_reviews','bad_reviews','special_reviews',\
                               'about', 'address','phone','website',\
                               'time recommended','opening hours',\
                               'transportation _mode','attributes_crawled time'])
    
    
    
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down

#Forming selector path
sleep(randint(1,5)) 
sel = Selector(text=driver.page_source)
sleep(randint(1,5)) 

#select areas where we going to extract info
res = sel.xpath('.//div[@class="container"]')   

xpath_name='//div[@class="row row-top"]//div[@class="title"]/h1/text()'   #passed
name = res.xpath(xpath_name).extract_first() 

xpath_eng='//div[@class="row row-top"]//div[@class="en"]/text()'    #passed
eng = res.xpath(xpath_eng).extract_first() 

xpath_total_reviews = '//div[@class="mhd mhd-large"]/span/em/text()'    #passed
total_reviews = res.xpath(xpath_total_reviews).extract_first() 

xpath_good_reviews = '//li[@data-category="13"]/a/span[@class="num"]/text()'   #passed
good_reviews = res.xpath(xpath_good_reviews).extract_first()

xpath_avg_reviews = '//li[@data-category="12"]/a/span[@class="num"]/text()'   #passed
avg_reviews = res.xpath(xpath_avg_reviews).extract_first()

xpath_bad_reviews = '//li[@data-category="11"]/a/span[@class="num"]/text()'  
bad_reviews = res.xpath(xpath_bad_reviews).extract_first()

xpath_special_reviews = '//li[@data-category="1"]/a/span[@class="num"]/text()'    #special case, there are many different special tags
special_reviews = res.xpath(xpath_special_reviews).extract_first()

xpath_about1='//div[@data-cs-p="概况"]/div/text()'  #specific location    #passed
xpath_about2='//div[@class="main-detail"]/dl[1]/dd/text()'   #general location
if res.xpath(xpath_about2).extract_first() != None:
    about = (driver.find_element_by_xpath('//div[@class="main-detail"]/dl[1]/dd')).text
else:
    about = (driver.find_element_by_xpath('//div[@data-cs-p="概况"]/div')).text

#xpath_price =    the price shown here is a list and may not directly related to the POI(may be a travel package)
#price = 

xpath_address1 ='//div[@class="mhd"]/p/text()'   #景点位置   #passed
xpath_address2 ='//div[@class="address"]/text()'   #地址     #passed
if res.xpath(xpath_address1).extract_first() != None:
    address = res.xpath(xpath_address1).extract_first()
else:
    address = res.xpath(xpath_address2).extract_first()


xpath_phone1 ='//li[@class="tel"]/div[@class="content"]/text()'   #specific location   #passed
xpath_phone2 ='//li[@class="item-tel"]/div[@class="content"]/text()'   #general        #passed
if res.xpath(xpath_phone1).extract_first() != None:   
    phone = res.xpath(xpath_phone1).extract_first()
else:
    phone = res.xpath(xpath_phone2).extract_first()                        


xpath_website = '//li[@class="item-site"]/div[@class="content"]/a/@href'  #passed
website = res.xpath(xpath_website).extract_first()     


xpath_rec_time ='//li[@class="item-time"]/div[@class="content"]/text()'   #only appeared for specific location, but share sme xpath
if res.xpath(xpath_address1).extract_first() != None:    #confirm its a specific location
    rec_time = res.xpath(xpath_rec_time).extract_first()
else:
    rec_time = 'NA'
    
xpath_op_hr1 = '//div[@class="mod mod-detail"]/dl[3]/dd/text()'     #specific location case 1
xpath_op_hr1_1 = '//div[@class="mod mod-detail"]/dl[3]/dd//div/text()'   #specific location case 2
xpath_op_hr2 ='//li[@class="item-time"]/div[@class="content"]/text()'
if res.xpath(xpath_address1).extract_first() != None:   #confirm it is a specific location
    if res.xpath(xpath_op_hr1).extract_first() != None:
        op_hr=res.xpath(xpath_op_hr1).extract_first()
    else:
        op_hr=res.xpath(xpath_op_hr1_1).extract_first()
else:
    op_hr=res.xpath(xpath_op_hr2).extract_first()  #general
    
    
xpath_trans1 = '//div[@class="mod mod-detail"]/dl[1]/dd/text()'    #specific location   #passed
xpath_trans2 = '//div[@class="main-detail"]/dl[3]/dd/text()'    #general   #passed
if res.xpath(xpath_trans1).extract_first() != None:
    transportation = res.xpath(xpath_trans1).extract_first()
else:
    transportation = res.xpath(xpath_trans2).extract_first()


today = date.today()
today_date = today.strftime("%Y%m%d")

poi_df.loc[poi_df.shape[0]] = [name]+[eng]+[total_reviews]+[good_reviews]+\
                              [avg_reviews]+[bad_reviews]+[special_reviews]+\
                              [about]+[address]+[phone]+[website]+\
                              [rec_time]+[op_hr]+\
                              [transportation] + [today_date]  

driver.quit()


poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/MFW4_1.csv")