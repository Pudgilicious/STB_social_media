from selenium import webdriver
from scrapy import Selector
import pandas as pd
import csv
from time import sleep

driver = webdriver.Chrome('./chromedriver')

#url = 'https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html'
url = 'https://www.tripadvisor.com.sg/RestaurantSearch-g294265-oa9000-Singapore.html#EATERY_OVERVIEW_BOX'

driver.get(url)

# There are 372 pages of restaurants in Tripadvisor.
for i in range(74):
#for i in range(372):
    print(i)     
#    if i == 0:
#         try:
#             driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#             driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#             sleep(2)
#             next_page_button = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
#             next_page_button.click()
#         except:
#             driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#             driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#             sleep(5)
#             next_page_button = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
#         next_page_button.click()
#         continue     

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # Extract data
    sleep(1) #2
    sel = Selector(text=driver.page_source)
    sleep(1)
    for res in sel.xpath('//div[@id="EATERY_SEARCH_RESULTS"]/div[@class="prw_rup prw_sponsoredListings_restaurants_tripads_slot0"]'):
        link = res.xpath('//div[@id="EATERY_SEARCH_RESULTS"]/div[@class="prw_rup prw_sponsoredListings_restaurants_tripads_slot0"]/div[@class="listing rebrand listingIndex-n"]/div[@class="ui_columns is-mobile"]/div/h3/a/@data-url').extract_first()
        link = link.replace('http://www.tripadvisor.com.sg', '')
        print(link)
        with open('trip_res_link.txt', mode='a') as f:
            f.write(link + "\n")   #f.write(link + "\n")

    for res in sel.xpath('//div[@data-index]'):
        link = res.xpath('div/div/div/a[@target="_blank"]/@href').extract_first()
        link = link.replace('http://www.tripadvisor.com.sg', '')
        print(link)
        with open('trip_res_link.txt', mode='a') as f:
            f.write(link + "\n")


    try:
        next_page_button = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
    except:
        sleep(1)
        next_page_button = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
    next_page_button.click()

driver.quit()
