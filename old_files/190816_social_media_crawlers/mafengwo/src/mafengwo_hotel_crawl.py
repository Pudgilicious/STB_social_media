from selenium import webdriver
from scrapy import Selector
from random import randint
import csv
import pandas as pd
from time import sleep



url = 'http://www.mafengwo.cn/hotel/10754/?sFrom=mdd'
driver = webdriver.Chrome('../chromedriver')
book_dict = {
    'http://images.mafengwo.net/images/hotel/newlogo/mafengwo_2018@2x.png': 'mafengwo',
    'http://images.mafengwo.net/images/hotel/ota/hotels_w100h20_2x_2.png': 'Hotels.com',
    'http://images.mafengwo.net/images/hotel/ota/agoda_w100h20_2x_2.png': 'agoda',
    'http://images.mafengwo.net/images/hotel/ota/booking_w100h20_2x_2.png': 'Booking.com',
    'http://images.mafengwo.net/images/hotel/ota/ctrip_w100h20_2x_2.png': '携程',
    'http://images.mafengwo.net/images/hotel/ota/youyu_w100h20_2x.png': '有鱼订房'
}

driver.get(url)
driver.maximize_window()
sleep(30)
jump_url = 'http://www.mafengwo.cn/hotel/10754/?sFrom=mdd#avl=0&distance=10000&price=-&feature=0&fav=0&sort=comment-DESC&page='
for i in range(24):  #24 pages
    # if i < 15:
    #     continue
    # elif i == 15:
    #     jump_url += str(i+1)
    #     driver.get(jump_url)
    #     driver.maximize_window()
    #     sleep(30)

    data = {
        'Chinese_name': [],
        'English_name': [],
        'scores': [],
        'review_number': [],
        'location_area': [],
        'booking_website': [],
        'booking_price(lowest)': [],
        'coordinates': []
    }
    sleep(2)
    sel = Selector(text=driver.page_source)

    for hotel in sel.xpath('//div[@id="_j_hotel_list"]/div[@class="hotel-item clearfix _j_hotel_item"]'):   #List of hotels in that page
        chinese_name = hotel.xpath('@data-name').extract_first()
        if not chinese_name:
            chinese_name = 'NULL'
        data['Chinese_name'].append(chinese_name)
        print(i, chinese_name)
        lat = hotel.xpath('@data-lat').extract_first()
        lng = hotel.xpath('@data-lng').extract_first()
        if not lat:
            lat = 'NULL'
            lng = 'NULL'
        data['coordinates'].append((lat, lng))
        english_name = hotel.xpath('div[@class="hotel-title"]/div[@class="title"]/span/text()').extract_first()
        if not english_name:
            english_name = 'NULL'
        data['English_name'].append(english_name)
        score = hotel.xpath('div[@class="hotel-info "]/ul[@class="nums clearfix"]/li/em/text()').extract_first()
        if not score:
            score = 'NULL'
        data['scores'].append(score)
        review_number = hotel.xpath('div[@class="hotel-info "]/ul[@class="nums clearfix"]/li/a/em/text()').extract_first()
        if not review_number:
            review_number = 'NULL'
        data['review_number'].append(review_number)
        location = hotel.xpath('div[@class="hotel-info "]/div[@class="location"]/span/a/text()').extract_first()
        if not location:
            location = 'NULL'
        data['location_area'].append(location)
        booking_list = hotel.xpath('div[@class="hotel-btns"]/a')
        booking_websites = ''
        booking_price = ''
        for item in booking_list:
            price = item.xpath('div[@class="price _j_booking_price"]/strong/text()').extract()[1]
            if not price:
                price = 'NULL'
            booking_price += price + '\n'
            title = item.xpath('div[@class="ota"]/div[@class="name"]/strong/text()').extract_first()
            if not title:
                picture_url = item.xpath('div[@class="ota"]/div[@class="name"]/strong/img/@src').extract_first()
                title = book_dict[picture_url]
            booking_websites += title + '\n'
        data['booking_website'].append(booking_websites)
        data['booking_price(lowest)'].append(booking_price)

    df = pd.DataFrame(data)
    if i == 0:
        df.to_csv('../data/mafengwo_hotel.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)
    else:
        old_df = pd.read_csv('../data/mafengwo_hotel.csv', index_col=[0])
        new_df = pd.concat([old_df, df], ignore_index=True, sort=False)
        new_df.to_csv('../data/mafengwo_hotel.csv', encoding='utf_8_sig', quoting=csv.QUOTE_ALL)

    if i == 23:
        print('Finished.')
        break

    try:
        next_page_button = driver.find_element_by_link_text('后一页')
    except:
        sleep(4)
        next_page_button = driver.find_element_by_link_text('后一页')
    print('Sleeping...')
    sleep(randint(27, 139) / 10)
    try:
        sleep(3)
        next_page_button.click()
    except:
        sleep(4)
        next_page_button = driver.find_element_by_link_text('后一页')
        next_page_button.click()




driver.quit()
