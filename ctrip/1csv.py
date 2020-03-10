#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:07:56 2020

@author: jia
"""

import pandas as pd
import os
#input data and change to string

data=pd.read_csv('./200216_102752/reviews/1.csv')



path = './200216_102752/reviews'
for i in range(2,519):
    try:
        data=data.append(pd.read_csv(path+'/{}.csv'.format(i)))
    except:
        print(str(i)+' not exist')
        continue
    
data['REVIEW_INDEX']=list(range(data.shape[0]))

data.to_csv('./merged_csv.csv', index=False)