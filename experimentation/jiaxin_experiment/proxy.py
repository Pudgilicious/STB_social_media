#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:06:48 2020

@author: jia
"""
import numpy as np

from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list

from selenium import webdriver

proxies_countries=list(map(lambda x: x.country, proxies))


           

'''PROXY = ind[7].get_address()

webdriver.DesiredCapabilities.CHROME['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    
    "proxyType":"MANUAL",
    
}
ind1=list(map(lambda x:x.get_address(),ind))

driver = webdriver.Chrome('./chromedriver')

driver.get('https://you.ctrip.com/sight/singapore53/147110.html')

a = [ind[1].get_address(), ind[2].get_address()]
b = proxy_check_simple(a)
c = proxy_check_simple(ind1)'''

def proxy_check_simple(proxies):
    import requests
    from requests.exceptions import ConnectionError, ProxyError
    good_proxies = []
    proxy_list = []
    def check(proxy):
        try:
            response = requests.get("https://ipapi.co/json/", proxies = proxy, timeout = 10)
            good_proxies.append(proxy)
            print(str(proxy) + " is good.")
        except ProxyError:
            print(str(proxy) + " is not responding.")
        except ConnectionError:
            print(str(proxy) + " connection denied.")
        except:
            print(str(proxy) + " exceeded timeout or other errors.")
    count = 0
    for proxy in proxies:
        check(proxy)
        count += 1
        print(str(count) + '/' + str(len(proxies)) + ' tested.')
        if len(good_proxies) == 20:
            break
        # if count == 11:
        #     break
    return good_proxies


try:
    urllib.urlopen(
        "http://example.com",
        proxies={'http':'http://example.com:8080'}
    )
except IOError:
    print "Connection error! (Check proxy)"
else:
    print "All was fine"