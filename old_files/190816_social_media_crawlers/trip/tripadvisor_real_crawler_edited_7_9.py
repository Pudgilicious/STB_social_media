from selenium import webdriver
from scrapy import Selector
import pandas as pd
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class TripAdvisorCrawler:
    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password
        self.linklist_to_clawer = []
        for i in open('res_link_dedup.txt'):
            self.linklist_to_clawer.append('https://www.tripadvisor.sg' + i)
        # options = Options()
        # options.add_argument('headless')
        # self.driver = webdriver.Chrome('/Users/admin/Desktop/chromedriver', options=options)
        self.driver = webdriver.Chrome('./chromedriver')
        self.name_list = []
        self.phonenumber_list = []
        self.address_list = []
        self.block_list = []
        self.price_list = []
        self.meal_list = []
        self.cuisine_type_list = []
        self.feature_list = []
        # self.atmosphere_list = []
        self.rating_atmosphere_list = []
        self.review_number_list = []
        self.rating_list = []
        self.rating_food_list = []
        self.rating_service_list = []
        self.rating_value_list = []
        self.open_hours_list = []
        self.data = {}
        self.coordinate = []
        self.special_diets = []
        self.dining_category = []
        self.index = []
        

    def log_in(self):
        self.driver.get('https://www.tripadvisor.cn')  #Go to this website
        self.driver.implicitly_wait(20)   #Driver to wait for 20s
        login_button = self.driver.find_element_by_class_name('login-button')
        login_button.send_keys('\n')   #this is same as enter. From selenium package
        time.sleep(2)
        user_name_input = self.driver.find_element_by_xpath('')     #Input box. Like filling in stuff here

    def crawl(self):
        count = 0
        for link in self.linklist_to_clawer:           
            print(count, 'of', len(self.linklist_to_clawer))
            count = count + 1             
            if (count < 7001): 
                continue
            if (count > 9000): 
                continue           
            try:
                self.index = []
                self.name_list = []
                self.phonenumber_list = []
                self.address_list = []
                self.block_list = []
                self.price_list = []
                self.meal_list = []
                self.cuisine_type_list = []
                self.feature_list = []
                # self.atmosphere_list = []
                self.rating_atmosphere_list = []
                self.review_number_list = []
                self.rating_list = []
                self.rating_food_list = []
                self.rating_service_list = []
                self.rating_value_list = []
                # self.open_hours_list = []
                self.data = {}
                self.coordinate = []
                self.special_diets = []
                self.dining_category = []   #added by JR
    
                time.sleep(random.uniform(1, 2))
                self.driver.get(link)
                self.driver.implicitly_wait(70)
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #Scroll down webpage to get more information
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.uniform(1, 2))
                sel = Selector(text=self.driver.page_source)
                # The attributes are lists, which are used to built a dic for dataframe later
                name = sel.xpath('//h1[@class="ui_header h1"]/text()').extract_first()
                self.name_list.append(name.encode('utf-8'))
                
                #Append count
                self.index.append(count)        
        
                # Dining category (cheap eats, fine dining, mid range)
                categories = ''
                #category = sel.xpath('//div[@class="prw_rup prw_restaurants_restaurant_detail_tags tagsContainer"]/a/@href').extract_first()            
                category  = self.driver.find_elements_by_css_selector(".header_links")
                categories  = [el.text for el in category]
                
                self.dining_category.append(categories)
                
                
                # Data of block
                block = ''
                block = sel.xpath('//span[@class="restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei restaurants-detail-overview-cards-LocationOverviewCard__nearbyText--6M5-L"]/div/text()').extract_first()
                self.block_list.append(block)
                if len(self.block_list) == 0:
                    block = ''
                    self.block_list.append(block.encode('utf-8'))
    
                # Data of phone number (xpath may change in each iteration). // search whole page. /search in node
                phone_number = ''
                phone_number = sel.xpath('//div[@class="restaurants-detail-overview-cards-LocationOverviewCard__detailLink--iyzJI"]/a/@href').extract_first()
                self.phonenumber_list.append(phone_number)
                # for i in sel.xpath('//ul[@class="detailsContent"]/li/div[@class="detail"]'):
                #     if i.xpath('text()').extract_first() == 'Phone Number:\n':
                #         phone_number = i.xpath('span/text()').extract_first()
                #         self.phonenumber_list.append(phone_number)
                # if len(self.phonenumber_list) == 0:
                #     self.phonenumber_list.append(phone_number)
    
                # Data of address (xpath may change in each iteration)
                address = ''
                address = sel.xpath('//span/div[@class="ui_link"]/span/text()').extract_first()
                # for i in sel.xpath('//ul[@class="detailsContent"]/li/div[@class="detail"]'):
                #     if i.xpath('text()').extract_first() == 'Address:\n':
                #         for j in i.xpath('span/span[@class="format_address"]/span/text()').extract():
                #             address = address + j + ' '
                #         address = address[:-1]
                #         self.address_list.append(address)
                # if len(self.address_list) == 0:
                #     self.address_list.append(address)
                self.address_list.append(address.encode('utf-8'))
    
                # Data of ratings of food, service, substantial and atmosphere
                food = ''
                service = ''
                value = ''
                atmosphere = ''
                for i in sel.xpath('//div[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingQuestionRow--5nPGK"]'):
                    if i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq"]/text()').extract_first() == 'Food':
                        food = i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC"]/span/@class').extract_first()
                        self.rating_food_list.append(food.encode('utf-8'))
                    if i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq"]/text()').extract_first() == 'Service':
                        service = i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC"]/span/@class').extract_first()
                        self.rating_service_list.append(service.encode('utf-8'))
                    if i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq"]/text()').extract_first() == 'Value':
                        value = i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC"]/span/@class').extract_first()
                        self.rating_value_list.append(value.encode('utf-8'))
                    if i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq"]/text()').extract_first() == 'Atmosphere':
                        atmosphere = i.xpath('span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC"]/span/@class').extract_first()
                        self.rating_atmosphere_list.append(atmosphere.encode('utf-8'))
    
                if len(self.rating_food_list) == 0:
                    self.rating_food_list.append(food)
                if len(self.rating_service_list) == 0:
                    self.rating_service_list.append(service)
                if len(self.rating_value_list) == 0:
                    self.rating_value_list.append(value)
                if len(self.rating_atmosphere_list) == 0:
                    self.rating_atmosphere_list.append(atmosphere)
    
                # Data of price, cuisine type, meal, feature, atmosphere
                price = ''
                cuisine_type = ''
                meal = ''
                feature = ''
                special_diets = ''
                for i in sel.xpath('//div[@class="ui_column  "]/div'):
                    if i.xpath('div[@class="restaurants-details-card-TagCategories__categoryTitle--28rB6"]/text()').extract_first() == 'PRICE RANGE':
                        price = i.xpath('div[@class="restaurants-details-card-TagCategories__tagText--Yt3iG"]/text()').extract_first()
                        self.price_list.append(price.encode('utf-8'))
    
                    if i.xpath('div[@class="restaurants-details-card-TagCategories__categoryTitle--28rB6"]/text()').extract_first() == 'CUISINES':
                        cuisine_type = i.xpath('div[@class="restaurants-details-card-TagCategories__tagText--Yt3iG"]/text()').extract_first()
                        self.cuisine_type_list.append(cuisine_type)
    
                    if i.xpath('div[@class="restaurants-details-card-TagCategories__categoryTitle--28rB6"]/text()').extract_first() == 'Meals':
                        meal = i.xpath('div[@class="restaurants-details-card-TagCategories__tagText--Yt3iG"]/text()').extract_first()
                        self.meal_list.append(meal)
    
                    if i.xpath('div[@class="restaurants-details-card-TagCategories__categoryTitle--28rB6"]/text()').extract_first() == 'FEATURES':
                        feature = i.xpath('div[@class="restaurants-details-card-TagCategories__tagText--Yt3iG"]/text()').extract_first()
                        self.feature_list.append(feature)
    
                    if i.xpath('div[@class="restaurants-details-card-TagCategories__categoryTitle--28rB6"]/text()').extract_first() == 'Special Diets':
                        special_diets = i.xpath('div[@class="restaurants-details-card-TagCategories__tagText--Yt3iG"]/text()').extract_first()
                        self.special_diets.append(special_diets)
    
                if len(self.special_diets) == 0 and len(self.special_diets) == 0 and len(self.price_list) == 0 and len(self.cuisine_type_list) == 0 and len(self.meal_list) == 0 and len(self.feature_list) == 0:
                    for i in sel.xpath('//div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__detailsSummary--evhlS"]/div'):
                        if i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_"]/text()').extract_first() == 'PRICE RANGE':
                            price = i.xpath('div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"]/text()').extract_first()
                            self.price_list.append(price.encode('utf-8'))
    
                        if i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_"]/text()').extract_first() == 'CUISINES':
                            cuisine_type = i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"]/text()').extract_first()
                            self.cuisine_type_list.append(cuisine_type)
    
                        if i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_"]/text()').extract_first() == 'Meals':
                            meal = i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"]/text()').extract_first()
                            self.meal_list.append(meal)
    
                        if i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_"]/text()').extract_first() == 'FEATURES':
                            feature = i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"]/text()').extract_first()
                            self.feature_list.append(feature)
    
                        if i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_"]/text()').extract_first() == 'Special Diets':
                            special_diets = i.xpath(
                                'div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"]/text()').extract_first()
                            self.special_diets.append(special_diets)
    
    
                if len(self.special_diets) == 0:
                    self.special_diets.append(special_diets)
                if len(self.price_list) == 0:
                    self.price_list.append(price)
                if len(self.cuisine_type_list) == 0:
                    self.cuisine_type_list.append(cuisine_type)
                if len(self.meal_list) == 0:
                    self.meal_list.append(meal)
                if len(self.feature_list) == 0:
                    self.feature_list.append(feature)
    
                # Data of open hours
                open_hours = ''
                # for i in sel.xpath('//div[@class="hours content"]/div[@class="detail"]//*/text()').extract():
                #     open_hours = open_hours + i + ' '
                #     open_hours = open_hours[:-1]
                # self.open_hours_list.append(open_hours)
    
                # Data of review numbers
                review_number = ''
                # all_language_button = self.driver.find_element_by_id('taplc_location_review_filter_controls_0_filterLang_ALL')
                # all_language_button.send_keys('\n')
                review_number = sel.xpath('//a[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG"]/text()').extract_first()
                self.review_number_list.append(review_number)
    
                # Data of rating
                rating = ''
                rating = sel.xpath('//span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl"]/text()').extract_first()
                if len(self.rating_list) == 0:
                    self.rating_list.append(rating.encode('utf-8'))
    
                # Data of coordinates
                coordinates = ''
                coordinates = sel.xpath('//span[@data-test-target]/img/@src').extract_first()
                try:
                    coordinates = coordinates[coordinates.find('|')+1:]
                except AttributeError:
                    time.sleep(5)
                    sel = Selector(text=self.driver.page_source)
                    time.sleep(1)
                    coordinates = sel.xpath('//span[@data-test-target]/img/@src').extract_first()
                    try:
                        coordinates = coordinates[coordinates.find('|') + 1:]
                    except AttributeError:
                        pass
                self.coordinate.append(coordinates)
    
                # Save Data
                self.data = {
                    'index': self.index,                
                    'name': self.name_list,
                    'phonenumber': self.phonenumber_list,
                    'address': self.address_list,
                    'block': self.block_list,
                    'price': self.price_list,
                    'meal': self.meal_list,
                    'cuisine_type': self.cuisine_type_list,
                    'feature': self.feature_list,
                    # 'atmosphere': self.atmosphere_list,
                    'review_number': self.review_number_list,
                    'rating': self.rating_list,
                    'rating_food': self.rating_food_list,
                    'rating_service': self.rating_service_list,
                    'rating_value': self.rating_value_list,
                    'rating_atmosphere': self.rating_atmosphere_list,
                    # 'open_hours': self.open_hours_list,
                    'special_diets': self.special_diets,
                    'coordinates': self.coordinate,
                    'dining_category': self.dining_category
                }
                print(self.data)
                df = pd.DataFrame(self.data)
                if count == 1:
                    df.to_csv('trip_adviser_res_7_9.csv')
                else:
                    df.to_csv('trip_adviser_res_7_9.csv', mode='a', header=None)
                
            except:
                print('Error in ' + str(count))
                log = "./log/" + str(count) +'.txt'
                f = open(log, 'w')
                f.close()
                
            
        self.driver.quit()
    # def save_data(self, path):
    #     self.data = {
    #         'name_list': self.name_list,
    #         'phonenumber_list': self.phonenumber_list,
    #         'address_list': self.address_list,
    #         'block_list': self.block_list,
    #         'price_list': self.price_list,
    #         'meal_list': self.meal_list,
    #         'cuisine_type_list': self.cuisine_type_list,
    #         'feature_list': self.feature_list,
    #         'atmosphere_list': self.atmosphere_list,
    #         'review_number_list': self.review_number_list,
    #         'rating_list': self.rating_list,
    #         'rating_food_list': self.rating_food_list,
    #         'rating_service_list': self.rating_service_list,
    #         'rating_value_list': self.rating_value_list,
    #         'rating_atmosphere_list': self.rating_atmosphere_list,
    #         'open_hours_list': self.open_hours_list,
    #     }
    #     df = pd.DataFrame(self.data)
    #     df.to_csv(path)


if __name__ == '__main__':
        clawer = TripAdvisorCrawler('your_account', 'your_password')
        # clawer.log_in()
        clawer.crawl()
        # clawer.save_data('trip_adviser_res.csv')


