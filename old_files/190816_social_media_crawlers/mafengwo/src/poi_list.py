#This script gets poi list from mafengwo

from selenium import webdriver
from scrapy import Selector
from time import sleep
import pandas as pd
import csv
from random import randint

driver = webdriver.Chrome('../chromedriver')
url = 'http://www.mafengwo.cn/jd/10754/gonglve.html'
driver.get(url)

for i in range(20):  #Loop 20 pages
    data = {
        'name': [],
        'link': []
    }
    # if i < 20:
    #     continue
    print('Sleeping...')
    if not i == 0:
        sleep(randint(977, 4565)/10)
    sel = Selector(text=driver.page_source)
    data['name'] = sel.xpath('//div[@class="bd"]/ul[@class="scenic-list clearfix"]/li/a/@title').extract()   #Get the title of poi
    data['link'] = sel.xpath('//div[@class="bd"]/ul[@class="scenic-list clearfix"]/li/a/@href').extract()    #Get the link 
    print(i, data['name'])
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if i == 0:
        driver.execute_script("window.scrollTo(0, 3000);")
        driver.maximize_window()
    else:
        pass

    if i == 0:
        df = pd.DataFrame(data)
        df.to_csv('../data/mafengwo_poi_list.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
    else:
        df = pd.DataFrame(data)
        old_df = pd.read_csv('../data/mafengwo_poi_list.csv', index_col=[0])
        new_df = pd.concat([old_df, df], ignore_index=True, sort=False)
        new_df.to_csv('../data/mafengwo_poi_list.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
    next_page = driver.find_element_by_link_text('后一页')
    sleep(1.2)
    if i == 19:
        break
    else:
        next_page.click()
    # next_page.send_keys('\n')

