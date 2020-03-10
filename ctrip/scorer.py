#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 17:23:46 2020

@author: jia
"""

import sys
sys.path.append('./common_class_functions')

import yaml
from ibm_sentiment_scorer_fsm import IBMSentimentScorerFSM


with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

# Amend the corresponding variables in config_file.yml to continue from previous API calls.
target_folder = configs['Ctrip']['target_folder']
continue_in_folder = configs['Ctrip']['continue_in_folder']
continue_from_poi_index = configs['Ctrip']['continue_from_poi_index']
continue_from_row_index = configs['Ctrip']['continue_from_row_index']
API_options = configs['Ctrip']['API_options']
# Initialize FSM object
fsm = IBMSentimentScorerFSM(
    website_name='ctrip',
    website_id=2,
    target_folder=target_folder,
    continue_in_folder=continue_in_folder,
    continue_from_poi_index=continue_from_poi_index,
    continue_from_row_index=continue_from_row_index,
    API_options=API_options
)

# Start API calls
fsm.start()