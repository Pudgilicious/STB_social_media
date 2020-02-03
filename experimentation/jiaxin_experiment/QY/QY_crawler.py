#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:19:35 2020

@author: jia
"""

import pandas as pd
from scrapy import Selector
import os
import re
import utils
from time import sleep
import traceback
from random import random
from selenium import webdriver
from datetime import datetime, date, timedelta
from random import randint

class QYCrawler:
    attributes_col_names = ['POI_INDEX',
                            'TOTAL_REVIEWS',
                            'ABOUT_SUMMARY',
                            #'ABOUT',
                            'RANKING',
                            'TICKET_INFO',
                            'RATES',
                            'ADDRESS',
                            'PHONE',
                            'WEBSITE',
                            'TRANSPORTATION_MODE',
                            'OPENING_HOURS',
                            'ATTRIBUTES_CRAWLED_TIME'
                           ]

    reviews_col_names = ['REVIEW_INDEX',
                         'WEBSITE_INDEX',
                         'POI_INDEX',
                         'REVIEWER_URL',
                         'REVIEW_RATING',
                         'REVIEW_DATE',
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
        self.db_out_flag = db_out_flag
        
        
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
        self.last_page_number=None                                                     
        
        # Create unique CSVs.
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        os.makedirs('./output/{}/'.format(self.datetime_string))
        os.makedirs('./output/{}/reviews'.format(self.datetime_string))
        self.attributes_df.to_csv('./output/{}/attributes.csv'.format(self.datetime_string),
                                  mode='a',
                                  index=False)
        
        
    
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
                     
            if self.fsm_state == 3: 
                self.fsm_state=2
            sleep(1+random()*2)
            
            
            if self.fsm_state != 3:
                if self.fsm_state == 2:
                    # Note change in FSM state
                    self.fsm_state = 1   
                    
                try:
                    self.driver.get(self.current_poi_url)
                    self.sel = Selector(text=self.driver.page_source)
                    res = self.sel.xpath('//div[@id="app"]')           
                    if  res == []:   
                        log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                        log_file.write('{}, {}, {}, {}'\
                                          .format(self.current_poi_index,
                                                self.current_poi_name,
                                                datetime.now(),
                                                'POI website not working'))
                        log_file.close()
                        self.poi_df = self.poi_df.iloc[1:]
                        continue
                    #crawl attributes
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
                    #if self.reviews_crawled==True:
                     #   os.remove('./output/{}/reviews/{}.csv'
                      #                     .format(self.datetime_string,
                       #                            self.current_poi_index)) 
                    print("Exception has occurred. Please check log file.")
                    self.reviews_crawled=False
                    sleep(1)
                    return
            
                
                
            
        self.driver.quit()
        self.fsm_state = 4
            

  
    def crawl_attributes(self):
        sleep(1+random())
        #select areas where we going to extract info
        res = self.sel.xpath('.//div[@class="poi-detail"]')    
        
        
        #need parse ,"xxx条点评"
        xpath_tot_reviews = '//a[@data-bn-ipg="place-poi-detail-viewAllReviews"]/text()'     
        total_review=res.xpath(xpath_tot_reviews).extract_first() 

        xpath_summary = '//div[@class="poi-detail"]/div/p/text()'
        if res.xpath(xpath_summary).extract_first() != None:
            about_summary=res.xpath(xpath_summary).extract_first() 
        else: 
            about_summary='Not Available'
        
        #about is missing here, need to clarify the difference between about and about_summary
        
        
        #need parse, "第x名",change to int
        xpath_ranking = '//li[@class="rank"]/span/text()'     
        ranking_bf=res.xpath(xpath_ranking).extract_first() 
        
        xpath_ticket = './/li[./span[contains(text(),"门票：")]]/div/p/text()'
        if res.xpath(xpath_ticket).extract_first() != None:
            ticket_info=res.xpath(xpath_ticket).extract_first()
        else:
            ticket_info = str(None)

        #parse, remove spaces, change to float
        xpath_rate = '//span[@class="number"]/text()'    
        rate=res.xpath(xpath_rate).extract_first()
        
        xpath_address='.//li[./span[contains(text(),"地址：")]]/div/p/text()'
        if res.xpath(xpath_address).extract_first() != None:
            address=res.xpath(xpath_address).extract_first() 
        else:
            address='Not Available'
            
        xpath_phone='.//li[./span[contains(text(),"电话：")]]/div/p/text()'
        if res.xpath(xpath_phone).extract_first() != None:
            phone=res.xpath(xpath_phone).extract_first() 
        else:
            phone='Not Available'


        xpath_web =  './/li[./span[contains(text(),"网址：")]]/div/a/@href'
        if res.xpath(xpath_web).extract_first()!=None:
            website=res.xpath(xpath_web).extract_first() 
        else:
            website='Not Available'

        #need edit, share same xpath with phone case 2
        xpath_trans = './/li[./span[contains(text(),"到达方式：")]]/div/p/text()'  
        if res.xpath(xpath_trans).extract_first() != None :
            transportation_mode=res.xpath(xpath_trans).extract_first() 
        else:
            transportation_mode='Not Available'
  

        xpath_openhr = './/li[./span[contains(text(),"开放时间：")]]/div/p/text()'
        if res.xpath(xpath_openhr).extract_first() != None:
            opening_hours=res.xpath(xpath_openhr).extract_first()  
        else:
            opening_hours='Not Available'
        
        # Parsing attributes.
        total_reviews=self.parse_total_reviews(total_review)
        ranking=self.parse_ranking(ranking_bf)
        rates=self.parse_rate(rate)
        
        poi_attributes = [self.current_poi_index,
                          total_reviews, 
                          about_summary, 
                          #about, 
                          ranking,
                          ticket_info,
                          rates,
                          address,
                          phone,
                          website,
                          transportation_mode,
                          opening_hours,
                          datetime.now()
                         ]
        
        # Inserting attributes into dataframe
        poi_attributes_dict = dict(zip(self.attributes_col_names, poi_attributes))
        self.attributes_df = self.attributes_df.append(poi_attributes_dict, ignore_index=True)
        
        
    def crawl_reviews(self):
        res1 = self.sel.xpath('.//div[@class="compo-main compo-feed"]') 
        xpath_last_page='.//div[@class="ui_page"]/a/@data-page'
        page_list=res1.xpath(xpath_last_page).getall()
        if len(page_list)>1:                                                   #get the last page_number
            self.last_page_number=int(page_list[-2])
        else:
            self.last_page_number=1
            
        if self.current_page==None:                                 
            self.current_page=0
            
        if self.number_of_pages is not None:
            for i in range(self.number_of_pages):
                self.crawl_reviews_1_page(self.current_poi_index)
                self.current_page += 1
                print('Page {} done.'.format(self.current_page))
                self.reviews_to_csv()
                if self.review_final_page:
                    self.review_final_page = False
                    break
        else:
            while not self.review_final_page:
                self.crawl_reviews_1_page(self.current_poi_index)
                self.current_page += 1
                print('Page {} done.'.format(self.current_page))
                self.reviews_to_csv()
                if self.review_final_page:
                    self.review_final_page = False
                    break
                    
                    
    def reviews_to_csv(self):
        self.reviews_df.to_csv('./output/{}/reviews/{}.csv'.\
                               format(self.datetime_string, 
                                      self.current_poi_index), 
                               mode='a', 
                               header=False,
                               index=False)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
    

    def crawl_reviews_1_page(self, poi_index): 
        self.reviews_crawled=True
        res1 = self.sel.xpath('.//div[@class="compo-main compo-feed"]') 
        sleep(random())
        
        xpath_url = './/a[@class="largeavatar"]/@href' 
        reviewer_url1 = res1.xpath(xpath_url).getall()

        xpath_rates = './/ul[@class="comment-list"]//li//span[@class="poi-stars"]'
        star = res1.xpath(xpath_rates).getall()
        def regex_cnt(string,pattern):
            return len(re.findall(pattern,string))
        review_rating1=list(map(lambda x:regex_cnt(x,"singlestar full"),star))
       
        
        xpath_date = './/a[@class="date"]/text()'  
        review_date1 = res1.xpath(xpath_date).getall()   

        
        review_body_list=[]
        for i in range(1,len(reviewer_url1)+1):
            xpath_body='//li[{}]//p[@class="content"]/text()'.format(i)
            reviews=res1.xpath(xpath_body).getall()
            review_body_list.append(reviews)
            
        
        # Parsing reviews
        review_date1=list(map(self.parse_review_date,review_date1))
        
        for i in range(len(reviewer_url1)):
            reviewer_url = reviewer_url1[i]
            review_date =  review_date1[i]
            review_rating = review_rating1[i]
            review_body = self.parse_review_body(review_body_list[i])
            
            
            review_details = [None, # REVIEW_INDEX
                              4, # WEBSITE_INDEX (QY is '4')
                              self.current_poi_index,
                              reviewer_url,
                              review_rating,
                              review_date,
                              review_body,
                              #translated_review_body_google,
                              #translated_review_body_watson,
                              datetime.now()
                              ]
            

        # Inserting reviews into dataframe.
            review_details_dict = dict(zip(self.reviews_col_names, review_details))
            self.reviews_df = self.reviews_df.append(review_details_dict, ignore_index=True)
            

        next_page_button = self.driver.find_elements_by_xpath('//a[@title="下一页"]')
        if next_page_button:
            if self.driver.current_url!= self.current_poi_url:
                raise Exception("wrong_page")
            else:
                self.driver.execute_script("arguments[0].click()",next_page_button[0])
                sleep(1+random()*2)
                self.sel = Selector(text=self.driver.page_source)
        else :
            sleep(1+random())
            if self.last_page_number== 1:
                print("can't click or last page")
                self.review_final_page= True
            elif self.number_of_pages!= None and self.current_page <= self.number_of_pages:
                raise Exception("random clicking happened")
            elif self.last_page_number >1 and self.current_page < self.last_page_number-1:
                raise Exception("lagged, need to recrawl")
            else:
                print("can't click or last page")
                self.review_final_page= True
            
    def crawl_aggretage_list(self):
        url= "https://place.qyer.com/singapore/sight/"
        self.driver.get(url)

        # Initialize pandas data-frame with name of place and link
        poi_df = pd.DataFrame(columns=['WEBSITE_INDEX','POI_NAME','ENGLISH_NAME', 'URL'])
        
        # There are 24 pages of attractions in QY.
        for i in range(1,25):
               
        
                print("page" + str(i)) #counter to keep track at which page    
                sleep(randint(1,3))
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
            
                 #Forming selector path
                sleep(1+random()*2)
                self.sel = Selector(text=self.driver.page_source)
                
                
                res = self.sel.xpath('//div[@class="qyMain fl"]')    
                end_link = '/div/h3/a/@href'     
                end_text = '/div/h3/a[@target="_blank"]/text()'
                end_eng='/div/h3/a[@target="_blank"]/span/text()'
                #end_reviews = '/div/div[1]/span[2]/a/text()'
            
                #For each page, there are 15 attractions listed
                for a in range (1,16):
                
                    #Forming a string
                    xpath_link = '//*[@id="poiLists"]/li[' + str(a) +']' + end_link   
                    xpath_text = '//*[@id="poiLists"]/li[' + str(a) +']' + end_text
                    xpath_eng = '//*[@id="poiLists"]/li[' + str(a) +']' + end_eng
                    #xpath_reviews = '//*[@id="poiLists"]/li[' + str(a) +']' + end_reviews
                    
                    website_index=4
                    link = res.xpath(xpath_link).extract_first()     #eg. link = res.xpath('div[1]/div/div/div/div[2]/a[@target="_blank"]/@href').extract_first()       
                    text = res.xpath(xpath_text).extract_first()  
                    eng = res.xpath(xpath_eng).extract_first()  
                    #reviews = res.xpath(xpath_reviews).extract_first() 
                
                
                    poi_df.loc[poi_df.shape[0]] = [website_index] + [text] + [eng] + [link] #+ [reviews]
                        
                        
                next_page_button = self.driver.find_elements_by_xpath('//a[@title="下一页"]')
                if next_page_button:
                    sleep(1+random())    
                    next_page_button[0].click()  
                else:
                    print("Can't click or last page")
                    
                sleep(randint(1,5))  
                self.sel = Selector(text=self.driver.page_source)
                
        self.driver.quit()
        
        #Write out as data-frame with date
        #today = date.today()
        #today_date = today.strftime("%Y%m%d")
         
    
    # Methods below are all utility functions.all are static method
    def parse_total_reviews(self, text):
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0
    
    def parse_ranking(self, text):
        return int(re.search(r'\d+', text).group())
    
    def parse_rate(self, text):
        if text:
            return float(text.replace(' ', ''))
        else:
            return 0
        
    def parse_review_date(self, text):
        text1=text.replace('\n                  ','')
        return datetime.strptime(text1[0:10],"%Y-%m-%d")
    
    def parse_review_body(self, list_item):
        text=' '.join(list_item)
        return text.replace('\n','')
    
    