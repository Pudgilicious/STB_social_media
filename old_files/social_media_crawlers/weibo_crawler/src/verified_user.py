import pandas as pd
import csv
import json
import urllib3
from urllib3.contrib.socks import SOCKSProxyManager
import re
from datetime import datetime
from time import sleep
import random

urllib3.disable_warnings()

header = {
    #'authority': 'm.weibo.cn',
    #'method': 'GET',
    #'path': '/u/2714280233?uid=2714280233&luicode=10000011&lfid=2304132714280233_-_WEIBO_SECOND_PROFILE_WEIBO',
    #'scheme': 'https',
    #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    #'accept-encoding': 'gzip, deflate, br',
    #'accept-language': 'en-US,en;q=0.9',
    #'cache-control': 'max-age=0',
    #'cookie': '',
    #'upgrade-insecure-requests': '1',
    #'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',

    #Personal info - confidential
	'authority': 'www.weibo.com',
	'method': 'GET',
	'path': '/aj/v6/user/newcard?ajwvr=6&id=1761179351&type=1&callback=STK_156593008809052',
	'scheme': 'https',
	'accept': '*/*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9,zh-SG;q=0.8,zh;q=0.7',
	'cookie': 'UOR=www.google.com,www.weibo.com,www.google.com; SINAGLOBAL=1525441123962.0125.1563516441265; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; login_sid_t=42365f95532fc7e8ec40abb36eb94654; cross_origin_proto=SSL; _ga=GA1.2.1243091386.1565929705; _gid=GA1.2.773005754.1565929705; TC-V5-G0=c9fb286cd873ae77f97ce98d19abfb61; WBStorage=4b0a0a9ea4ac3871|undefined; _s_tentry=-; Apache=349691126504.53436.1565929709606; ULV=1565929709624:2:1:1:349691126504.53436.1565929709606:1563516441278; appkey=; ALF=1597465948; SSOLoginState=1565929950; SUB=_2A25wUkGPDeRhGeFM41EX9SnEzTqIHXVTJjRHrDV8PUNbmtBeLUjhkW9NQL1Vn1puWy9BJTJVDoZ9IqWIPkd4N7UQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPKfy_lgzexX0esnAENkcy5JpX5KzhUgL.FoME1hecSKMRSoq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMf1Kz41Kece0.0; SUHB=0auANfUNx0iY4E; wvr=6; wb_view_log_7283657866=1024*7681; TC-Page-G0=153ff31dae1cf71cc65e7e399bfce283|1565930089|1565930089; WBtopGlobal_register_version=307744aa77dd5677; webim_unReadCount=%7B%22time%22%3A1565930102323%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'


}


# In cards 0
account_data = {'昵称': 'screen_name', '简介': 'description', '等级': 'rank', '注册时间': 'registered time', '阳光信用': 'credit',
                'verified_type': 'verified_type'
                }

personal_data = {'性别': 'gender', '生日': 'birthday', '所在地': 'address', '大学': 'college', '高中': 'high_school', '初中':
    'junior high school', '小学': 'primary_school', '公司': 'company', '家乡': 'hometown', '海外': 'oversea???',
                 '感情状况': 'relationship', '昵称': 'nickname', '简介': 'description', '中专技校': 'technical school',
                 '审核时间': 'company_verified_time',
                 '高职': 'vocational school'}

influence_data = {'weibo_yesterday_number': 'weibo_yesterday_number',
                  'weibo_yesterday_interaction': 'weibo_yesterday_interaction',
                  'review_yesterday_interaction': 'review_yesterday_interaction',
                  'story_yesterday_interaction': 'story_yesterday_interaction'}

places_been_to_data = {'total': 'total_country_number', 'title_sub': 'country',
                       'last_check_in_time': 'last_check_in_time',
                       'check_in_times': 'check_in_times'}


def create_dic(account_data, personal_data, influence_data):
    dic = {}
    for key in account_data.keys():
        dic[account_data[key]] = list()
    for key in personal_data.keys():
        dic[personal_data[key]] = list()
    for key in influence_data.keys():
        dic[influence_data[key]] = list()
    for key in places_been_to_data.keys():
        dic[places_been_to_data[key]] = list()
    return dic


def construct_basic_profile_api(uid):
    basic_profile_uid = '230283' + uid
    basic_api_1 = 'https://m.weibo.cn/api/container/getIndex?containerid='
    basic_api_2 = '_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid='

    return basic_api_1 + basic_profile_uid + basic_api_2 + basic_profile_uid


# This api returns the data of places a visitor has been to in Singapore
def construct_places_api(uid):
    basic_profile_uid = '230283' + uid
    place_list_pai_1 = 'https://m.weibo.cn/api/container/getIndex?containerid=2310340004&count=10&extparam=uid,'
    place_list_api_2 = '&title=%E5%8E%BB%E8%BF%87%E7%9A%84%E5%9B%BD%E5%AE%B6%E5%92%8C%E5%9C%B0%E5%8C%BA&luicode=10000011&lfid=2310340013'
    # place_list_api_3 = '_-_INFO'
    return place_list_pai_1 + uid + place_list_api_2


def construct_user_influence_api(uid):
    influence_uid = '231353' + uid
    basic_profile_uid = '230283' + uid
    influence_api_1 = 'https://m.weibo.cn/api/container/getIndex?containerid='
    influence_api_2 = '&luicode=10000011&lfid='

    return influence_api_1 + influence_uid + influence_api_2 + basic_profile_uid


def extract_influence_data(json_file):
    global dic
    # data = json_file['data']['cards']
    # weibo_yesterday_number = data[0]['card_group'][1]['group'][0]['item_title']
    # weibo_yesterday_interaction = data[1]['card_group'][2]['group'][0]['item_title']
    # review_yesterday_interaction = data[1]['card_group'][2]['group'][1]['item_title']
    # story_yesterday_interaction = data[1]['card_group'][2]['group'][2]['item_title']
    # dic['weibo_yesterday_number'].append(weibo_yesterday_number)
    # dic['weibo_yesterday_interaction'].append(weibo_yesterday_interaction)
    # dic['review_yesterday_interaction'].append(review_yesterday_interaction)
    # dic['story_yesterday_interaction'].append(story_yesterday_interaction)
    dic['weibo_yesterday_number'].append('stope crawling this')
    dic['weibo_yesterday_interaction'].append('stope crawling this')
    dic['review_yesterday_interaction'].append('stope crawling this')
    dic['story_yesterday_interaction'].append('stope crawling this')


def extract_personal_account_data(json_file):
    data = json_file['data']['cards']

    for part in data:
        # print(part)
        # print('\n')
        if len(part['card_group']) == 0:
            continue
        if part['card_group'][0]['desc'] == '账号信息':

            # account data extraction
            for item in part['card_group']:
                if item['card_type'] == 42:
                    pass
                elif item['card_type'] == 41:
                    if 'item_name' in item.keys():
                        if item['item_name'] == 'Tap to set alias':
                            pass
                        else:
                            dic[account_data[item['item_name']]].append(item['item_content'])
                    elif 'item_type' in item.keys():
                        if item['item_type'] == 'verify_yellow' or 'verify_blue':
                            dic['verified_type'].append(item['item_content'])
                        else:
                            print('Attention!' ' New item_type:')
                            print(item['item_type'])
                else:
                    print('Attention! New card_type: ')
                    print(item['card_type'])

        elif part['card_group'][0]['desc'] == '个人信息':

            # personal data extraction
            for item in part['card_group']:
                if item['card_type'] == 42:
                    pass
                elif item['card_type'] == 41:
                    if 'item_name' in item.keys():
                        dic[personal_data[item['item_name']]].append(item['item_content'])
                    else:
                        if 'blank' in dic.keys():
                            dic['blank'][0] += '\n' + item['item_content']
                        else:
                            # print(item)
                            dic['blank'] = list()
                            dic['blank'].append(item['item_content'])
                else:
                    print('Attention! New card_type: ')
                    print(item['card_type'])
        elif part['card_group'][0]['desc'] == '签到足迹':
            pass
        else:
            print('Attention! ')
            print(part['card_group'][0]['desc'])

    for key in personal_data:
        if len(dic[personal_data[key]]) == 0:
            dic[personal_data[key]].append('none')
    for key in account_data:
        if len(dic[account_data[key]]) == 0:
            dic[account_data[key]].append('none')


# It returns the page number of the place list
def extract_places_data(json_file, first_flag):
    data = json_file['data']
    # print(data.keys())
    if first_flag:
        dic['total_country_number'].append(data['cardlistInfo']['total'])
    # print(data)
    # print('\n')
    for place in data['cards'][0]['card_group']:
        # print(place)
        # print('\n')
        if len(dic['country']) == 0:
            dic['country'].append(place['title_sub'])
        else:
            dic['country'][0] += '\n' + place['title_sub']

        last_time = place['desc1'].split('，')[0]
        # print(last_time)
        total_times_for_a_place = place['desc1'].split('，')[1]
        # print(total_times_for_a_place)

        if len(dic['last_check_in_time']) == 0:
            dic['last_check_in_time'].append(last_time)
        else:
            dic['last_check_in_time'][0] += '\n' + last_time
            # print(last_time)

        if len(dic['check_in_times']) == 0:
            dic['check_in_times'].append(total_times_for_a_place)
        else:
            dic['check_in_times'][0] += '\n' + total_times_for_a_place
            # print(total_times_for_a_placep)

    return data['cardlistInfo']['page']


def handle_empty_places_data():
    pass


def write_file(dic):
    old_df = pd.read_csv('./output/user_data.csv')
    new_df = pd.DataFrame(dic)
    print(new_df[['screen_name', 'uid', 'verified_type', 'gender', 'total_country_number']])
    print('\n')
    df = pd.concat([old_df, new_df], ignore_index=True, sort=False)
    df.to_csv('./output/user_data.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def request_json(api, http):
    r = http.request('GET', api, headers=header)
    js = json.loads(r.data)
    return js


def proxy_request_json(api, proxy):
    r = proxy.request('GET', api, headers=header)
    js = json.loads(r.data)
    return js


def add_time_and_uid(uid, dic):
    dic['uid'] = uid
    dic['crawled_time'] = get_current_time()


if __name__ == '__main__':

    dic = create_dic(account_data, personal_data, influence_data)
    # empty_df = pd.DataFrame(dic)
    # empty_df.to_csv('user_data.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)

    file = pd.read_csv('./data/target_verified_user.csv')
    file2 = pd.read_csv('./output/user_data.csv')
    http = urllib3.PoolManager()

    count = 0
    for index, u in enumerate(file['user_id']):

        # if count <= 209:
        #     count += 1
        #     continue
        print('Sleeping...')
        sleep(random.randint(200, 2700) / 10)

        try:
            inf_json = ''
            dic = create_dic(account_data, personal_data, influence_data)
            uid = str(file['user_id'][index])
            add_time_and_uid(uid, dic)
            basic_api = construct_basic_profile_api(uid)
            inf_api = construct_user_influence_api(uid)
            places_api = construct_places_api(uid)

            basic_json = request_json(basic_api, http)
            extract_personal_account_data(basic_json)

            first_flag = True
            places_json = request_json(places_api, http)
            page = extract_places_data(places_json, first_flag)
            # There may be many pages of the places list
            if page:
                first_flag = False
                page_number = 2
                while page > 1:
                    places_api = construct_places_api(uid) + '&page=' + str(page_number)
                    page_number += 1
                    page -= 1
                    places_json = request_json(places_api, http)
                    extract_places_data(places_json, first_flag)
            else:
                pass

            # Stop crawling the influence data

            extract_influence_data(inf_json)

            print('Count: ' + str(count))
        except KeyError as e:
            print('KeyError!')
            print('Influence:')
            print(inf_json)
            print('\n')
            print('Basic: ')
            print(basic_json)
            print('Places:')
            print(places_json)
            print('Long Sleep')
            print(e)
            print('user_id: ' + u)
            sleep(random.randint(3000, 27000) / 10)

            continue
        count += 1
        write_file(dic)













