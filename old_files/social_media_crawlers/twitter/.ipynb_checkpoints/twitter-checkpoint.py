# This script is to get the list of possible visitors of Singapore from Twitter
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import Selector
import pandas as pd
from datetime import datetime
import csv
from time import sleep
import urllib3
import re
from random import randint
from datetime import timedelta

driver = webdriver.Chrome('./twitter/chromedriver')


def construct_url(key_word):
    key_word = key_word.replace(' ', '%20')
    u = 'https://twitter.com/search?q=Marina%20Bay%20Sands%20near%3A%22Singapore%22%20within%3A15mi'
    url1 = 'https://twitter.com/search?l=&q='
    url2 = '%20near%3A%22Singapore%22%20within%3A15mi'
    start_date = (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    url3 = '%20since%3A' + start_date + '%20until%3A' + end_date
    return url1 + key_word + url2 + url3


def load_more_results(driver):
    for i in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)


def extract_data(driver, data_dic, i):
    sel = Selector(text=driver.page_source)
    tweet_list = sel.xpath('//ol/li[@data-item-type="tweet"]')

    for tweet in tweet_list:
        number_id = tweet.xpath('div/div[@class="content"]/div/a/@data-user-id').extract_first()
        screen_name = tweet.xpath('div/div[@class="content"]/div/a/span/strong/text()').extract_first()
        avatar = tweet.xpath('div/div[@class="content"]/div/a/img/@src').extract_first()
        user_name = tweet.xpath('div/div[@class="content"]/div/a/span/b/text()').extract_first()
        posted_time = tweet.xpath('div/div[@class="content"]/div/small[@class="time"]/a/@title').extract_first()
        text_list = tweet.xpath('div/div[@class="content"]/div[@class="js-tweet-text-container"]/*//text()').extract()
        text = ''
        for j in text_list:
            text += j
        picture_list = tweet.xpath('div/div[@class="content"]/div[@class="AdaptiveMediaOuterContainer"]/*//@src').extract()
        picture = ''
        for j in picture_list:
            picture  = picture + j + '\n'
        # print(screen_name)
        # print(text)

        data_dic['number_id'].append(number_id)
        data_dic['screen_name'].append(screen_name)
        data_dic['avatar'].append(avatar)
        data_dic['user_name'].append(user_name)
        data_dic['posted_time'].append(posted_time)
        data_dic['text'].append(text)
        data_dic['pictures'].append(picture)
        data_dic['crawled_time'].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data_dic['keyword'].append(i)


if __name__ == '__main__':
    # file = pd.read_csv('Attractions_names.csv')
    file = pd.read_csv('./twitter/ta_poi.csv')
    # enlgish_name_list = file['English_name']
    enlgish_name_list = file['name']
    start_flag = True
    for i in enlgish_name_list:
        data_dic = dict.fromkeys(['number_id', 'screen_name', 'avatar', 'user_name', 'posted_time', 'text',
                                 'pictures', 'crawled_time', 'keyword'])
        for key in data_dic:
            data_dic[key] = list()

        # if i != 'Singapore Parliament Building':
        #     pass
        # else:
        #     start_flag = True
        # if not start_flag:
        #     continue
        print(i)
        url = construct_url(i)
        driver.get(url)
        sleep(randint(0, 30))
        load_more_results(driver)
        # sleep(60)
        extract_data(driver, data_dic, i)
        print('######\nNew Data', len(data_dic['number_id']))
        df0 = pd.read_csv('./twitter/tweets.csv', index_col=[0])
        df = pd.DataFrame(data_dic).append(df0, ignore_index=True)
        # Remove duplicate rows
        df = df.drop_duplicates()
        df.to_csv('./twitter/tweets.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)

    print(len(df))
    driver.quit()


