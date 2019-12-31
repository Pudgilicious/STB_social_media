from selenium import webdriver
from scrapy import Selector
import pandas as pd
from time import sleep
from random import randint
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import csv


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


file = pd.read_csv('area_list.csv')
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(70)

# First part of the url
url_1 = 'https://www.instagram.com'

area_list = file['area_list']
result_file = pd.read_csv('poi_url.csv')
urls_done = list(set(result_file['area']))

index = 0
while index < 155:
    area = area_list[index]
    # if index < 31:
    #     continue
    if area in urls_done:
        index += 1
        # print('continue', index)
        continue
    dic = {}
    url = url_1 + area
    driver.get(url)
    sleep(randint(1923, 3278)/500)

    try:
        see_more_button = driver.find_elements_by_link_text('See More')[0]
    except IndexError:
        sel = Selector(text=driver.page_source)
        if sel.xpath('//div[@class="error-container -cx-PRIVATE-ErrorPage__errorContainer -cx-PRIVATE-ErrorPage__errorContainer__"]/h2/text()').extract_first() ==  '''Sorry, this page isn't available.''':
            with open('exception2', 'a') as exfile:
                exfile.write(str(index) + ',')
                index += 1
                print('Broken url')
                continue
        else:
            if sel.xpath('//a[@class="sfiKI"]/text()').extract_first() == 'Singapore':
                print('Just no see_more_button')
            else:
                print('Banned. Long sleep and try again.')
                sleep(randint(10412, 12987)/10)
                continue

    while True:
        try:
            see_more_button.click()
            sleep(randint(192, 278) / 200)
        except StaleElementReferenceException:
            break

    sel = Selector(text=driver.page_source)

    poi_name_list = sel.xpath('//div[@class="jLdQ3"]/ul[@class="gGvEF"]/li/a/text()').extract()
    poi_url_list = sel.xpath('//div[@class="jLdQ3"]/ul[@class="gGvEF"]/li/a/@href').extract()
    dic['poi_name'] = poi_name_list
    dic['poi_url'] = poi_url_list
    area_list2 = [area]*len(poi_name_list)
    dic['area'] = area_list2
    try:
        df = pd.DataFrame(dic)
    except ValueError as e:
        print(e)
        index += 1
        with open('exception', 'a') as exfile:
            exfile.write(str(index)+',')
        continue

    df.to_csv('poi_url.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False, mode='a', header=0)

    print(index)
    index += 1
    print('Processed:', round((index+1)/len(area_list)*100, 2), '%')


print('Finished.')
driver.quit()
