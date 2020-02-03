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
import os
print(os.getcwd())


with open('config_file_Ctrip.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']
csv_input_path = configs['Ctrip']['csv_input_path']

db_in_flag = configs['Ctrip']['read_from_database']
db_out_flag = configs['Ctrip']['write_to_database']

if db_in_flag == 'csv':
    
    df = pd.read_csv(csv_input_path)
    
    def parse_reviews(text):
        if re.search(r'\d+',str(text)):
            return int(re.search(r'\d+', text).group())
        else:
            return 0

    df['num_reviews'] = df['num_reviews'].apply(parse_reviews)
    df['link'] = df['link'].apply(lambda x: "https://you.ctrip.com"+x)
    
    poi_index=list(range(len(df['POI'])))
    
    poi_df = pd.DataFrame({'poi_index':poi_index, 
                           'poi_name':df['POI'], 
                           'poi_url':df['link']}
                           )
    
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
    #start_page=configs['QY']['start_page']
    fsm.start(number_of_pages)
    end_time = time.time()
    print('Total time taken (min): ' + str(round((end_time - start_time)/60, 2)))