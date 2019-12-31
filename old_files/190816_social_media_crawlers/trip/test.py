#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 10:14:06 2019

@author: jirong
"""

from selenium import webdriver
from scrapy import Selector
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('./chromedriver')
url = "https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d12083737-Reviews-Sow_Reap_cafe-Singapore.html"
driver.get(url)

elements = driver.find_elements_by_css_selector(".header_links")
storyTitles = [el.text for el in elements]
print(storyTitles)
#storyUrls = [el.get_attribute("href") for el in elements]