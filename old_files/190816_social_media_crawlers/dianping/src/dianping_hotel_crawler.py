import json
import time
import pandas as pd
import csv
import urllib3
from time import sleep


url1 = 'http://ohwebapi.meituan.com/oh/listinfo?cityId=2311&cityNameEn=singapore&checkinDate='
ctime = time.strftime("%Y-%m-%d")
limit = 100  # The number of hotels obtained every request
offset = 0   # Increase by 100 each loop


http = urllib3.PoolManager()

for i in range(0, 8):
    print(i)
    data = {
        'Chinese_name': [],
        'image_list': [],
        'poi_recommend_tag': [],
        'English_name': [],
        'score_intro': [],
        'score_description': [],
        'pos_descr': [],
        'sale_tags': [],
        'lowest_price': [],
        'history_sale_count_number': [],
        'area_name': [],
        'coordinates': [],
        'avg_score': [],
        'review_number': [],
    }
    url2 = ctime + '&checkoutDate=' + ctime + '&limit=' + str(limit) + '&offset=' + str(offset) + '&sort=smart'
    offset = offset + limit
    url = url1 + url2

    response = http.request('GET', url)
    sleep(2)
    res = json.loads(response.data)    #For reading json data

    for j in range(len(res['data']['searchResult'])):
        data['Chinese_name'].append(res.get("data").get("searchResult")[j].get('name'))
        data['image_list'].append(res.get("data").get("searchResult")[j].get('imageList'))
        data['poi_recommend_tag'].append(res.get("data").get("searchResult")[j].get('poiRecommendTag'))
        data['English_name'].append(res.get("data").get("searchResult")[j].get('nameEn'))
        data['score_intro'].append(res.get("data").get("searchResult")[j].get('scoreIntro'))
        data['score_description'].append(res.get("data").get("searchResult")[j].get('scoreDescription'))
        data['pos_descr'].append(res.get("data").get("searchResult")[j].get('posDescr'))
        st = ''
        slist = res.get("data").get("searchResult")[j].get('saleTags')
        for t in slist:
            st += t
        data['sale_tags'].append(st)
        data['lowest_price'].append(res.get("data").get("searchResult")[j].get('lowestPrice'))
        data['history_sale_count_number'].append(res.get("data").get("searchResult")[j].get('historySaleCountNumber'))
        data['area_name'].append(res.get("data").get("searchResult")[j].get('areaName'))
        data['coordinates'].append((
        res.get("data").get("searchResult")[i].get('lat'), res.get("data").get("searchResult")[j].get('lng')))
        data['avg_score'].append(res.get("data").get("searchResult")[j].get('avgScore'))
        data['review_number'].append( res.get("data").get("searchResult")[j].get('markNumbers'))

    df = pd.DataFrame(data)
    if i == 0:
        df.to_csv('../data/dianping_hotel.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
    else:
        old_df = pd.read_csv('../data/dianping_hotel.csv', index_col=[0])
        new_df = pd.concat([old_df, df], ignore_index=True, sort=False)
        new_df.to_csv('../data/dianping_hotel.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)

