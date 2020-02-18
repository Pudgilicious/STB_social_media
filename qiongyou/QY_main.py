#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:15:53 2020

@author: jia
"""

import pandas as pd
import mysql.connector
import yaml
import re
import time
from QY_fsm import QY_FSM



with open('config_file_QY.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']
csv_input_path = configs['QY']['csv_input_path']

db_in_flag = configs['QY']['read_from_database']
db_out_flag = configs['QY']['write_to_database']

if db_in_flag == 'csv':
    
    df = pd.read_csv(csv_input_path)
    df['URL']=list(map(lambda x: 'https://'+ x[2:], df['URL']))
    
    poi_df = pd.DataFrame({'poi_index':df['POI_INDEX'], 
                           'poi_name':df['POI_RAW_NAME'], 
                           'poi_url':df['URL']}
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
    fsm = QY_FSM(chromedriver_path, poi_df, cnx, db_out_flag)
    number_of_pages=configs['QY']['number_of_pages']
    #start_page=configs['QY']['start_page']
    fsm.start(number_of_pages)
    end_time = time.time()
    print('Total time taken (min): ' + str(round((end_time - start_time)/60, 2)))