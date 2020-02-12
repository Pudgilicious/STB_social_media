#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:19:02 2020

@author: jia
"""


import pandas as pd
import os
import os.path

os.chdir("/home/jia/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment")
#pd.read_excel('../')
print(os.path.dirname(__file__))
f = pd.read_excel(os.path.dirname(__file__) + '/experimentation/jiaxin_experiment/STB.xls')