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

driver = webdriver.Chrome('./chromedriver')

url= "https://you.ctrip.com/sight/Singapore53.html"
driver.get(url)


# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI', 'link', 'num_reviews'])

# There are 106 pages of attractions in Ctrip.
for i in range(1,107):
       

        print("page" + str(i)) #counter to keep track at which page    
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
         #Forming selector path
        sleep(1) 
        sel = Selector(text=driver.page_source)
        sleep(1)
        
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
        
            link = res.xpath(xpath_link).extract_first()     #eg. link = res.xpath('div[1]/div/div/div/div[2]/a[@target="_blank"]/@href').extract_first()       
            text = res.xpath(xpath_text).extract_first()  
            reviews = res.xpath(xpath_reviews).extract_first() 
        
        
        
            try:
                if link:     #If link exist   
                    poi_df.loc[poi_df.shape[0]] = [text] + [link] + [reviews]
                   
            except:
                print("can't write")
                
                
        url1= "https://you.ctrip.com/sight/singapore53/s0-p{}.html".format(i+1)   
        driver.get(url1) 
        
#try:
     #       next_page_button = driver.find_element_by_xpath('//a[@class="nextpage"]')
       
#except:
         #   sleep(1)
          #  next_page_button = driver.find_element_by_xpath('//a[@class="nextpage"]')
        
    
#try:
           # next_page_button.click()  
          #  sel = Selector(text=driver.page_source)
       
#except:
            #print("Can't click or last page")
        
driver.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/trialctriplist.csv")# changed storage position and name_jia