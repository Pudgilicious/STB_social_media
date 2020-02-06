#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:41:52 2020

@author: jia
"""


from time import sleep
from shop_crawler import ShoppingCrawler

class Shop_FSM:
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.crawler = ShoppingCrawler(chromedriver_path, poi_df, cnx, db_out_flag)


    def start(self,number_of_pages=None):
        crawler = self.crawler
        while crawler.fsm_state != 4:
            crawler.crawl_shops(number_of_pages)
            # Case were POI link is not working
            if crawler.fsm_state == 3:
                sleep(2)  # 2 second window for keyboard interrupt
                crawler.fsm_state = 2
               #crawler.crawl_pois(number_of_pages)