import pandas as pd
import json
import urllib3
import re
import twint
import mysql.connector
from time import sleep
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from random import randint
from urllib.parse import quote
from scrapy import Selector

from utils import insert_into_table

def construct_url(platform,
                  key,
                  end_date=datetime.now().strftime('%Y-%m-%d'),
                  duration=4):

    if platform == 'instagram':
        url = 'https://www.instagram.com/graphql/query/?query_hash=1b84447a4d8b6d6d0426fefb34514485&variables='
        url += quote('{"id":' + '"' + str(key) + '"' + ',"first":50}')
        return url

    if platform == 'twitter':
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = (end_date - timedelta(days=duration)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        url = 'https://twitter.com/search?l=&q='
        url += quote(key)
        url += '%20near%3A%22Singapore%22%20within%3A15mi'
        url += '%20since%3A' + start_date + '%20until%3A' + end_date
        return url

    else:
        print('Error at construct_url(): Please check your platform entry.')

def extract_twitter_profile(user_name, user_id, cnx, cursor):

    # Check if user_name already exist in twitter_user table.
    cursor.execute(
        """
        SELECT * FROM twitter_users WHERE user_id = {}
        """.format('"' + user_id + '"')
    )

    twitter_user = cursor.fetchall()

    # If user not in table, insert info into table.
    if not twitter_user:
        c = twint.Config()
        c.Format = None
        c.Geo = None
        c.Store_object = True
        c.Hide_output = True
        c.Username = user_name
        twint.run.Lookup(c)

        user = twint.output.users_list[-1]
        crawled_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        col_names = ('user_id',
                     'user_name',
                     'raw_home_location',
                     'image_url',
                     'crawled_time')

        entry = (str(user.id),
                 user.username,
                 user.location,
                 user.avatar,
                 crawled_time)

        insert_script = insert_into_table(table='twitter_users',
                                          col_names=col_names,
                                          entry=entry)

        cursor.execute(insert_script)

        cnx.commit()


def convert_tweets_datetime(date_time_str):
    return str(datetime.strptime(date_time_str, '%I:%M %p - %d %b %Y'))

def extract_data(platform, keyword, cnx, cursor, data=None, driver=None):
    if platform == 'instagram':
        for post in data['data']['location']['edge_location_to_media']['edges']:

            # Selecting only the required data.
            number_id = post['node']['id']
            user_id = post['node']['owner']['id']
            timestamp = datetime.fromtimestamp(post['node']['taken_at_timestamp'])
            post_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            try:
                caption = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
                caption = re.sub(r'"', r'\"', caption)
            except IndexError:
                caption = 'None'

            # Insert into MySQL database.
            cursor.execute(
                """
                INSERT INTO instagrams (
                    number_id,
                    user_id,
                    keyword,
                    post_time,
                    caption
                )
                VALUES ({}, {}, {}, {}, {});
                """.format(
                    '"' + number_id + '"',
                    '"' + user_id + '"',
                    '"' + keyword + '"',
                    '"' + post_time + '"',
                    '"' + caption + '"'
                )
            )

            cnx.commit()

    if platform == 'twitter':

        sel = Selector(text=driver.page_source)
        tweet_list = sel.xpath('//ol/li[@data-item-type="tweet"]')

        for tweet in tweet_list:

            # Selecting only the required data.
            user_id = tweet.xpath('div/div[@class="content"]/div/a/@data-user-id').extract_first()
            user_name = tweet.xpath('div/div[@class="content"]/div/a/span/b/text()').extract_first()
            post_time = tweet.xpath('div/div[@class="content"]/div/small[@class="time"]/a/@title').extract_first()
            post_time = convert_tweets_datetime(post_time)
            text_list = tweet.xpath('div/div[@class="content"]/div[@class="js-tweet-text-container"]/*//text()').extract()
            text = ''
            for j in text_list:
                text += j
            tweet = re.sub(r'"', r'\"', text)
            crawled_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            col_names = ('user_id',
                         'user_name',
                         'keyword',
                         'keyword_or_latlong',
                         'post_time',
                         'tweet',
                         'crawled_time')

            entry = (user_id,
                     user_name,
                     keyword,
                     'keyword',
                     post_time,
                     tweet,
                     crawled_time)

            insert_script = insert_into_table(table='tweets',
                                              col_names=col_names,
                                              entry=entry)

            cursor.execute(insert_script)

            extract_twitter_profile(user_name=user_name,
                                    user_id=user_id,
                                    cnx=cnx,
                                    cursor=cursor)

            cnx.commit()

def crawl_instagram():

    # Get poi information into df.
    poi_df = pd.read_csv('poi.csv')
    pk_list = list(poi_df['pk'])
    poi_list = list(poi_df['poi_name'])

    http = urllib3.PoolManager()
    urllib3.disable_warnings()

    # Initialize MySQL connection and cursor.
    cnx = mysql.connector.connect(host='localhost',
                                  database='sentimentDB',
                                  user='test_user',
                                  password='Password123!')
    cursor = cnx.cursor(prepared=True)
    cursor.execute('SET NAMES utf8mb4')
    print('Connection to MySQL server made.\n')

    for index, pk in enumerate(pk_list):
        keyword = poi_list[index]
        print(keyword)
        url = construct_url(platform='instagram', key=pk)
        response = http.request('GET', url)
        if response.status == 200:
            json_result = json.loads(response.data)
            try:
                extract_data(platform='instagram',
                             keyword=keyword,
                             cnx=cnx,
                             cursor=cursor,
                             data=json_result)
                cnx.commit()
            except TypeError as e:
                print('##### EXCEPTION #####')
                print(e)
                print('#####################')
                with open('exception_instagram', 'w') as outfile:
                    outfile.write(str(pk) + '\n')
                    sleep(300)

    cursor.close()
    cnx.close()


def crawl_twitter(end_date=datetime.now().strftime('%Y-%m-%d'), duration=4):

    # Get poi information into df.
    poi_df = pd.read_csv('poi_twitter.csv')
    poi_list = list(poi_df['POI_DESC'])
    poi_lat = list(poi_df['LATITUDE'])
    poi_long = list(poi_df['LONGITUDE'])

    # Initialize MySQL connection and cursor.
    cnx = mysql.connector.connect(host='localhost',
                                  database='sentimentDB',
                                  user='test_user',
                                  password='Password123!')
    cursor = cnx.cursor(prepared=True)
    cursor.execute('SET NAMES utf8mb4')
    print('Connection to MySQL server made.\n')

    def load_more_results(driver):
        for i in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)

    driver = webdriver.Chrome('./chromedriver')

    for i, keyword in enumerate(poi_list):
        _lat, _long = str(poi_lat[i]), str(poi_long[i])
        print(keyword, (_lat, _long))

        # Get tweets by lat/long.
        r = '0.1km'
        c = twint.Config()
        c.Format = None
        c.Username = None
        c.Geo = _lat + ',' + _long + ',' + r
        c.Store_object = True
        c.Hide_output = True
        c.Limit = 10
        twint.run.Search(c)
        tweets = twint.output.tweets_list #list of c limit objects

        # Insert into MySQL database.
        for t in tweets:
            user_id = str(t.user_id)
            user_name = t.username
            tweet = re.sub(r'"', r'\"', t.tweet)
            ts = t.datetime/1000
            post_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            crawled_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            col_names = ('user_id',
                         'user_name',
                         'keyword',
                         'latitude',
                         'longitude',
                         'keyword_or_latlong',
                         'post_time',
                         'tweet',
                         'crawled_time')

            entry = (user_id,
                     user_name,
                     keyword,
                     _lat,
                     _long,
                     'latlong',
                     post_time,
                     tweet,
                     crawled_time)

            insert_script = insert_into_table(table='tweets',
                                              col_names=col_names,
                                              entry=entry)

            cursor.execute(insert_script)

            extract_twitter_profile(user_name=user_name,
                                    user_id=user_id,
                                    cnx=cnx,
                                    cursor=cursor)

        cnx.commit()

        # Get tweets by keyword.
        url = construct_url(platform='twitter',
                            key=keyword,
                            end_date=end_date,
                            duration=duration)
        driver.get(url)
        sleep(randint(0, 30))
        load_more_results(driver)

        try:
            extract_data(platform='twitter',
                         keyword=keyword,
                         cnx=cnx,
                         cursor=cursor,
                         driver=driver)
            cnx.commit()

        except:
            print("An error has occured.")
            with open('exception_twitter', 'w') as outfile:
                outfile.write(str(keyword) + '\n')
                sleep(300)

    driver.quit()
    cursor.close()
    cnx.close()
