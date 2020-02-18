#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:16:48 2020

@author: jia
"""

# coding=utf-8
from datetime import datetime
import sys
import json
import base64
import time
import pandas as pd
import os
os.chdir("/home/jia/Desktop/git/STB_social_media_analytics")
# make it work in both python2 both python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context






#for API    
API_KEY = 'ARe9sGfm23Tph0rDwr8htjkh'
SECRET_KEY = '6EToGoaPLmXHLOCvanY62Zm6T8dQofCR'
COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


class BaiduAPI:
                                              
    """
        get token
    """
    def fetch_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print(err)
        if (IS_PY3):
            result_str = result_str.decode()
    
    
        result = json.loads(result_str)
    
        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not 'brain_all_scope' in result['scope'].split(' '):
                print ('please ensure has check the  ability')
                exit()
            return result['access_token']
        else:
            print ('please overwrite the correct API_KEY and SECRET_KEY')
            exit()
    
    """
        call remote http server
    """
    def make_request(self, url, comment):
        #print("---------------------------------------------------")
        #print("评论文本：")
        #print("    " + comment)
        #print("\n评论观点：")
        response = self.request(url, json.dumps(
        {
           "text": comment,
            "type": 5     #5 is the corpora for tourism, other type please see:https://ai.baidu.com/docs#/NLP-Apply-API/09fc895f
        }))
    
        data = json.loads(response)
    
        if "error_code" not in data or data["error_code"] == 0:
            for item in data["items"]:
                # positive
                if item["sentiment"] == 2:
                    #print(u"    POS: " + item["prop"] + item["adj"])
                    self.sentiment = 'POS'
                    self.aspect = item["prop"]
                    self.adjective = item["adj"]
                # neutral
                if item["sentiment"] == 1:
                    #print(u"    NEU: " + item["prop"] + item["adj"])
                    self.sentiment = 'NEU'
                    self.aspect = item["prop"]
                    self.adjective = item["adj"]
                # negative
                if item["sentiment"] == 0:
                    #print(u"    NEG: " + item["prop"] + item["adj"])
                    self.sentiment = 'NEU'
                    self.aspect = item["prop"]
                    self.adjective = item["adj"]
                    
                    
                sentiment_detail=[self.current_index, self.sentiment, self.aspect,self.adjective]   
                sentiment_dict = dict(zip(self.sentiment_col, sentiment_detail))
                self.sentiment_df= self.sentiment_df.append(sentiment_dict, ignore_index=True)
                self.sentiment_df.drop_duplicates()
                
        else:
            # print error response
            print(response)
            
        # 防止qps超限
        time.sleep(0.5)
    
    """
        call remote http server
    """
    def request(self, url, data):
        req = Request(url, data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
            if (IS_PY3):
                result_str = result_str.decode()
            return result_str
        except  URLError as err:
            print(err)
    
    def sentiment(self):
        # get access token
        token = self.fetch_token()
    
        # concat url
        url = COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token
        
        #create csv file for the output
        self.sentiment_col=['review_index', 
                       'sentiment',
                       'aspect',
                       'adjective']
        self.sentiment_df = pd.DataFrame(columns=self.sentiment_col)
        datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        self.sentiment_df.to_csv('./experimentation/jiaxin_experiment/Baidu_API/BD_{}sentiment.csv'.format(datetime_string),index=False)    
        #input Alidata
        comment_list=pd.read_csv('./experimentation/jiaxin_experiment/Baidu_API/2.csv')
        review_index=list(range(len(comment_list['REVIEW_BODY'])))
        df=pd.DataFrame({'index': review_index,
                         'reviews':comment_list['REVIEW_BODY']
                         })
        
        while len(df.index) > 0:
            self.current_index = df.iloc[0][0]
            print(self.current_index)
            current_comment=df.iloc[0][1]
            self.make_request(url,current_comment)
            df=df.iloc[1:]
        

        self.sentiment_df.to_csv('./experimentation/jiaxin_experiment/Baidu_API/BD_{}sentiment.csv'.format(datetime_string),
                                                          mode='a', 
                                                          header=False,
                                                          index=False)
                
        



b=BaiduAPI()
b.sentiment()