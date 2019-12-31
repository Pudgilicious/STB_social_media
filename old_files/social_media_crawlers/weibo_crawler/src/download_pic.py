import urllib3
import pandas as pd
import re
import os

urllib3.disable_warnings()
pic_downloaded_list = []

for name in os.listdir('./output/pictures'):
    if name[0:-4] not in pic_downloaded_list:
        pic_downloaded_list.append(name[0:-4])


weibo_data = pd.read_csv('./output/cleaned_data.csv')

picture_urls = []

for urls in weibo_data['pictures']:
    if urls != 'No Picture':
        for url in urls.split(' '):
            if url != '':
                picture_urls.append(url)
    else:
        pass

temp = set(picture_urls)
picture_urls = list(temp)

http = urllib3.PoolManager()


def save_pictures(url, data):
    picture_id = re.findall('/\w+.jpg', url)
    if len(picture_id) == 0:
        picture_id = re.findall('/\w+.gif', url)
    else:
        pass
    with open('./output/pictures/' + picture_id[0][1:], 'wb') as outfile:
        outfile.write(data)


count = 0
picture_number = 0
for url in picture_urls:
    picture_id = re.findall('/\w+.jpg', url)
    if len(picture_id) == 0:
        picture_id = re.findall('/\w+.gif', url)
    if picture_id[0][1:-4] not in pic_downloaded_list:
        picture_number += 1

start_flag = False
for url in picture_urls:
    # if url == 'https://wx1.sinaimg.cn/large/694c8146ly1fhuax5ckdej20qo0zkk38.jpg':
    #     start_flag = True
    # if start_flag:
    picture_id = re.findall('/\w+.jpg', url)
    if len(picture_id) == 0:
        picture_id = re.findall('/\w+.gif', url)

    if picture_id[0][1:-4] not in pic_downloaded_list:
        response = http.request('GET', url)
        save_pictures(url, response.data)
        count += 1
        print(str(count) + '/' + str(picture_number) + ' pictures have been downloaded.')
    # if count == 1:
    #     break


