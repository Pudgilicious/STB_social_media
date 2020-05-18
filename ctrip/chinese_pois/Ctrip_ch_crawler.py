#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:12:27 2020

@author: jia
"""

import pandas as pd
from scrapy import Selector
import os
import re
from time import sleep
import traceback
from random import random, randint
from selenium import webdriver
from datetime import datetime
# for proxy account
import urllib.request
import socket
import urllib.error
from proxy import working_proxies


class CtripCrawler:
    attributes_col_names = ['POI_INDEX',
                            'ENG_NAME'
                            ]

    reviews_col_names = ['POI_INDEX',
                         'REVIEWER_NAME',
                         'REVIEW_RATING',
                         'REVIEW_DATE',
                         'REVIEW_BODY'
                         ]

    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):

        self.chromedriver_path = chromedriver_path
        self.driver = None
        self.poi_df = poi_df
        if cnx:
            self.cursor = cnx.cursor()
        self.db_out_flag = db_out_flag
        # for FMS
        self.fsm_state = "0_init"

        # User input parameters into crawl_pois method, from config_file_Ctrip.yml
        self.timeout = None
        self.proxy_mode = None
        self.authen_count = None
        self.earliest_date=None
        
        self.current_date=None
        
        # update after each POI is crawled
        self.current_page = 1  # current crawling review page
        self.current_poi_index = None
        self.current_poi_name = None
        self.current_poi_url = None
        self.review_final_page = False
        self.reviews_crawled = False
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
        self.current_url = None
        self.last_page_number = 0

        # for proxy and authentication
        self.initial_proxy_mode = None  # to know whether to switch back to local IP
        self.sel = None  # for authentication test
        self.count = 0  # double check authentication
        self.count_proxy = 1  # count number of proxies tested
        self.PROXY = None
        self.proxy_num = 0  # proxy position in working proxy list
        self.working_proxies = list((working_proxies())['IP'])

        # Create unique CSVs.
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        os.makedirs('./output/{}/'.format(self.datetime_string))
        os.makedirs('./output/{}/reviews'.format(self.datetime_string))


    def add_to_database(self):
        # Read csv, add to database, then cnx.commit().
        return

    def crawl_pois(self, proxy_mode=None, timeout=None, authen_count=None, earliest_date=None):
 
        if self.fsm_state == "0_init":

            
            if proxy_mode is not None:
                self.initial_proxy_mode = proxy_mode
                self.proxy_mode = proxy_mode
            if authen_count is not None:
                self.authen_count = authen_count
            if earliest_date is not None:
                self.earliest_date=earliest_date
            # initialization finish, change state
            self.fsm_state = "1_normal"

        # to disable images
        # chromeOptions = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chromeOptions.add_experimental_option("prefs", prefs)
        # self.driver = webdriver.Chrome(self.chromedriver_path)#chrome_options=chromeOptions)

        while len(self.poi_df.index) > 0:

            if self.fsm_state == "3_crash":
                self.fsm_state = "2_error_handling"
            sleep(random())

            if self.fsm_state != "3_crash":
                if self.fsm_state == "2_error_handling":
                    # Note change in FSM state
                    self.fsm_state = "1_normal"
                    # while fsm date == 1 (start crawling)

            # set proxy
            if self.proxy_mode == 3:
                print(str(len(self.working_proxies)) + ' proxies in list')
                self.count_proxy += 1
                self.proxy_num = randint(1, len(self.working_proxies) - 1)
                self.PROXY = self.working_proxies[self.proxy_num]
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy": self.PROXY,
                    "ftpProxy": self.PROXY,
                    "sslProxy": self.PROXY,
                    "proxyType": "MANUAL",
                }
                socket.setdefaulttimeout(self.timeout)

                # switch back to local IP address for faster crawling
                if self.initial_proxy_mode == 2:
                    if self.count_proxy == round(
                            3600 / int(self.timeout)):  # wait for hr to switch back to local ip
                        self.proxy_mode = 2

            self.driver = webdriver.Chrome(self.chromedriver_path)

            if self.fsm_state == "1_normal":
                self.current_poi_index = self.poi_df.iloc[0][0]
                self.current_poi_name = self.poi_df.iloc[0][2]
                self.current_poi_url = self.poi_df.iloc[0][3]

                try:
                    self.driver.get(self.current_poi_url)
                except:
                    print('timeout')
                    pass

                # handling time out error, (currently no need)
                # log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                # log_file.write('{}, {}, {}, \n{}, \n{}\n '.format(self.current_poi_index,
                # self.current_poi_name,
                # datetime.now(),
                # PROXY,
                # 'time out error'))
                # log_file.close()
                # self.driver.quit()
                # change to another proxy
                # self.working_proxies.remove(PROXY)
                # self.proxy_num=randint(1,len(self.working_proxies))
                # return

                sleep(1 + random())
                self.sel = Selector(text=self.driver.page_source)
                
                
                if self.proxy_mode == 3:
                    #################handle proxy failure, case 1 ########################################
                    # the proxy is able to access the page, but fail to load all information properly
                    res1 = self.sel.xpath('//*[@id="root"]//div[@class="full_failure"]')
                    if res1 != []:
                        sleep(randint(1, 3) + random())
                        log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                        log_file.write('{}, {}, {}, \n{}, \n{}\n '.format(self.current_poi_index,
                                                                          self.current_poi_name,
                                                                          datetime.now(),
                                                                          self.PROXY,
                                                                          'loading incomplete, proxy fails'))
                        log_file.close()
                        self.driver.quit()
                        # change to another proxy
                        # self.working_proxies.remove(PROXY)
                        self.proxy_num = randint(1, len(self.working_proxies) - 1)  # switch to another PROXY
                        self.PROXY = self.working_proxies[self.proxy_num]
                        continue

                #################handle proxy failure, case 2 ########################################
                # the page display error msg, nothing is displayed, res2,res3 are for 2 diff web structures
                # res2=self.sel.xpath('.//div[@class="brief-box clearfix"]')
                # res3=self.sel.xpath('.//div[@class="content cf dest_details"]')
                # if res2 == [] or res3 == []:
                #   sleep(randint(1,3)+random())
                #  log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                # log_file.write('{}, {}, {}, \n{}, \n{}\n '.format(self.current_poi_index,
                #                                           self.current_poi_name,
                #                                          datetime.now(),
                #                                         PROXY,
                #                                        'chrome loading error, proxy fails'))
                # log_file.close()
                # self.driver.quit()
                # change to another proxy
                # self.working_proxies.remove(PROXY)
                # self.proxy_num=randint(1,len(self.working_proxies))
                # continue

                #################handle error of authentication########################################
                # check whether the authentication img exist
                # reload 3 times to aviod error due to lagging
                res = self.sel.xpath('/html/body/div[3]/div[3]/img')  # path does not exist if no authentication
                if res != []:
                    self.count += 1
                    sleep(randint(1, 3) + random())
                    if self.count == self.authen_count:
                        log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                        log_file.write('{}, {}, {}, {}\n'.format(self.current_poi_index,
                                                                 self.current_poi_name,
                                                                 datetime.now(),
                                                                 'caught by Ctrip, authentication test'))
                        log_file.close()
                        self.driver.quit()
                        # self.working_proxies.remove(PROXY)
                        self.count = 0
                        self.timeout = timeout
                        self.proxy_mode = 3
                    continue

                ####################################################################################################
                # finally, start crawling

                try:
                    #################handle error of redirecting########################################
                    self.current_url = self.driver.current_url
                    if self.current_url == 'https://you.ctrip.com/':
                        log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                        log_file.write('{}, {}, {}, {}\n'.format(self.current_poi_index,
                                                                 self.current_poi_name,
                                                                 datetime.now(),
                                                                 'current POI does not exist'))
                        log_file.close()
                        self.poi_df = self.poi_df.iloc[1:]
                        raise Exception("current POI does not exist")
                        continue
                    ####################################################################################################


                        # Crawl reviews
                    #if not self.reviews_crawled and self.number_of_pages != 0:
                    
                    order_by_time=self.driver.find_elements_by_xpath('//ul[@class="selectlist undis"]/li[3]/a')
                    self.driver.execute_script("arguments[0].click()", order_by_time[0])
                    sleep(5+random())
                    
                    self.sel = Selector(text=self.driver.page_source)
                    self.reviews_df.to_csv('./output/{}/reviews/{}.csv'
                                           .format(self.datetime_string,
                                                   self.current_poi_index),
                                           mode='a',
                                           index=False
                                           )    
                    
                    
                    self.crawl_reviews()

                    if self.db_out_flag != 'csv':
                        self.add_to_database()

                    self.current_page = 1
                    self.reviews_crawled = False
                    self.current_date=None
                    self.earliest_date=earliest_date
                    self.driver.quit()
                    self.poi_df = self.poi_df.iloc[1:]
                    


                except:
                    self.fsm_state = "3_crash"
                    # self.driver.quit()
                    self.current_page = 1
                    log_file = open('./output/{}/log.txt'
                                    .format(self.datetime_string), 'a+')
                    log_file.write('{}, {}, page: {}, {}\n' \
                                   .format(self.current_poi_index,
                                           self.current_poi_name,
                                           self.current_page,
                                           datetime.now()))
                    log_file.write(traceback.format_exc() + '\n')
                    log_file.close()
                    # erase every thing from the POI review csv, rewrite in next loop

                    if self.reviews_crawled == True:
                        os.remove('./output/{}/reviews/{}.csv'
                                  .format(self.datetime_string,
                                          self.current_poi_index))
                    print("Exception has occurred. Please check log file.")
                    self.reviews_crawled = False
                    self.driver.quit()
                    # self.working_proxies.remove(PROXY)

                    sleep(1)
                    return

        self.driver.quit()
        self.fsm_state = "4_complete"

    def reviews_to_csv(self):
        """
        store reviews to csv files
        """
        self.reviews_df.to_csv('./output/{}/reviews/{}.csv'.format(self.datetime_string, self.current_poi_index),
                               mode='a', header=False, index=False)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)

   
    def crawl_reviews(self):
        """
        crawl reviews of a POI
        """
        self.reviews_crawled == True
        
        if self.current_page is None:
            self.current_page = 1
        if self.earliest_date is not None:
            self.current_date = datetime.now().date()
            while self.current_date >= self.earliest_date:
                sleep(random())
                self.crawl_reviews_1_page(self.current_poi_index)
                self.reviews_to_csv()
                print('Page {} done.'.format(self.current_page))
                self.current_page += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break


    def crawl_reviews_1_page(self, poi_index):
        """
        crawl one page of reviews of a POI
        @param poi_index: the current crawling POI
        """
        # driver = self.driver
        # sel = Selector(text=driver.page_source)

        res1 = self.sel.xpath('//div[@class="weibocombox"]')


        xpath_user_name = './/a[@itemprop="author"]/text()'
        reviewer_name1 = res1.xpath(xpath_user_name).getall()

        xpath_review_time = './/em[@itemprop="datePublished"]/text()'
        review_date1 = res1.xpath(xpath_review_time).getall()

        xpath_review = './/span[@class="heightbox"]/text()'
        review_body = res1.xpath(xpath_review).getall()

        xpath_rates = './/ul//span/@style'
        rates = res1.xpath(xpath_rates).getall()

        # Parsing attributes.
        review_ratings1 = list(map(self.parse_review_rating2, rates))
        review_body1 = list(map(self.parse_review_body1, review_body))

        for i in range(len(reviewer_name1)):
            reviewer_name = reviewer_name1[i]
            review_date = review_date1[i]
            self.current_date=datetime.strptime(review_date, '%Y-%m-%d').date()
            review_ratings = review_ratings1[i]
            review_body = review_body1[i]
            
            review_details = [poi_index,
                              reviewer_name,
                              review_ratings,
                              review_date,
                              review_body
                              ]
            #if self.earliest_date is not None and self.current_date < self.earliest_date:
             #  break
            # Inserting reviews into dataframe.
            review_details_dict = dict(zip(self.reviews_col_names, review_details))
            self.reviews_df = self.reviews_df.append(review_details_dict, ignore_index=True)
            
        
        next_page_button = self.driver.find_elements_by_xpath('//a[@class="nextpage"]')
        if next_page_button:
            if self.driver.current_url != self.current_poi_url:
                raise Exception("wrong_page")
            else:
                sleep(random())
                self.driver.execute_script("arguments[0].click()", next_page_button[0])
                sleep(5+random())
                self.sel = Selector(text=self.driver.page_source)
        else:
            sleep(1 + random())
            self.current_page = 1
            self.review_final_page = True

    # Methods below are all utility functions.

    def parse_review_rating2(self, text):
        """

        @param text: a string contains the rating given by reviewer, with each 20 corresponding to 1 star in rating
        @return: the rate given by the reviewer, in the form of integer
        """
        return int(text[6:text.find('%')]) / 20

    def parse_review_body1(self, text):
        """

        @param text: a string contains review body
        @return: string with unnecessary blanks removed
        """
        return " ".join(text.split())
