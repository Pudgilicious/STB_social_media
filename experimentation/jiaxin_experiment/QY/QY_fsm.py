#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:17:35 2020

@author: jia
"""

from time import sleep
from QY_crawler import QYCrawler

class QY_FSM:
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.crawler = QYCrawler(chromedriver_path, poi_df, cnx, db_out_flag)


    def start(self,number_of_pages=None):
        crawler = self.crawler
        while crawler.fsm_state != 4:
            crawler.crawl_pois(number_of_pages)
            # Case were POI link is not working
            if crawler.fsm_state == 3:
                sleep(2)  # 2 second window for keyboard interrupt
                print('exccccuuuuutttttttttiiiiiinnnnnggg')
                crawler.fsm_state = 2
                crawler.crawl_pois(number_of_pages)

#state 0: initialization
#state 1: start crawling
#state 2: transition between 3 and 1
#state 3: crashed
#sstate 4: final