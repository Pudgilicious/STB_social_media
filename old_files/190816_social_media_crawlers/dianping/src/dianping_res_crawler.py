import pandas as pd
from selenium import webdriver
from scrapy import Selector
from time import sleep
import csv
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('../chromedriver')
url = 'https://www.dianping.com/singapore/food/'

driver.get(url)
page_number = 1
while True:
    data = {
        'name': [],
        'tags': [],
        'service': [],
        'environment': [],
        'taste': [],
        'price': [],
        'review_number': [],
        'address': [],
        'features': [],
        'stars': []
    }
    print('Page:', page_number)
    # if page_number < 2:
    #     page_number += 1
    #     continue
    sleep(1)
    sel = Selector(text=driver.page_source)
    sleep(1)
    shops = sel.xpath('//div[@id="searchList"]/dl/dd')
    for shop in shops:
        data['name'].append(shop.xpath('ul[@class="detail"]/li[@class="shopname"]/a/text()').extract_first())
        tag_list = shop.xpath('ul[@class="detail"]/li[@class="tags"]/a/text()').extract()
        tags  = ''
        for i in tag_list:
            tags += i + ' '
        data['tags'].append(tags)
        data['service'].append(shop.xpath('ul[@class="remark"]/li[@class="grade"]/span[@class="score3"]/text()').extract_first())
        data['environment'].append(shop.xpath('ul[@class="remark"]/li[@class="grade"]/span[@class="score2"]/text()').extract_first())
        data['taste'].append(shop.xpath('ul[@class="remark"]/li[@class="grade"]/span[@class="score1"]/text()').extract_first())
        data['price'].append(shop.xpath('strong[@class="average"]/text()').extract_first())
        data['review_number'].append(shop.xpath('ul[@class="remark"]/li/a/text()').extract_first())
        data['address'].append(shop.xpath('ul[@class="detail"]/li[@class="address"]/text()').extract()[1])
        feature_list = shop.xpath('ul[@class="detail"]/li[@class="features"]/a')
        tmp = ''
        for dish in feature_list:
            recommand_number = dish.xpath('@title').extract_first()
            tmp = tmp + recommand_number + '\n'
            for c in dish.xpath('text()').extract():
                tmp += c
            tmp += '\n'
        data['features'].append(tmp)
        data['stars'].append(shop.xpath('ul[@class="remark"]/li/span/@title').extract_first())

    df = pd.DataFrame(data)
    if page_number == 1:
        df.to_csv('../data/dianping_res.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
    else:
        df.to_csv('../data/dianping_res.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, mode='a', header=False)
    # Go to next page
    try:
        next_page_button = driver.find_element_by_link_text('下一页')
        sleep(2)
        next_page_button.send_keys('\n')
        page_number += 1
    except NoSuchElementException:
        print('No next page.')
        driver.quit()



