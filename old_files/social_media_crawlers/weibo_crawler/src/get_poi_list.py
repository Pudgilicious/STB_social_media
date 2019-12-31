import pandas as pd
import json
import urllib3
import csv

# url = 'https://m.weibo.cn/api/container/getIndex?title=%E5%95%86%E5%9C%88&containerid=1001018006500000000000000_-_poilist&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%96%B0%E5%8A%A0%E5%9D%A1&page=1'

url_first_part = 'https://m.weibo.cn/api/container/getIndex?title=%E5%95%86%E5%9C%88&containerid=1001018006500000000000000_-_poilist&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%96%B0%E5%8A%A0%E5%9D%A1&page='
dic = {}

dic_keys = ['card_type', 'card_type_name', 'card_id', 'title', 'scheme', 'display_arrow', 'pic', 'title_sub', 'desc1', 'desc2', 'card_display_type', 'buttons', 'right_pannel', 'itemid']

for key in dic_keys:
    dic[key] = list()

http = urllib3.PoolManager()


def renew_dic(dic):
    for key in dic_keys:
        dic[key] = list()


def write_first(dic):
    df = pd.DataFrame(dic)
    df.to_csv('./data/poi_list.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)


def write_file(dic):
    old_df = pd.read_csv('./data/poi_list.csv')
    new_df = pd.DataFrame(dic)
    df = pd.concat([old_df, new_df], ignore_index=True, sort=False)
    df.to_csv('./data/poi_list.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL, index=False)


for i in range(0, 100):
    i = i + 1
    url = url_first_part + str(i)
    result = http.request('GET', url)
    json_reslut = json.loads(result.data)
    print('Page ' + str(i) +': '+ str(json_reslut['ok']))
    data_set = json_reslut['data']['cards'][0]['card_group']
    for poi in data_set:
        print(poi['title_sub'])
        for key in data_set[0].keys():
            dic[key].append(poi[key])

    # write_first(dic)
    write_file(dic)
    renew_dic(dic)
    print('Page: ' + str(i) + ' finished.')
