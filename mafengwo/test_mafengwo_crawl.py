#Using this script to test out mafengwo pages

from selenium import webdriver
from scrapy import Selector
from scrapy.http import HtmlResponse
import pandas as pd
import csv
import re
from time import sleep
from datetime import date

driver = webdriver.Chrome('./chromedriver')

url = "https://www.mafengwo.cn/poi/5422487.html"

driver.get(url)

#Get review title
#/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[1]/a
#/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[2]/a

#Get review body
#/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[1]/p/text()
#/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[2]/p/text()

#Get ratings
#/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[1]/span
#/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[2]/span

#Get 

