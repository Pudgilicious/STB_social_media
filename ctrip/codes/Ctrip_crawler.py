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
                            'ENG_NAME',
                            'TOTAL_REVIEWS',
                            'RANKING',
                            'RATINGS',
                            'ADDRESS',
                            'OPENING_HOURS',
                            'ATTRIBUTES_CRAWLED_TIME'
                            ]

    reviews_col_names = ['REVIEW_ID',
                         'WEBSITE_INDEX',
                         'POI_INDEX',
                         'REVIEWER_NAME',
                         'REVIEW_RATING',
                         'REVIEW_DATE',
                         'REVIEW_TIME',
                         'REVIEW_BODY',
                         'ATTRIBUTES_CRAWLED_TIME'
                         # 'TRANSLATED_REVIEW_BODY_GOOGLE',
                         # 'TRANSLATED_REVIEW_BODY_WATSON'
                         ]

    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        """

        @param chromedriver_path: the path of the chromedriver file
        @param poi_df: the dataframe contains all POIs and their respective URLs
        @param cnx: connection to mySQL
        @param db_out_flag: output format, usually csv
        """
        self.chromedriver_path = chromedriver_path
        self.driver = None
        self.poi_df = poi_df
        if cnx:
            self.cursor = cnx.cursor()
        self.db_out_flag = db_out_flag
        # for FMS
        self.fsm_state = "0_init"

        # User input parameters into crawl_pois method, from config_file_Ctrip.yml
        self.number_of_pages = None
        self.timeout = None
        self.proxy_mode = None
        self.authen_count = None

        # update after each POI is crawled
        self.current_page = 1  # current crawling review page
        self.current_poi_index = None
        self.current_poi_name = None
        self.current_poi_url = None
        self.review_final_page = False
        self.attributes_crawled = False
        self.reviews_crawled = False
        self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
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
        self.attributes_df.to_csv('./output/{}/attributes.csv'.format(self.datetime_string), mode='a', index=False)

    def add_to_database(self):
        # Read csv, add to database, then cnx.commit().
        return

    def crawl_pois(self, number_of_pages=None, proxy_mode=None, timeout=None, authen_count=None):
        """

        @param number_of_pages: the nuber of pages going to be crawled for each POI, if None, crawl all pages, if 0, only attributes will be crawled
        @param proxy_mode: choose between 1,2,3. 1 for local IP address, 2 for switching to proxy if caught by authentication, 3 ofr proxy addresses
        @param timeout: the time allow for a page to complete the load
        @param authen_count: the times allowed to reload a failed page, use to confirm an authentification test is met, not lag happened
        @return: a series of csv files, 'attribute': 1 list of attribtues of all POIs, review folder: each POI has a csv file for its reviews, named according to their respective POI index
        """
        if self.fsm_state == "0_init":

            # number of pages to crawl
            if number_of_pages is not None:
                self.number_of_pages = number_of_pages
            if proxy_mode is not None:
                self.initial_proxy_mode = proxy_mode
                self.proxy_mode = proxy_mode
            if authen_count is not None:
                self.authen_count = authen_count

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
                self.current_poi_name = self.poi_df.iloc[0][1]
                self.current_poi_url = self.poi_df.iloc[0][2]

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
                    if not self.reviews_crawled and self.number_of_pages != 0:
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
                        self.attributes_crawled = False
                        self.reviews_crawled = False
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

    def crawl_attributes(self):
        """
        crawl attributes of a POI
        """
        poi_index = self.current_poi_index
        # select areas where we going to extract info
        res = self.sel.xpath('.//div[@class="brief-box clearfix"]')
        res1 = self.sel.xpath('.//div[@class="content cf dest_details"]')

        if res:
            eng_name = "not available"

            xpath_total_reviews = '//a[@data-reactid="58"]/text()'
            total_review = res.xpath(xpath_total_reviews).extract_first()

            # xpath_name = '//h2[@data-reactid="38"]/text()'
            # name=res.xpath(xpath_name).extract_first()

            xpath_rate = '//i[@class="num"]/text()'
            rating = res.xpath(xpath_rate).extract_first()

            xpath_add = '//span[@data-reactid="45"]/text()'
            address = res.xpath(xpath_add).extract_first()

            xpath_openhr = '//span[@data-reactid="51"]/text()'
            opening_hours = res.xpath(xpath_openhr).extract_first()

            # Parsing attributes.
            total_reviews = self.parse_total_reviews1(total_review)

        else:
            xpath_eng = '//div[@class="f_left"]/p/text()'
            eng_name1 = res1.xpath(xpath_eng).extract_first()

            xpath_total_reviews = '//span[@class="f_orange"]/text()'
            total_reviews = res1.xpath(xpath_total_reviews).extract_first()

            # xpath_name = '//div[@class="f_left"]/h1/a/text()'
            # name=res1.xpath(xpath_name).extract_first()

            xpath_rate = '//span[@class="score"]/b/text()'
            rating = res1.xpath(xpath_rate).extract_first()

            xpath_add = '//p[@class="s_sight_addr"]/text()'
            add = res1.xpath(xpath_add).extract_first()

            xpath_openhr = '//dl[@class="s_sight_in_list"]/dd/text()'
            opening_hours = res1.xpath(xpath_openhr).extract_first()

            # Parsing attributes
            address = self.parse_attribute_address(add)
            eng_name = self.parse_eng_name(eng_name1)

        ranking = poi_index
        # crawltime=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        poi_attributes = [poi_index,
                          eng_name,
                          total_reviews,
                          ranking,
                          rating,
                          address,
                          opening_hours,
                          datetime.now()
                          ]

        # print(poi_attributes)

        # Inserting attributes into dataframe
        poi_attributes_dict = dict(zip(self.attributes_col_names, poi_attributes))
        self.attributes_df = self.attributes_df.append(poi_attributes_dict, ignore_index=True)
        sleep(2 + random() * 2)

    def crawl_reviews(self):
        """
        crawl reviews of a POI
        """
        self.reviews_crawled == True
        res = self.sel.xpath('//div[@class="clearfix"]')
        res1 = self.sel.xpath('//div[@class="weibocombox"]')
        if res:
            xpath_end = './/a[@class="btn-last-page  "]/text()'
            last = res.xpath(xpath_end).getall()
        else:
            xpath_end = '//b[@class="numpage"]/text()'
            last = res1.xpath(xpath_end).getall()
        if last == []:
            self.last_page_number == 1
        else:
            self.last_page_number = int(last[0])

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

    def crawl_reviews_1_page(self, poi_index):
        """
        crawl one page of reviews of a POI
        @param poi_index: the current crawling POI
        """
        # driver = self.driver
        # sel = Selector(text=driver.page_source)
        sleep(random() * 2)
        res = self.sel.xpath('//div[@class="clearfix"]')
        res1 = self.sel.xpath('//div[@class="weibocombox"]')

        if res:

            xpath_user_name = './/li/div[@class="user-date"]/span/text()[1]'
            reviewer_name1 = res.xpath(xpath_user_name).getall()

            xpath_review_time = './/li/div[@class="user-date"]/span/text()[3]'
            review_time_tgt = res.xpath(xpath_review_time).getall()

            xpath_review = './/li/p/text()'
            review = res.xpath(xpath_review).getall()

            # check rating exist or not
            xpath_existance = './/li/div[@style="margin-bottom: 0px;"]'
            if res.xpath(xpath_existance).getall() != []:
                review_ratings = []
                for i in range(len(reviewer_name1)):
                    xpath_rates = './/li[{}]/h4/span/text()[2]'.format(i)
                    individual_rate = res.xpath(xpath_rates).extract_first()
                    if individual_rate != None:
                        review_ratings += individual_rate
                    else:
                        review_ratings += "9"  # if rating does not exist, print 9

            else:
                xpath_rates = './/li/h4/span/text()[2]'
                review_ratings = res.xpath(xpath_rates).getall()

            # parsing elements
            review_date1 = list(map(self.parse_review_date1, review_time_tgt))
            review_time1 = list(map(self.parse_review_time1, review_time_tgt))
            review_ratings1 = list(map(self.parse_review_rating1, review_ratings))
            review_body1 = list(map(self.parse_review_body1, review))

        else:
            xpath_user_name = './/a[@itemprop="author"]/text()'
            reviewer_name1 = res1.xpath(xpath_user_name).getall()

            xpath_review_time = './/em[@itemprop="datePublished"]/text()'
            review_date1 = res1.xpath(xpath_review_time).getall()

            xpath_review = './/span[@class="heightbox"]/text()'
            review_body = res1.xpath(xpath_review).getall()

            xpath_rates = './/ul//span/@style'
            rates = res1.xpath(xpath_rates).getall()

            review_time1 = ['Not Available'] * len(reviewer_name1)

            # Parsing attributes.
            review_ratings1 = list(map(self.parse_review_rating2, rates))
            review_body1 = list(map(self.parse_review_body1, review_body))

        for i in range(len(reviewer_name1)):
            reviewer_name = reviewer_name1[i]
            review_date = review_date1[i]
            review_time = review_time1[i]
            review_ratings = review_ratings1[i]
            review_body = review_body1[i]

            review_details = [None,  # REVIEW_INDEX
                              2,  # WEBSITE_INDEX (Ctrip is '2')
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
                self.driver.execute_script("arguments[0].click()", next_page_button[0])
                sleep(1 + random() * 2)
                self.sel = Selector(text=self.driver.page_source)
            else:
                sleep(1 + random())
                if self.number_of_pages != None:
                    if self.last_page_number < self.number_of_pages and self.current_page < self.last_page_number:
                        raise Exception("lagged, need to recrawl")
                    else:
                        self.review_final_page = True
                else:
                    self.review_final_page = True



        else:
            next_page_button = self.driver.find_elements_by_xpath('//a[@class="nextpage"]')
            if next_page_button:
                if self.driver.current_url != self.current_poi_url:
                    raise Exception("wrong_page")
                else:
                    sleep(random())
                    self.driver.execute_script("arguments[0].click()", next_page_button[0])
                    sleep(1 + random() * 2)
                    self.sel = Selector(text=self.driver.page_source)
            else:
                sleep(1 + random())
                if self.number_of_pages != None:
                    if self.last_page_number < self.number_of_pages and self.current_page < self.last_page_number:
                        raise Exception("lagged, need to recrawl")
                    else:
                        self.current_page = 1
                        self.review_final_page = True
                else:
                    self.current_page = 1
                    self.review_final_page = True

    # Methods below are all utility functions.
    def parse_total_reviews1(self, text):
        """

        @param text: the web element contains the number of reviews, always in the form 'xx条点评‘
        @return: int form, number of reviews
        """
        if re.search(r'\d+', str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0

    def parse_eng_name(self, text):
        """

        @param text: a string containing english name of the POI, usually with blanks
        @return: a string, english name of the POI, without unnecessary blanks
        """
        return ''.join(filter(str.isalpha, text))

    def parse_attribute_address(self, text):
        """

        @param text: a string contain the address of the POI, usually with blanks
        @return: a string, address of the POI, without unecessary blanks
        """
        return (text[3:]).replace(' ', '')

    def parse_review_date1(self, text):
        """

        @param text: a string contains the post date of a review
        @return: a date object
        """
        return datetime.strptime(text[0:10], "%Y-%m-%d").date()

    def parse_review_time1(self, text):
        """

        @param text: a string contains the post time of a review
        @return: a time object
        """
        return format(datetime.strptime(text[11:16], "%H:%M"), "%H:%M")

    def parse_review_rating1(self, text):
        """

        @param text: a string contains the rating given by reviewer, usually in the form 'x分'
        @return: the rate given by the reviewerm, in the form of integer
        """
        return int(text)

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
