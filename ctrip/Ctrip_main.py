#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:12:16 2020

@author: jia
"""

import pandas as pd
import mysql.connector
import yaml
import re
import time
from Ctrip_fsm import Ctrip_FSM




with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']
csv_input_path = configs['Ctrip']['csv_input_path']

db_in_flag = configs['Ctrip']['read_from_database']
db_out_flag = configs['Ctrip']['write_to_database']


if db_in_flag == 'csv':
    
   df = pd.read_csv(csv_input_path)
    
   def parse_reviews(text):
        """

        @param text: a string contains the number of reviews for a POI, usually in the form 'xx条点评‘
        @return: intger form of the number of reviews
        """
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0
        
   #df['num_reviews'] = df['num_reviews'].apply(parse_reviews)                 #validation measures
   df['URL'] = df['URL'].apply(lambda x: "https://you.ctrip.com"+x)
    
   #poi_index=list(range(len(df['Poi'])))                                      #later change to read from file
    
   poi_df = pd.DataFrame({'poi_index':df['POI_INDEX'], 
                          'poi_name':df['POI_NAME'], 
                          'poi_url':df['URL'],
                          'is_prioritized':df['IS_PRIORITIZED']}
                           )
   
   prioritize=configs['Ctrip']['prioritize']
   if prioritize is True:
       poi_df=poi_df[poi_df['is_prioritized']==1]
    
   '''poi_index = [1,2]
   poi_name=['fountain of wealth',
              'Big Bus Singapore']
            
   poi_url=['https://you.ctrip.com/sight/singapore53/132965.html',
             'https://you.ctrip.com/sight/singapore53/2482004.html'] 
    
   poi_df = pd.DataFrame({'poi_index':poi_index,
                           'poi_name':poi_name,
                           'poi_url':poi_url},
                          )'''
    
if db_in_flag != 'csv':
    poi_df = pd.DataFrame()

if db_in_flag != 'csv' or db_out_flag != 'csv':
    cnx = mysql.connector.connect(host=configs['General']['host'],
                                  database=configs['General']['database'],
                                  user=configs['General']['user'],
                                  password=configs['General']['password']
                                 )
else:
    cnx = None
    
if __name__=="__main__":
    start_time = time.time()
    fsm = Ctrip_FSM(chromedriver_path, poi_df, cnx, db_out_flag)
    number_of_pages=configs['Ctrip']['number_of_pages']
    proxy_mode=configs['Ctrip']['proxy_mode']
    timeout=configs['Ctrip']['timeout']
    authen_count=configs['Ctrip']['authen_count']
    #start_page=configs['QY']['start_page']
    fsm.start(number_of_pages,proxy_mode,timeout,authen_count)
    end_time = time.time()
    print('Total time taken (min): ' + str(round((end_time - start_time)/60, 2)))
