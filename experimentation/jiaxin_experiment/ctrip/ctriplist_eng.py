#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:06:39 2020

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


options = webdriver.ChromeOptions()
prefs = {
  "translate_whitelists": {"cn":"en"},
  "translate":{"enabled":"true"}
}
options.add_experimental_option("prefs", prefs)
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)



url= "https://you.ctrip.com/sight/Singapore53.html"
chrome.get(url)
sleep(5) #for a manual choose of "always translate pages"



# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI', 'link', 'num_reviews'])

# There are 106 pages of attractions in Ctrip.
for i in range(1,113):
       

        print("page" + str(i)) #counter to keep track at which page   
        sleep(3)#to translate the page
        chrome.execute_script('window.scrollTo(0, 1080)')  #To scroll down
        sleep(2)
        chrome.execute_script('window.scrollTo(0, 2160)')  #To scroll down
        sleep(2)
        chrome.execute_script('window.scrollTo(0, 3000)')  #To scroll down
        sleep(2)

         #Forming selector path
         
        sel = Selector(text=chrome.page_source)
        sleep(1)
        
        res = sel.xpath('//div[/html/body/div[4]/div/div[2]/div/div[3]]')    
        end_link = '/div[2]/dl/dt/a/@href'     
        end_text1 = '/div[2]/dl/dt/a/font/font/text()'
        end_text2 = '/div[2]/dl/dt/font/a/font/text()'
        end_reviews = '/div[2]/ul/li[3]/a[@target="_blank"]/text()'
    
    
        
        #For each page, there are 15 attractions listed
        for a in range (1,20):
            
            #Forming a string
            xpath_link = 'div[' + str(a) +']' + end_link   
            xpath_text1 = 'div[' + str(a) +']' + end_text1
            xpath_text2 = 'div[' + str(a) +']' + end_text2
            xpath_reviews = 'div[' + str(a) +']' + end_reviews
        
            if res.xpath(xpath_text1).extract_first() != None:
                text = res.xpath(xpath_text1).extract_first()
            else:
                text = res.xpath(xpath_text2).extract_first()
                
            reviews = res.xpath(xpath_reviews).extract_first() 
            link = res.xpath(xpath_link).extract_first() 
          
        
            try:
                if link:     #If link exist   
                    poi_df.loc[poi_df.shape[0]] = [text] + [link] + [reviews]
                   
            except:
                print("can't write")
        

        
        sleep(1)        
        url1= "https://you.ctrip.com/sight/singapore53/s0-p{}.html".format(i+1)   
        chrome.get(url1) 
        
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
        
chrome.quit()

#Write out as data-frame with date
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/eng2.csv")