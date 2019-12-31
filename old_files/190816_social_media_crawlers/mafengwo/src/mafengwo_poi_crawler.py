import csv
from time import sleep
from scrapy import Selector
import pandas as pd
from selenium import webdriver
from random import randint

file = pd.read_csv('../data/mafengwo_poi_list.csv')
name_list = file['name']
link_list = file['link']
driver = webdriver.Chrome('../chromedriver')

for i in range(len(name_list)):
    # if i < 285:
    #     continue
    data = {
        'Chinese_name': [],
        'English_name': [],
        'open_time': [],
        'phone_number': [],
        'website': [],
        'introduction': [],
        'address': [],
        'review_number': [],
        'review_keywords': []
    }
    print(i, name_list[i])
    url = 'http://www.mafengwo.cn'+link_list[i]
    driver.get(url)
    sel = Selector(text=driver.page_source)
    print('Sleeping')
    if i != 0:
        sleep(randint(578, 9111)/100)
    data['Chinese_name'].append(sel.xpath('//div[@class="title"]/h1/text()').extract_first())
    data['English_name'].append(sel.xpath('//div[@class="title"]/div/text()').extract_first())
    for t in sel.xpath('//li[@class="item-time"]'):
        if t.xpath('div[@class="label"]/text()').extract_first() == '开放时间':
            data['open_time'].append(sel.xpath('div[@class="content"]/text()').extract_first())
    if len(data['open_time']) == 0:
        for t in sel.xpath('//div[@class="mod mod-detail"]/dl'):
            if t.xpath('dt/text()').extract_first() == '开放时间':
                data['open_time'].append(t.xpath('dd//text()').extract())

    data['phone_number'].append(sel.xpath('//li[@class="item-tel"]/div[@class="content"]/text()').extract_first())
    data['website'].append(sel.xpath('//li[@class="item-site"]/div[@class="content"]/a/text()').extract_first())
    data['introduction'].append(sel.xpath('//div[@class="summary"]//text()').extract())
    data['address'].append(sel.xpath('//div[@class="address"]/text()').extract_first())
    if not data['address'][0]:
        data['address'] = []
        data['address'].append(sel.xpath('//div[@class="mod mod-location"]/div[@class="mhd"]/p[@class="sub"]/text()').extract_first())

    data['review_number'].append(sel.xpath('//div[@class="mod mod-reviews"]/div[@class="mhd mhd-large"]/span/em/text()').extract_first())
    keyword = ''
    for w in sel.xpath('//div[@class="review-nav"]/ul//text()').extract():
        if '\n' in w:
            pass
        else:
            keyword += w
    keyword = keyword.replace('全部', '')
    data['review_keywords'].append(keyword)

    for key in data:
        if len(data[key]) == 0:
            data[key].append('NULL')
        elif not data[key][0]:
            data[key] = []
            data[key].append('NULL')
    print(data)
    if i == 0:
        df = pd.DataFrame(data)
        df.to_csv('../data/mafengwo_poi.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
    else:
        df = pd.DataFrame(data)
        old_df = pd.read_csv('../data/mafengwo_poi.csv', index_col=[0])
        new_df = pd.concat([old_df, df], ignore_index=True, sort=False)
        new_df.to_csv('../data/mafengwo_poi.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)

print('Finished.')
driver.quit()