import pandas as pd
import json
import urllib3
import csv
import re
from time import sleep
import random
from urllib3.contrib.socks import SOCKSProxyManager
from urllib3.connectionpool import MaxRetryError
from datetime import datetime

# status_count is the weibo number


def get_proxies():
    import requests

    API_URL = "http://list.didsoft.com/get?email=akhtung@gmail.com&pass=b9nkja&pid=sockspremium"

    response = requests.get(API_URL)
    proxies_text = response.text.split("\n")
    proxies = []
    for proxy_text in proxies_text:
        proxy_split = proxy_text.split("#")
        # if len(proxy_split[0]) > 2 and proxy_split[2] is not "CN":
        if len(proxy_split[0]) > 2:
            proxy = {"https":(proxy_split[1]+"://"+proxy_split[0])}
            proxies.append(proxy)
    return proxies


def proxy_check_simple(proxies):
    import requests
    from requests.exceptions import ConnectionError, ProxyError
    good_proxies = []
    proxy_list = []
    def check(proxy):
        try:
            response = requests.get("https://ipapi.co/json/", proxies = proxy, timeout = 10)
            good_proxies.append(proxy)
            print(str(proxy) + " is good.")
        except ProxyError:
            print(str(proxy) + " is not responding.")
        except ConnectionError:
            print(str(proxy) + " connection denied.")
        except:
            print(str(proxy) + " exceeded timeout or other errors.")
    count = 0
    for proxy in proxies:
        check(proxy)
        count += 1
        print(str(count) + '/' + str(len(proxies)) + ' tested.')
        if len(good_proxies) == 20:
            break
        # if count == 11:
        #     break
    return good_proxies

# url = 'https://m.weibo.cn/api/container/getIndex?title=%E4%BD%8D%E7%BD%AE&containerid=100101B2094757D16DA6F54993_-_weibofeed&luicode=10000011&lfid=1001018006500000000000000_-_poilist&page=0'
url = 'https://m.weibo.cn/api/container/getIndex?title=%E4%BD%8D%E7%BD%AE&containerid=100101B2094757D16DA6F54993_-_weibofeed&luicode=10000011&lfid=1001018006500000000000000_-_poilist&page='
url = url.replace('/p/index?', '/api/container/getIndex?')
url = url.replace(re.findall('&luicode=\d+', url)[0], '_-_weibofeed'+re.findall('&luicode=\d+', url)[0])
file = pd.read_csv('poi_list.csv')
proxies = get_proxies()                   ##comment out for non proxies
good_proxies = proxy_check_simple(proxies) ##comment out for non proxies


http = urllib3.PoolManager(timeout=26)

dic_keys = ['weibo_url', 'post_time', 'text', 'source', 'mid', 'user_id', 'screen_name', 'profile_url', 'statuses_count', 'verified', 'verified_type', 'user_description', 'gender', 'user_rank', 'mbrank', 'followers_count', 'follow_count', 'cover_image_phone', 'avatar', 'reposts_count', 'comments_count', 'attitudes_count', 'more_info_type', 'location', 'pictures', 'desc_more', 'mblog_vip_type', 'is_paid', 'badge', 'video', 'crawled_time']
dic = {}
for key in dic_keys:
    dic[key] = list()


def renewdic():
    for key in dic_keys:
        dic[key] = list()


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_user_info():
    url = 'https://m.weibo.cn/api/container/getIndex?uid=1767156601&luicode=10000011&lfid=100101B2094757D16DA6F54993_-_weibofeed&type=uid&value=1767156601&containerid=2302831767156601'


def write_first(dic):
    df = pd.DataFrame(dic)
    df.to_csv('weibo_data.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)


def get_response(url):
    global good_proxies
    response = http.request('GET', url)
    count_no_response = 0
    while count_no_response < 4:
        # print(response.data)
        if len(response.data) == 0 or json.loads(response.data)['ok'] == 0:
            count_no_response += 1
            print('Empty response')
            print('No Response: ' + str(count_no_response))
            print('Count:' + str(count))
            print('Request: ' + str(i))
            # sleep(5)

            work_flag = False
            while not work_flag:
                proxy = SOCKSProxyManager(good_proxies[random.randint(0, len(good_proxies) - 1)]['https'])
                try:
                    response = proxy.request('GET', url)
                    work_flag = True
                except MaxRetryError:
                    good_proxies = proxy_check_simple(proxies)
                    # response = proxy.request('GET', url)
            # if len(response.data) == 0 or json.loads(response.data)['ok'] == 0:
            #     count_no_response += 1
            #     print('No Response: ' + str(count_no_response))
            #     if count_no_response == 10:
            #         return response
            #     get_response(url, count_no_response)
            # else:
            #     return response
        else:
            return response


def write_file(dic):
    old_df = pd.read_csv('weibo_data.csv')
    new_df = pd.DataFrame(dic)
    df = pd.concat([old_df, new_df], ignore_index=True, sort=False)
    df.to_csv('weibo_data.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)


count = 0

poi_length = len(file['scheme'])
for index, u in enumerate(file['scheme']):

    continueno_response_count = 0
    # if count == 300:
    #     break
    # if count < 16:
    #     count += 1
    #     continue
    print(str(index) + '/' + str(poi_length))
    print('Sleeping...')
    # sleep(random.randint(223, 1032) / 10)
    jr1 = ''
    jr2 = ''
    # The quest send for each poi
    for i in range(1, 100):
        time_flag = False
        if continueno_response_count > 3:
            break
        print('\nRequest: ' + str(i))
        if i == 1:
            u = u.replace('/p/index?', '/api/container/getIndex?')
            u = u.replace(re.findall('&luicode=\d+', url)[0], '_-_weibofeed' + re.findall('&luicode=\d+', url)[0])
        else:
            pass
        # print('URL: ' + u)

        result = get_response(u + '&page=' + str(i))

        try:
            json_result = json.loads(result.data)
            if json_result == jr1 == jr2:
                break
            else:
                jr2 = jr1
                jr1 = json_result
        except AttributeError:
            continueno_response_count += 1
            continue

        print('OK: ' + str(json_result['ok']))
        location_name = json_result['data']['pageInfo']['page_title']

        # with open('/Users/admin/Desktop/STB/untitled/raw_data/' + location_name + str(i) + get_current_time(), 'w') as outfile:
        #     json.dump(json_result, outfile)

        for card in json_result['data']['cards']:
            if card['card_id'] == 'card_hq_poiweibo':
                data = card

        # data = json_result['data']['cards'][0]

        for weibo in data['card_group']:
            try:
                a = weibo['mblog']['created_at']
            except KeyError:
                continue
            print(location_name)
            dic['weibo_url'].append(weibo['scheme'])
            dic['post_time'].append(weibo['mblog']['created_at'])
            dic['mid'].append(weibo['mblog']['mid'])
            dic['text'].append(weibo['mblog']['text'])
            dic['source'].append(weibo['mblog']['source'])
            dic['is_paid'].append(weibo['mblog']['is_paid'])
            dic['mblog_vip_type'].append(weibo['mblog']['mblog_vip_type'])
            dic['user_id'].append(weibo['mblog']['user']['id'])
            dic['screen_name'].append(weibo['mblog']['user']['screen_name'])
            print('Name: ' + dic['screen_name'][-1])
            print('Check in time: ' + dic['post_time'][-1])
            dic['profile_url'].append(weibo['mblog']['user']['profile_url'])
            dic['statuses_count'].append(weibo['mblog']['user']['statuses_count'])
            dic['verified'].append(weibo['mblog']['user']['verified'])
            dic['verified_type'].append(weibo['mblog']['user']['verified_type'])
            dic['user_description'].append(weibo['mblog']['user']['description'])
            dic['gender'].append(weibo['mblog']['user']['gender'])
            dic['user_rank'].append(weibo['mblog']['user']['urank'])
            dic['mbrank'].append(weibo['mblog']['user']['mbrank'])
            dic['followers_count'].append(weibo['mblog']['user']['followers_count'])
            dic['follow_count'].append(weibo['mblog']['user']['follow_count'])
            dic['cover_image_phone'].append(weibo['mblog']['user']['cover_image_phone'])
            dic['avatar'].append(weibo['mblog']['user']['avatar_hd'])
            dic['reposts_count'].append(weibo['mblog']['reposts_count'])
            dic['comments_count'].append(weibo['mblog']['comments_count'])
            dic['attitudes_count'].append(weibo['mblog']['attitudes_count'])
            dic['more_info_type'].append(weibo['mblog']['more_info_type'])
            dic['location'].append(location_name)

            if '前' in dic['post_time'][-1]:
                time_flag = True
            if '天' in dic['post_time'][-1]:
                time_flag = True

            # The pictures
            picture_str = ''
            try:
                for i in weibo['mblog']['pics']:
                    picture_str += (i['large']['url']) + ' '
                dic['pictures'].append(picture_str)
            except KeyError:
                # No pictures in this blog
                dic['pictures'].append('No Picture')

            # The videos
            try:
                type = weibo['mblog']['page_info']['type']
                if type == 'video':
                    dic['video'].append(weibo['mblog']['page_info']['media_info']['stream_url_hd'])
                else:
                    dic['video'].append('No video')
            except KeyError:
                dic['video'].append('No video')


            badge_str = ''
            try:
                badge = weibo['mblog']['user']['badge']
                for i in badge:
                    badge_str += i+': '+ str(badge[i]) + '&'
                dic['badge'].append(badge_str)
            except KeyError:
                dic['badge'].append('No badge')

            dic['desc_more'].append(json_result['data']['pageInfo']['desc_more'])
            dic['crawled_time'].append(get_current_time())

        write_file(dic)
        renewdic()
        if not time_flag:
            print('No more recent visitors.')
            count += 1
            break
    # write_first(dic)
    count += 1




