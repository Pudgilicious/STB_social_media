#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:12:27 2020

@author: jia
"""

import pandas as pd
import mysql.connector
from scrapy import Selector
import os
import re
import yaml
import utils
from time import sleep
import traceback
from random import random
from selenium import webdriver
from datetime import datetime, date, timedelta
from random import random

class CtripCrawler:
    attributes_col_names = ['POI_INDEX',
                            'TOTAL_REVIEWS',
                            'RANKING',
                            'RATINGS',
                            'ADDRESS',
                            'OPENING_HOURS',
                            'ATTRIBUTES_CRAWLED_TIME'
                           ]

    reviews_col_names = ['REVIEW_INDEX',
                         'WEBSITE_INDEX',
                         'POI_INDEX',
                         'REVIEWER_NAME',
                         'REVIEW_RATING',
                         'REVIEW_DATE',
                         'REVIEW_TIME',
                         'REVIEW_BODY',
                         'ATTRIBUTES_CRAWLED_TIME'
                         #'TRANSLATED_REVIEW_BODY_GOOGLE',
                         #'TRANSLATED_REVIEW_BODY_WATSON'
                        ]
    
    
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.chromedriver_path = chromedriver_path
        self.driver = None
        self.poi_df = poi_df
        if cnx:
            self.cursor = cnx.cursor()
            
        #for FMS
        self.fsm_state=0
        
        # User input parameters into crawl_pois method, from config_file_QY.yml
        self.number_of_pages = None

        #update after each POI is crawled
        self.current_page = None
        self.current_poi_index = None
        self.current_poi_name = None
        self.current_poi_url = None
        self.review_final_page = False
        self.attributes_crawled=False
        self.reviews_crawled=False
        self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
        self.sel = None                                
        self.current_url=None
        
       
        
        # Create unique CSVs.
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        os.makedirs('./output/{}/'.format(self.datetime_string))
        os.makedirs('./output/{}/reviews'.format(self.datetime_string))
        self.attributes_df.to_csv('./output/{}/attributes.csv'.format(self.datetime_string),mode='a', index=False)

                
    
    def add_to_database(self):
        # Read csv, add to database, then cnx.commit().
        return
    
    
    def crawl_pois(self, number_of_pages=None):
        if self.fsm_state == 0:
            if number_of_pages is not None:
                self.number_of_pages = number_of_pages
            #initialization finish, change state
            self.fsm_state = 1
            
        self.driver = webdriver.Chrome(self.chromedriver_path)  

        while len(self.poi_df.index) > 0:
    
            # Create <POI_INDEX>.csv in reviews and reviewers folders.
            if self.fsm_state == 1:
                self.current_poi_index = self.poi_df.iloc[0][0]
                self.current_poi_name = self.poi_df.iloc[0][1]
                self.current_poi_url = self.poi_df.iloc[0][2]
                self.reviews_df.to_csv('./output/{}/reviews/{}.csv'
                                       .format(self.datetime_string,
                                               self.current_poi_index),
                                       mode='a',
                                       index=False
                                       )
                     
            self.driver.get(self.current_poi_url)
            if self.fsm_state == 3: 
                self.fsm_state=2
            sleep(1+random()*2)
            self.sel = Selector(text=self.driver.page_source)
                
    #################handle error of redirecting########################################
            self. current_url= self.driver.current_url
            if self.current_url == 'https://you.ctrip.com/':
                log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                log_file.write('{}, {}, {}, {}'.format(self.current_poi_index,
                                                       self.current_poi_name,
                                                       datetime.now(),
                                                       'current POI does not exist'))
                log_file.close()
                self.poi_df = self.poi_df.iloc[1:]
                continue
    ####################################################################################################
    
            if self.fsm_state != 3:
                if self.fsm_state == 2:
                    # Note change in FSM state
                    self.fsm_state = 1   
                    
                try:
                    if not self.attributes_crawled:    
                            print('########## {}##########'.format(self.current_poi_name))
                            self.crawl_attributes()
                            self.attributes_df.to_csv('./output/{}/attributes.csv'.format(self.datetime_string),
                                                      mode='a', 
                                                      header=False,
                                                      index=False)
                            self.attributes_df = pd.DataFrame(
                                columns=self.attributes_col_names)
                            self.attributes_crawled = True  
                   
                    # Crawl reviews
                    if not self.reviews_crawled:
                        self.crawl_reviews()
            
                        if self.db_out_flag != 'csv':
                            self.add_to_database()
                            
                    
                    self.current_page = None
                    self.attributes_crawled = False
                    self.reviews_crawled = False
                    
                    self.poi_df = self.poi_df.iloc[1:]
        
                        
                   
                except:
                    self.fsm_state=3
                    self.driver.quit()
                    self.current_page = None
                    log_file = open('./output/{}/log.txt'
                                    .format(self.datetime_string), 'a+')
                    log_file.write('{}, {}, page: {}, {}\n'\
                               .format(self.current_poi_index,
                                       self.current_poi_name,
                                       self.current_page,
                                       datetime.now()))
                    log_file.write(traceback.format_exc() + '\n')
                    log_file.close()
                    #erase every thing from the POI review csv, rewrite in next loop
                    f = open("./output/{}/reviews/{}.csv".format(self.datetime_string,
                                                                 self.current_poi_index), "w")
                    f.truncate()
                    f.close()
                    print("Exception has occurred. Please check log file.")
                    sleep(1)
                    return
            
                
                
            
        self.driver.quit()
        self.fsm_state = 4
 
                
    def crawl_reviews(self):
        if self.current_page==None:
            self.current_page=1
        if self.number_of_pages is not None:
            for i in range(self.number_of_pages):
                self.crawl_reviews_1_page(self.current_poi_index)
                print('Page {} done.'.format(self.current_page))
                self.current_page += 1
                self.reviews_to_csv()
                if self.review_final_page:
                    self.review_final_page = False
                    break
        else:
            while not self.review_final_page:
                self.crawl_reviews_1_page(self.current_poi_index)
                self.reviews_to_csv()
                print('Page {} done.'.format(self.current_page))
                self.current_page += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break
                    
                    
    def reviews_to_csv(self):
        self.reviews_df.to_csv('./output/{}/reviews/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', header=False, index=False)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
        
    
    def crawl_attributes(self):
        poi_index=self.current_poi_index
      
        #select areas where we going to extract info
        res = self.sel.xpath('.//div[@class="brief-box clearfix"]')
        res1= self.sel.xpath('.//body') 

        
        if res:
            xpath_total_reviews = '//a[@data-reactid="58"]/text()'    
            total_review =res.xpath(xpath_total_reviews).extract_first() 

            #xpath_name = '//h2[@data-reactid="38"]/text()'    
            #name=res.xpath(xpath_name).extract_first()   

            xpath_rate = '//i[@class="num"]/text()'    
            rating=res.xpath(xpath_rate).extract_first()  

            xpath_add = '//span[@data-reactid="45"]/text()'    
            address=res.xpath(xpath_add).extract_first()  

            xpath_openhr = '//span[@data-reactid="51"]/text()'   
            opening_hours=res.xpath(xpath_openhr).extract_first()  
            
            # Parsing attributes.
            total_reviews = self.parse_total_reviews1(total_review)
 
        else:
            xpath_total_reviews = '//span[@class="f_orange"]/text()'  
            total_reviews =res1.xpath(xpath_total_reviews).extract_first() 

            #xpath_name = '//div[@class="f_left"]/h1/a/text()'    
            #name=res1.xpath(xpath_name).extract_first()   

            xpath_rate = '//span[@class="score"]/b/text()'    
            rating=res1.xpath(xpath_rate).extract_first()  

            xpath_add = '//p[@class="s_sight_addr"]/text()' 
            add=res1.xpath(xpath_add).extract_first()  

            xpath_openhr = '//dl[@class="s_sight_in_list"]/dd/text()'    
            opening_hours=res1.xpath(xpath_openhr).extract_first()  
            
            # Parsing attributes
            address=self.parse_attribute_address(add)
            
     
        ranking=poi_index
        #crawltime=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                                    
        poi_attributes = [poi_index,
                          total_reviews, 
                          ranking, 
                          rating,  
                          address, 
                          opening_hours,
                          datetime.now()
                         ]
                                    
        #print(poi_attributes)
        
        # Inserting attributes into dataframe
        poi_attributes_dict = dict(zip(self.attributes_col_names, poi_attributes))
        self.attributes_df = self.attributes_df.append(poi_attributes_dict, ignore_index=True)
        sleep(2+random()*2)

    def crawl_reviews_1_page(self,poi_index):   
        #driver = self.driver
        #sel = Selector(text=driver.page_source)
        sleep(random()*2)
        res = self.sel.xpath('//div[@class="clearfix"]')    
        res1= self.sel.xpath('//div[@class="weibocombox"]')
    
        if res:
            xpath_user_name = './/li/div[@class="user-date"]/span/text()[1]'  
            reviewer_name1 = res.xpath(xpath_user_name).getall()   

            xpath_review_time ='.//li/div[@class="user-date"]/span/text()[3]'  
            review_time_tgt =res.xpath(xpath_review_time).getall() 
            
            xpath_review='.//li/p/text()'
            review=res.xpath(xpath_review).getall() 
    
            xpath_rates='.//li/h4/span/text()[2]'
            review_ratings=res.xpath(xpath_rates).getall()
            
            #parsing elements
            review_date1= list(map(self.parse_review_date1,review_time_tgt))
            review_time1= list(map(self.parse_review_time1,review_time_tgt))
            review_ratings1= list(map(self.parse_review_rating1,review_ratings))
            review_body1=list(map(self.parse_review_body1,review))
        
        else:
            xpath_user_name = './/a[@itemprop="author"]/text()'  
            reviewer_name1 = res1.xpath(xpath_user_name).getall()   

            xpath_review_time ='.//em[@itemprop="datePublished"]/text()'  
            review_date1 =res1.xpath(xpath_review_time).getall()   

            xpath_review='.//span[@class="heightbox"]/text()'
            review_body=res1.xpath(xpath_review).getall() 
    
            xpath_rates='.//ul//span/@style'
            rates=res1.xpath(xpath_rates).getall()
            
            review_time1 = 'Not Available'
            
            # Parsing attributes.
            review_ratings1= list(map(self.parse_review_rating2,rates))
            review_body1=list(map(self.parse_review_body1,review_body1))
        
        for i in range(len(reviewer_name1)):
            reviewer_name=reviewer_name1[i]
            review_date=review_date1[i]
            review_time=review_time1[i]
            review_ratings=review_ratings1[i]
            review_body=review_body1[i]
            
        
        review_details = [None, # REVIEW_INDEX
                          2, # WEBSITE_INDEX (Ctrip is '2')
                          poi_index,
                          reviewer_name,
                          review_ratings,
                          review_date,
                          review_time,
                          review_body,
                          datetime.now()
                          ]
            
            
            
        # Inserting reviews into dataframe.
        review_details_dict = dict(zip(self.reviews_col_names, review_details))
        self.reviews_df = self.reviews_df.append(review_details_dict, ignore_index=True)
        
        if res:
            next_page_button = self.driver.find_elements_by_xpath('//a[@class="down  "]')
            if next_page_button:
                if self.driver.current_url!= self.current_poi_url:
                    raise Exception("wrong_page")
                else:
                    self.driver.execute_script("arguments[0].click()",next_page_button[0])
                    sleep(1+random()*2)
                    self.sel = Selector(text=self.driver.page_source)
            else :
                sleep(1+random())
                if self.current_page <= self.number_of_pages:
                    raise Exception("random clicking happened")
                else:
                    print("Can't click or last page")
                    self.reviews_crawled=True
                    self.review_final_page= True
                    
        else:
            next_page_button = self.driver.find_elements_by_xpath('//a[@class="nextpage"]')
            if next_page_button:
                if self.driver.current_url!= self.current_poi_url:
                    raise Exception("wrong_page")
                else:
                    self.driver.execute_script("arguments[0].click()",next_page_button[0])
                    sleep(1+random()*2)
                    self.sel = Selector(text=self.driver.page_source)
            else :
                sleep(1+random())
                if self.current_page <= self.number_of_pages:
                    raise Exception("random clicking happened")
                else:
                    print("Can't click or last page")
                    self.reviews_crawled=True
                    self.review_final_page= True
            
        
            
        

    
    # Methods below are all utility functions.
    def parse_total_reviews1(self, text):
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0
    
    def parse_attribute_address(self, text):
        return (text[3:]).replace(' ','')
    
    def parse_review_date1(self, text):
        return datetime.strptime(text[0:10],"%Y-%m-%d")
        
    def parse_review_time1(self, text):
        return datetime.strptime(text[11:16],"%H:%M")

    
    def parse_review_rating1(self, text):
        return int(text)
    
    def parse_review_rating2 (self, text):
        return int(text[6:text.find('%')])/20
    
    def parse_review_body1(self, text):
        return text.replace('\n','')
