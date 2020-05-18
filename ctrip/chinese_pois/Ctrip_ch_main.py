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
from Ctrip_ch_fsm import Ctrip_FSM




with open('chinese_pois_config.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']
csv_input_path = configs['Ctrip']['csv_input_path']

db_in_flag = configs['Ctrip']['read_from_database']
db_out_flag = configs['Ctrip']['write_to_database']


if db_in_flag == 'csv':
    
   df = pd.read_csv(csv_input_path)
    
  
   poi_df = pd.DataFrame({'poi_index':df['POI_INDEX'], 
                          'poi_name':df['POI_NAME'], 
                          'city_name':df['CITY_NAME'],
                          'poi_url':df['URL']
                          })
   

    
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
    proxy_mode=configs['Ctrip']['proxy_mode']
    timeout=configs['Ctrip']['timeout']
    authen_count=configs['Ctrip']['authen_count']
    earliest_date=configs['Ctrip']['earliest_date']
    #start_page=configs['QY']['start_page']
    fsm.start(proxy_mode,timeout,authen_count,earliest_date)
    end_time = time.time()
    print('Total time taken (min): ' + str(round((end_time - start_time)/60, 2)))
