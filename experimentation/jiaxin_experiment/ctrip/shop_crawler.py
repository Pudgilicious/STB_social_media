#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:23:19 2020

@author: jia
"""

import pandas as pd
from scrapy import Selector
import os
import re
import utils
from time import sleep
import traceback
from random import random
from selenium import webdriver
from datetime import datetime, date, timedelta
from random import random

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import base64
from PIL import Image
from aip import AipOcr

#for authentication


class ShoppingCrawler:
    attributes_col_names = ['POI_INDEX',
                       'ENGLISH_NAME'
                           ]


    
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.chromedriver_path = chromedriver_path
        self.driver = None
        self.poi_df = poi_df
        if cnx:
            self.cursor = cnx.cursor()
        self.db_out_flag = db_out_flag 
        #for FMS
        self.fsm_state=0

        #update after each POI is crawled
        self.current_page = None
        self.current_poi_index = None
        self.current_poi_url =None
        self.review_final_page = False
        self.attributes_crawled=False
        self.sel = None                                
        self.current_url=None
        self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
        
       
        #for authentication test
        self.count=1
        self. unlock= unlockScrapy(object)
        # Create unique CSVs.
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        os.makedirs('./output/{}/'.format(self.datetime_string))
        self.attributes_df.to_csv('./output/{}/attributes.csv'.format(self.datetime_string),mode='a', index=False)

                
    
    def add_to_database(self):
        # Read csv, add to database, then cnx.commit().
        return
    
    
    def crawl_shops(self, number_of_pages=None):
        if self.fsm_state == 0:
            if number_of_pages is not None:
                self.number_of_pages = number_of_pages
            #initialization finish, change state
            self.fsm_state = 1
            
        self.driver = webdriver.Chrome(self.chromedriver_path)  

        while len(self.poi_df.index) > 0:
            
    
            # Create <POI_INDEX>.csv in reviews and reviewers folders.
            if self.fsm_state == 1:
                self.current_poi_index = self.poi_df.iloc[0][0]
                self.current_poi_name = self.poi_df.iloc[0][1]
                self.current_poi_url = self.poi_df.iloc[0][2]
                
            self.driver.get(self.current_poi_url)
            if self.fsm_state == 3: 
                self.fsm_state=2
            sleep(1+random()*2)
            self.sel = Selector(text=self.driver.page_source)               
    #################handle error of authentication########################################
            res=self.sel.xpath('/html/body/div[3]/div[3]/img')
            if res != []:
                self.count+=1
                if self.count == 3:
                    log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                    log_file.write('{}, {}, {}, {}\n'.format(self.current_poi_index,
                                                           self.current_poi_name,
                                                           datetime.now(),
                                                           'Caught by Ctrip, go authentication test'))
                    log_file.close()
                    self.count = 1
                    unlock()
                
                continue
    ####################################################################################################
    
            if self.fsm_state != 3:
                if self.fsm_state == 2:
                    # Note change in FSM state
                    self.fsm_state = 1   
                    
                try:
            #################handle error of redirecting########################################
                    self. current_url= self.driver.current_url
                    if self.current_url == 'https://you.ctrip.com/':
                        log_file = open('./output/{}/log.txt'.format(self.datetime_string), 'a+')
                        log_file.write('{}, {}, {}, {}\n'.format(self.current_poi_index,
                                                               self.current_poi_name,
                                                               datetime.now(),
                                                               'current POI does not exist'))
                        log_file.close()
                        raise Exception("current POI does not exist")
                        self.poi_df = self.poi_df.iloc[1:]
                        continue
            ####################################################################################################
                    if not self.attributes_crawled:    
                            print('########## {}##########'.format(self.current_poi_name))
                            self.crawl_attributes()
                            self.attributes_df.to_csv('./output/{}/attributes.csv'.format(self.datetime_string),
                                                      mode='a', 
                                                      header=False,
                                                      index=False)
                            self.attributes_df = pd.DataFrame(
                                columns=self.attributes_col_names)
                            self.attributes_crawled = True  
                   

                    self.attributes_crawled = False
                    
                    self.poi_df = self.poi_df.iloc[1:]
        
                        
                   
                except:
                    self.fsm_state=3
                    self.driver.quit()
                    self.current_page = None
                    log_file = open('./output/{}/log.txt'
                                    .format(self.datetime_string), 'a+')
                    log_file.write('{}, {}, page: {}, {}\n'\
                               .format(self.current_poi_index,
                                       self.current_poi_name,
                                       self.current_page,
                                       datetime.now()))
                    log_file.write(traceback.format_exc() + '\n')
                    log_file.close()
                    #erase every thing from the POI review csv, rewrite in next loop
                   #erase every thing from the POI review csv, rewrite in next loop
                    #if self.reviews_crawled==True:
                     #   os.remove('./output/{}/reviews/{}.csv'
                      #                     .format(self.datetime_string,
                       #                            self.current_poi_index)) 
                    print("Exception has occurred. Please check log file.")
                    self.reviews_crawled=False
                    sleep(1)
                    return
            
                
                
            
        self.driver.quit()
        self.fsm_state = 4
 
    def crawl_attributes(self):
        poi_index=self.current_poi_index
        #select areas where we going to extract info
        res = self.sel.xpath('.//div[@class="dest_toptitle detail_tt"]')
       
        xpath_eng='//div[@class="f_left"]/p/text()'
        eng_name=res.xpath(xpath_eng).extract_first()
        
        poi_attributes = [poi_index,
                          eng_name]
        
        poi_attributes_dict = dict(zip(self.attributes_col_names, poi_attributes))
        self.attributes_df = self.attributes_df.append(poi_attributes_dict, ignore_index=True)
        sleep(random()*2)
   
    # Methods below are all utility functions.
''' def parse_total_reviews1(self, text):
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0
    
    def parse_attribute_address(self, text):
        return (text[3:]).replace(' ','')
    
    def parse_review_date1(self, text):
        return datetime.strptime(text[0:10],"%Y-%m-%d").date()
        
    def parse_review_time1(self, text):
        return format(datetime.strptime(text[11:16],"%H:%M"),"%H:%M")
    
    def parse_review_rating1(self, text):
        return int(text)
    
    def parse_review_rating2 (self, text):
        return int(text[6:text.find('%')])/20
    
    def parse_review_body1(self, text):
        return text.replace('\n','')'''

# 破解携程反爬验证
class unlockScrapy(object):
 
    def __init__(self, driver):
        super(unlockScrapy, self).__init__()
        # selenium驱动
        self.driver = driver
        self.WAPPID = '18383870'                                               #'百度文字识别appid'
        self.WAPPKEY = 'U9A5vH5d7ITt3T5VE08Fooib'                              #'百度文字识别appkey'
        self.WSECRETKEY ='r1QkcgOYWMNMrXOj35x1ZV2XKaxAV6nR'                    #'百度文字识别secretkey'
        # 百度文字识别sdk客户端
        self.WCLIENT = AipOcr(self.WAPPID, self.WAPPKEY, self.WSECRETKEY)
 
    # 按顺序点击图片中的文字
    def clickWords(self, wordsPosInfo):
        # 获取到大图的element
        imgElement = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/img")
        # 根据上图文字在下图中的顺序依次点击下图中的文字
        for info in wordsPosInfo:
            ActionChains(self.driver).move_to_element_with_offset(
                to_element=imgElement, xoffset=info['location']['left'] + 20,
                yoffset=info['location']['top'] + 20).click().perform()
            time.sleep(1)
 
    # 下载上面的小图和下面的大图
    def downloadImg(self):
        # 小图的src
        codeSrc = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[1]/img").get_attribute("src")
        # 大图的src
        checkSrc = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/img").get_attribute("src")
        # 保存下载
        fh = open("code.jpeg", "wb")
        # 由于其src是base64编码的，因此需要以base64编码形式写入
        fh.write(base64.b64decode(codeSrc.split(',')[1]))
        fh.close()
        fh = open("checkCode.jpeg", "wb")
        fh.write(base64.b64decode(checkSrc.split(',')[1]))
        fh.close()
 
    # 图片二值化，便于识别其中的文字
    def chageImgLight(self):
        im = Image.open("code.jpeg")
        im1 = im.point(lambda p: p * 4)
        im1.save("code.jpeg")
        im = Image.open("checkCode.jpeg")
        im1 = im.point(lambda p: p * 4)
        im1.save("checkCode.jpeg")
 
    # 破解滑动
    def unlockScroll(self):
        # 滑块element
        elm = self.driver.find_element_by_xpath('.//div[@iclass="cpt-drop-btn"]')
        self. driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", 
                      elm,  
                      "unselectable",
                      "off")
        scrollElement = self.driver.find_elements_by_xpath('.//div[@iclass="cpt-drop-btn"]')[0]
        ActionChains(self.driver).click_and_hold(
            on_element=scrollElement).perform()
        ActionChains(self.driver).move_to_element_with_offset(
            to_element=scrollElement, xoffset=30, yoffset=10).perform()
        ActionChains(self.driver).move_to_element_with_offset(
            to_element=scrollElement, xoffset=100, yoffset=20).perform()
        ActionChains(self.driver).move_to_element_with_offset(
            to_element=scrollElement, xoffset=200, yoffset=50).perform()
 
    # 读取图片文件
    def getFile(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
 
    # 识别上面小图中的文字
    def iTow(self):
        try:
            op = {'language_type': 'CHN_ENG', 'detect_direction': 'true'}
            res = self.WCLIENT.basicAccurate(
                self.getFile('code.jpeg'), options=op)
            words = ''
            for item in res['words_result']:
                if item['words'].endswith('。'):
                    words = words + item['words'] + '\r\n'
                else:
                    words = words + item['words']
            return words
        except:
            return 'error'
 
    # 识别下面大图中文字的坐标
    def getPos(self, words):
        try:
            op = {'language_type': 'CHN_ENG', 'recognize_granularity': 'small'}
            res = self.WCLIENT.accurate(
                self.getFile('checkCode.jpeg'), options=op)
            # 所有文字的位置信息
            allPosInfo = []
            # 需要的文字的位置信息
            needPosInfo = []
            for item in res['words_result']:
                allPosInfo.extend(item['chars'])
            # 筛选出需要的文字的位置信息
            for word in words:
                for item in allPosInfo:
                    if word == item['char']:
                        needPosInfo.append(item)
            return needPosInfo
        except Exception as e:
            print(e)
 
    def main(self):
        # 破解滑块
        self.unlockScroll()
        time.sleep(2)
        # 下载图片
        self.downloadImg()
        time.sleep(2)
        # 图像二值化，方便识别
        self.chageImgLight()
        # 识别小图文字
        text = self.iTow()
        # 获取大图的文字位置信息
        posInfo = self.getPos(list(text))
        # 由于小图或大图文字识别可能不准确，因此这里设置识别出的文字少于4个则重新识别
        while len(posInfo) != 4 or len(text) != 4:
            # 点击重新获取图片，再次识别
            self.driver.find_elements_by_xpath(
                '/html/body/div[3]/div[4]/div/a')[0].click()
            time.sleep(2)
            self.downloadImg()
            time.sleep(2)
            text = self.iTow()
            posInfo = self.getPos(list(text))
        time.sleep(3)
        print('匹配成功，开始点击')
        # 点击下面大图中的文字
        self.clickWords(posInfo)
        # 点击提交按钮
        self.driver.find_elements_by_xpath(
            '/html/body/div[3]/div[4]/a')[0].click()
        time.sleep(2)
        # 如果破解成功，html的title会变
        if self.driver.title != '携程在手，说走就走':
            print('破解成功')
        else:
            # 再次尝试
            print('破解失败，再次破解')
            self.main()
 
 
def unlock():
    driver = webdriver.Chrome('./chromedriver')
    # 打开Chrome浏览器，需要将Chrome的驱动放在当前文件夹
    driver.get(
        'https://hotels.ctrip.com/hotel/6278770.html#ctm_ref=hod_hp_hot_dl_n_2_7')
    # 开始破解
    unlock = unlockScrapy(driver)
    unlock.main()
 
if __name__ == '__main__':
    unlock()



