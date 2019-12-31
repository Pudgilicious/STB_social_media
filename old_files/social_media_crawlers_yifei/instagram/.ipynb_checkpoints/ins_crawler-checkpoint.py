import pandas as pd
import csv
from time import sleep
from datetime import datetime
import urllib3
import json
from urllib.parse import quote

### INSERTION ###
import re
import mysql.connector
#################

keys1 = ['id', 'name', 'has_public_page', 'lat', 'lng', 'slug', 'blurb', 'website', 'phone','primary_alias_on_fb',
            'address_json', 'profile_pic_url']

keys2 = ['ins_id', 'comments_disabled', 'text', 'liked_by', 'owner', 'is_video', 'video_view_count', 'comment_count']
# Add end_cursor
keys3 = ['crawled_time', 'posted_time', 'media_link']

# 50 is the parameter on the number of posts
def construct_url(pk, count, end):
    url_part1 = 'https://www.instagram.com/graphql/query/?query_hash=1b84447a4d8b6d6d0426fefb34514485&variables='
    url_part2 = quote('{"id":' + '"' + str(pk) + '"' + ',"first":50}')
    # if count == 0:
    #     url_part2 = quote('{"id":' + '"' + str(pk) + '"' + ',"first":50}')
    # else:
    #     url_part2 = quote('{"id":' + '"' + str(pk) + '"' + ',"first":50, after:' + str(end) + '}')

    url = url_part1 + url_part2

    return url


def extract_data(dic, json_data):
    
### INSERTION ###
    try:
        cnx = mysql.connector.connect(host="localhost", 
                                      database="sentimentDB", 
                                      user="test_user", 
                                      password="Password123!")
        cnx.cursor().execute('SET NAMES utf8mb4')
    
    except mysql.connector.Error as err:
        print(err)
#################
            
    # Basic data about the location
    for key in keys1:
        dic[key].append(json_data['data']['location'][key])
    # Page info
    # dic['end_cursor'] = json_data['data']['location']['edge_location_to_media']['page_info']['end_cursor']
    # Ins data
    for ins in json_data['data']['location']['edge_location_to_media']['edges']:

        for key in keys1:
            dic[key].append(dic[key][0])

        dic['crawled_time'].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        dic['ins_id'].append(ins['node']['id'])
        dic['comments_disabled'].append(ins['node']['comments_disabled'])
        try:
            dic['text'].append(ins['node']['edge_media_to_caption']['edges'][0]['node']['text'])
        except IndexError:
            dic['text'].append('None')
        dic['comment_count'].append(ins['node']['edge_media_to_comment']['count'])
        dic['liked_by'].append(ins['node']['edge_liked_by']['count'])
        dic['owner'].append(ins['node']['owner']['id'])
        dic['is_video'].append(ins['node']['is_video'])
        if ins['node']['is_video']:
            dic['video_view_count'].append(ins['node']['video_view_count'])
        else:
            dic['video_view_count'].append(0)
        timestap =  datetime.fromtimestamp(ins['node']['taken_at_timestamp'])
        dic['posted_time'].append(timestap.strftime("%Y-%m-%d %H:%M:%S"))
        dic['media_link'].append(ins['node']['display_url'])

### INSERTION ###
        text_db = re.sub(r'"', r'\"', dic['text'][-1])
        
        cnx.cursor().execute(
            """
            INSERT INTO instagrams (
                number_id,
                user_id,
                keyword,
                posted_time,
                caption
                )
            VALUES ({}, {}, {}, {}, {});
            """.format(
                '"' + dic['ins_id'][-1] + '"',
                '"' + dic['owner'][-1] + '"',
                '"' + dic['name'][-1] + '"',
                '"' + dic['posted_time'][-1] + '"',
                '"' + text_db + '"'
                )
        )
        
        cnx.commit()
    
    cnx.close()
#################
    
    for key in keys1:
        dic[key].pop(-1)


def write_data(dic, path):
    df0 = pd.read_csv(path, index_col=[0])
    df = pd.DataFrame(dic)
    df = df.append(df0, ignore_index=True)
    df.to_csv(path, encoding='utf_8_sig', quoting=csv.QUOTE_ALL)


def construct_dic(keys1, keys2, keys3):
    keys1 = keys1
    keys2 = keys2
    keys3 = keys3
    dic = dict.fromkeys(keys1 + keys2 + keys3)
    return dic

urllib3.disable_warnings()
file = pd.read_csv('./instagram/cleaned_poi.csv')

pk_list = list(file['pk'])
name_list = list(file['poi_name'])
http = urllib3.PoolManager()

for index, pk in enumerate(pk_list):
    print(name_list[index], round(index/len(pk_list), 3))

    dic = construct_dic(keys1, keys2, keys3)
    for i in dic:
        dic[i] = list()
    end = 0 
    url = construct_url(pk, index, end)
    response = http.request('GET', url)
    if response.status == 200:
        json_result = json.loads(response.data)
        try:
            extract_data(dic, json_result)
        except TypeError as e:
            print('##### EXCEPTION #####\n' + e + '\n#####################')
            with open('exception', 'w') as outfile:
                outfile.write(str(pk)+'\n')
                sleep(300)
        write_data(dic, './instagram/ins_data.csv')
    else:
        with open('exception', 'w') as outfile:
            outfile.write(str(pk) + '\n')
