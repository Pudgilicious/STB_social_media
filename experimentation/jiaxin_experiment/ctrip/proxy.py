#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:06:48 2020

@author: jia
"""
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy   
#######################################importing proxy list####################################    

def working_proxies(countries_list=None):
    req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
    proxies = req_proxy.get_proxy_list() #this will create proxy list
    
    
    ##################################preparation of proxy list###############################
    proxies_address=list(map(lambda x: x.get_address(), proxies))
    proxies_countries=list(map(lambda x: str(x.country), proxies))
    
    
    df = pd.DataFrame({'countries': proxies_countries, 
                         'IP': proxies_address })
    
    #obtain the asia countries want to keep
    #countries=Counter(proxies_countries)
    #for key, value in countries.items():
     #   print(key, value)    
    
    if countries_list is None: 
        countries_list =[#'Indonesia'                                                             # total 23, 8/20
               #'Cambodia'                                                             # total 8, 3/8
               #'India'                                                                # total 23, 7/20
               'Hong Kong',                                                            # total 10, 6/10        chosen
               'Thailand',                                                             # total 26, 10/20       chosen
               #'Nepal'                                                                # total 11,  3/11
               #'Myanmar',                                                              # total 4, 2/4
               #'Bangladesh'                                                           # total 12, 2/12
               #'Philippines'                                                          # total 3, 1/3
               #'Singapore'                                                            # total 7, 2/7
               #'Mongolia'                                                             # total 4, 0/4
               'Vietnam',                                                              # total 11, 6/11        chosen
               'Pakistan',                                                             # total 14, 7/14        chosen
               #'Japan'                                                                # total 11, 1/11
               #'Korea'                                                                # total  1, 0/1
               #'China'                                                                # total 7, 0/7
               'Macau'                                                                # total 3, 3/3           chosen
               ]                                                              
        
    #delete unwanted IP addresses
    df= df[df['countries'].isin(countries_list)]
    
    return df
 
    #print out non-exsiting countries, remove from existng list, notify the non-existance


