#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:12:26 2020

@author: jia
"""

from time import sleep
from Ctrip_crawler import CtripCrawler

class Ctrip_FSM:
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.crawler = CtripCrawler(chromedriver_path, poi_df, cnx, db_out_flag)


    def start(self,number_of_pages=None, proxy_mode=None,timeout=None,authen_count=None):
        crawler = self.crawler
        while crawler.fsm_state != "4_complete":
            crawler.crawl_pois(number_of_pages,proxy_mode,timeout,authen_count)
            # Case were POI link is not working
            if crawler.fsm_state == "3_crash":
                sleep(2)  # 2 second window for keyboard interrupt
                crawler.fsm_state = "2_error_handling"
               #crawler.crawl_pois(number_of_pages)

#state 0: initialization   0_init
#state 1: start crawling   1_normal
#state 2: transition between 3 and 1    2_error_handling
#state 3: crashed      3_crash
#sstate 4: final       4_complete