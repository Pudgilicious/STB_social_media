from selenium import webdriver
from scrapy import Selector
from scrapy.http import HtmlResponse
import pandas as pd
import csv
import re
from time import sleep
from datetime import date

driver = webdriver.Chrome('./chromedriver')

url = "https://www.tripadvisor.com.sg/Attractions-g294265-Activities-a_allAttractions.true-Singapore.html"
#url = "https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html#EATERY_OVERVIEW_BOX"

driver.get(url)

# Initialize pandas data-frame with name of place and link
poi_df = pd.DataFrame(columns=['POI', 'link', 'num_reviews'])

# There are 28 pages of attractions in Tripadvisor.
for i in range(28):
    
    print("page" + str(i)) #counter to keep track at which page    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #To scroll down
    
    #Forming selector path
    sleep(1) 
    sel = Selector(text=driver.page_source)
    sleep(1)
      
    res = sel.xpath('//div[@id="FILTERED_LIST"]')    
    end_link = '/div/div/div/div[1]/div/div[1]/div[3]/a[@target="_blank"]/@href'     #Alternative: end_link = '/div/div/div/div[2]/a[@target="_blank"]/@href'
    end_text = '/div/div/div/div[1]/div/div[1]/div[3]/a[@target="_blank"]/text()'
    end_reviews = '/div/div/div/div[1]/div/div[1]/div[4]/div[2]/div/span[2]/a[@target="_blank"]/text()'
    
    #Looping through the div nodes
    for i in range(1, 100):
        
        #Forming a string
        xpath_link = 'div[' + str(i) +']' + end_link   
        xpath_text = 'div[' + str(i) +']' + end_text
        xpath_reviews = 'div[' + str(i) +']' + end_reviews
        
        link = res.xpath(xpath_link).extract_first()     #eg. link = res.xpath('div[1]/div/div/div/div[2]/a[@target="_blank"]/@href').extract_first()       
        text = res.xpath(xpath_text).extract_first()  
        reviews = res.xpath(xpath_reviews).extract_first() 
    
        try:
            if link:     #If link exist   
                poi_df.loc[poi_df.shape[0]] = [text] + [link] + [reviews]
                   
        except:
            print("can't write")
    
    try:
        next_page_button = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
    except:
        sleep(1)
        next_page_button = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
    
    try:
        next_page_button.click()    
    except:
        print("Can't click or last page")
        
driver.quit()

#Write out as data-frame
today = date.today()
today_date = today.strftime("%Y%m%d")
poi_df.to_csv("./experimentation/jiaxin_experiment/" + today_date + "_attractions_list.csv", encoding='utf-8', index = False)

#Full path examples
#ATTR_ENTRY_2149128 > div > div > div > div.tracking_attraction_photo.photo_booking.non_generic > a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]        #filtered list
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]  #next node 
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[2]/a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[5]
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[3]
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[2]/a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[1]/div/div[1]/div[3]/a
#/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div/div/div[1]/div/div[1]/div[4]/div[2]/div/span[2]/a