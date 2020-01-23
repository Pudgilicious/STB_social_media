import pandas as pd
import os
import re
import traceback
from selenium import webdriver
from datetime import datetime, timedelta
from time import sleep

class TripAdvisorCrawler:
    attributes_col_names = ['POI_INDEX',
                            'TOTAL_REVIEWS',
                            'RANKING',
                            'TRIP_TYPE',
                            'AVERAGE_RATING',
                            'RATING_5_COUNT',
                            'RATING_4_COUNT',
                            'RATING_3_COUNT',
                            'RATING_2_COUNT',
                            'RATING_1_COUNT',
                            'ABOUT',
                            'ADDRESS',
                            'ATTRIBUTES_CRAWLED_TIME'
                           ]

    reviews_col_names = ['REVIEW_INDEX',
                         'WEBSITE_INDEX',
                         'POI_INDEX',
                         'REVIEWER_URL',
                         'REVIEW_ID',
                         'REVIEW_DATE',
                         'REVIEW_RATING',
                         'REVIEW_TITLE',
                         'REVIEW_BODY',
                         'DATE_OF_EXPERIENCE',
                         'TRIP_TYPE',
                         'REVIEW_CRAWLED_TIME'
                        ]

    reviewers_col_names = ['REVIEWER_URL',
                           'REVIEWER_NAME',
                           'RAW_HOME_LOCATION',
                           'CLEANED_HOME_LOCATION',
                           'NUMBER_OF_CONTRIBUTIONS',
                           'HELPFUL_VOTES',
                           'REVIEWER_UPDATED_TIME'
                          ]

    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.driver = webdriver.Chrome(chromedriver_path)
        self.poi_df = poi_df
        if cnx:
            self.cursor = cnx.cursor()
        self.db_out_flag = db_out_flag

        self.fsm_state = 0

        # User input parameters into crawl_pois method
        self.number_of_pages = None
        self.earliest_date = None
        self.start_page = None
        self.trip_types_to_crawl = None

        # Reset after every trip type
        self.current_date = None
        self.current_page = None
        self.current_trip_type = None

        # Reset after every POI
        self.current_poi_index = None
        self.current_poi_name = None
        self.current_poi_url = None  # Original POI URL, not crawling/current page

        self.review_final_page = False
        self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
        self.reviewers_df = pd.DataFrame(columns=self.reviewers_col_names)

        # Create unique folder, sub-folders and attribute.csv
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        os.makedirs('./tripadvisor/output/{}/'.format(self.datetime_string))
        os.makedirs('./tripadvisor/output/{}/reviews'.format(self.datetime_string))
        os.makedirs('./tripadvisor/output/{}/reviewers'.format(self.datetime_string))
        self.attributes_df.to_csv('./tripadvisor/output/{}/attributes.csv'.format(self.datetime_string), mode='a', index=False)

    def add_to_database(self):
        # Read CSVs, add to database, then cnx.commit()
        return

    def crawl_pois(self, start_page=None, number_of_pages=None, earliest_date=None, trip_types=["Family", "Couples", "Solo", "Business", "Friends"]):
        self.fsm_state = 1
        if start_page is not None:
            self.start_page = start_page
        if number_of_pages is not None:
            self.number_of_pages = number_of_pages
        if earliest_date is not None:
            self.earliest_date = datetime.strptime(earliest_date, '%d-%m-%Y')

        for _, row in self.poi_df.iterrows():

            # Create <POI_INDEX>.csv in reviews and reviewers folders.
            self.current_poi_index = row['poi_index']
            self.current_poi_name = row['poi_name']
            self.current_poi_url = row['poi_url']
            self.reviews_df.to_csv('./tripadvisor/output/{}/reviews/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', index=False)
            self.reviewers_df.to_csv('./tripadvisor/output/{}/reviewers/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', index=False)

            if not self.trip_types_to_crawl:
                self.trip_types_to_crawl = trip_types

            while self.trip_types_to_crawl:
                self.current_trip_type = self.trip_types_to_crawl[0]
                if self.fsm_state != 3:
                    self.crawl_poi_by_trip_type()
                else:
                    return

    def crawl_poi_by_trip_type(self):
        print('########## {}, {} ##########'.format(self.current_poi_name, self.current_trip_type))

        try:
            self.fsm_state = 2
            self.driver.get(self.current_poi_url)
            sleep(2)

            # Click on "Traveller Type" filter, based on trip types 1-5
            traveller_type_element = self.driver.find_element_by_xpath('//div[@data-tracker="{}"]'.format(self.current_trip_type))
            traveller_type_element.click()
            sleep(2)

            self.crawl_attributes()
            self.attributes_df.to_csv('./tripadvisor/output/{}/attributes.csv'.format(self.datetime_string), mode='a', header=False, index=False)
            self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
            self.crawl_reviews()
            self.trip_types_to_crawl.pop(0)
            self.current_date = None
            self.current_page = None
            self.current_trip_type = None

            if self.db_out_flag != 'csv':
                self.add_to_database()

            # Need to un-filter "Traveller Type"
            self.driver.execute_script("scroll(0, 0);")  # JavaScript
            sleep(2)
            traveller_type_element = self.driver.find_element_by_xpath('//div[@data-tracker="{}"]'.format(self.current_trip_type))
            traveller_type_element.click()
            sleep(2)

        except Exception as e:
            self.fsm_state = 3
            print("Exception has occurred. Please check log file.")
            log = open('./tripadvisor/output/{}/log.txt'.format(self.datetime_string), 'a+')
            log.write('{}, {}, page: {}, {}, {}\n'.format(self.current_poi_index,
                                                          self.current_poi_name,
                                                          self.current_date,
                                                          self.current_page,
                                                          datetime.now()
                                                          ))
            log.write(traceback.format_exc() + '\n')
            log.close()

    ### KIV: WIP ###
    def open_to_page(self):
        pass

    def crawl_attributes(self):
        ranking_text = self.driver.find_element_by_xpath('//span[@class="header_popularity popIndexValidation "]').text
        rating_breakdown_elements = self.driver.find_elements_by_xpath('//span[@class="row_num  is-shown-at-tablet"]')
        address_text = self.driver.find_element_by_xpath('//span[@class="textAlignWrapper address"]').text
        about_more_button = self.driver.find_elements_by_xpath('//span[@class="attractions-attraction-detail-about-card-Description__readMore--2pd33"]')
        if about_more_button:
            about_more_button[0].click()
            sleep(2)
            about_text = self.driver.find_element_by_xpath('//div[@class="attractions-attraction-detail-about-card-Description__modalText--1oJCY"]').text
            about_more_close_button = self.driver.find_element_by_xpath('//div[@class="_2EFRp_bb"]')
            about_more_close_button.click()
            sleep(2)
        else:
            about_text = self.driver.find_element_by_xpath('//div[@class="attractions-attraction-detail-about-card-AttractionDetailAboutCard__section--1_Efg"]').text

        # Parsing attributes
        rating_breakdown = self.parse_rating_breakdown_elements(rating_breakdown_elements)
        total_reviews = self.calculate_total_reviews(rating_breakdown)
        ranking = self.parse_ranking_text(ranking_text)
        average_rating = self.calculate_average_rating(rating_breakdown)
        about = about_text
        address = address_text

        poi_attributes = [self.current_poi_index,
                          total_reviews,
                          ranking,
                          self.current_trip_type,
                          average_rating,
                          rating_breakdown[0],
                          rating_breakdown[1],
                          rating_breakdown[2],
                          rating_breakdown[3],
                          rating_breakdown[4],
                          about,
                          address,
                          datetime.now()
                         ]

        # Inserting attributes into dataframe
        poi_attributes_dict = dict(zip(self.attributes_col_names, poi_attributes))
        self.attributes_df = self.attributes_df.append(poi_attributes_dict, ignore_index=True)

    def crawl_reviews(self):
        if self.earliest_date is not None:
            self.current_date = datetime.now()
            self.current_page = 1
            while self.current_date >= self.earliest_date:
                print('Page {}'.format(self.current_page))
                self.crawl_reviews_1_page(self.current_poi_index)
                self.reviews_to_csv()
                self.current_page += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break
        elif self.number_of_pages is not None:
            self.current_page = 1
            for i in range(self.number_of_pages):
                print('Page {}'.format(self.current_page))
                self.crawl_reviews_1_page(self.current_poi_index)
                self.reviews_to_csv()
                self.current_page += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break
        else:
            self.current_page = 1
            while not self.review_final_page:
                print('Page {}'.format(self.current_page))
                self.crawl_reviews_1_page(self.current_poi_index)
                self.reviews_to_csv()
                self.current_page += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break

    def reviews_to_csv(self):
        self.reviews_df.to_csv('./tripadvisor/output/{}/reviews/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', header=False, index=False)
        self.reviewers_df.to_csv('./tripadvisor/output/{}/reviewers/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', header=False, index=False)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
        self.reviewers_df = pd.DataFrame(columns=self.reviewers_col_names)

    def crawl_reviews_1_page(self, poi_index):
        review_more_button = self.driver.find_elements_by_xpath('//span[@class="taLnk ulBlueLinks"]')
        if review_more_button:
            review_more_button[0].click()
            sleep(2)

        # Crawling review elements.
        reviewer_name_elements = self.driver.find_elements_by_xpath('//div[@class="info_text pointer_cursor"]/div[1]')
        home_location_elements = self.driver.find_elements_by_xpath('//div[@class="info_text pointer_cursor"]')
        review_date_elements = self.driver.find_elements_by_xpath('//span[@class="ratingDate"]')
        review_container_elements = self.driver.find_elements_by_xpath('//div[@class="review-container"]')
        review_title_elements = self.driver.find_elements_by_xpath('//span[@class="noQuotes"]')
        review_body_elements = self.driver.find_elements_by_xpath('//p[@class="partial_entry"]')
        date_of_experience_elements = self.driver.find_elements_by_xpath('//div[@data-prwidget-name="reviews_stay_date_hsx"]')

        for i in range(len(reviewer_name_elements)):
            reviewer_url = self.parse_userid_elements(reviewer_name_elements[i].text)
            reviewer_name = reviewer_name_elements[i].text
            review_id = review_container_elements[i].get_attribute('data-reviewid')
            review_date = self.parse_review_date(review_date_elements[i].get_attribute('title'))
            home_location = self.parse_home_location(home_location_elements[i].text, reviewer_name)
            review_rating_element = self.driver.find_element_by_xpath('//*[@id="review_{}"]/div/div[2]/span[1]'.format(review_id)).get_attribute('class')
            review_rating = self.parse_review_rating_element(review_rating_element)
            review_title = review_title_elements[i].text
            review_body = review_body_elements[i].text
            date_of_experience = self.parse_date_of_experience(date_of_experience_elements[i].text)

            if self.earliest_date is not None and self.current_date < self.earliest_date:
                break

            review_details = [None,  # REVIEW_INDEX
                              1,  # WEBSITE_INDEX (TripAdvisor is '1')
                              self.current_poi_index,
                              reviewer_url,
                              review_id,
                              review_date,
                              review_rating,
                              review_title,
                              review_body,
                              date_of_experience,
                              self.current_trip_type,
                              datetime.now()
                             ]

            reviewer_details = [reviewer_url,
                                reviewer_name,
                                home_location,
                                None,  # CLEANED_HOME_LOCATION
                                "CONTRIBUTION",
                                "VOTES",
                                datetime.now()
                               ]

            # Inserting reviews into dataframe.
            review_details_dict = dict(zip(self.reviews_col_names, review_details))
            self.reviews_df = self.reviews_df.append(review_details_dict, ignore_index=True)

            # Inserting reviewers into dataframe.
            reviewer_details_dict = dict(zip(self.reviewers_col_names, reviewer_details))
            self.reviewers_df = self.reviewers_df.append(reviewer_details_dict, ignore_index=True)

        next_button_element = self.driver.find_elements_by_xpath('//a[@class="nav next ui_button primary"]')
        if next_button_element:
            next_button_element[0].click()
            sleep(2)
        else:
            self.review_final_page = True

    # Instance method which also updates self.current_date.
    def parse_review_date(self, text):
        if len(re.search('(\d+) (\w+)', text).group(1)) == 1: # ensures %d %B %Y format
            text = '0' + text
        date = datetime.strptime(text, '%d %B %Y')
        self.current_date = date
        return date.strftime('%d-%m-%Y')

    # Methods below are all static utility functions.
    @staticmethod
    def calculate_total_reviews(rating_breakdown):
        return sum(rating_breakdown)

    @staticmethod
    def parse_ranking_text(text):
        return int(text[1:text.find(' of')].replace(',', ''))

    @staticmethod
    def calculate_average_rating(rating_breakdown):
        total = sum(rating_breakdown)
        if total == 0:
            return 0
        average = 0
        for i, j in enumerate(rating_breakdown[::-1]):
            average += (i+1)*j/total
        return average

    @staticmethod
    def parse_rating_breakdown_elements(elements):
        rating_breakdown = []
        for element in elements:
            text = element.text
            rating_breakdown.append(int(text.replace(',', '')))
        return rating_breakdown

    @staticmethod
    def parse_userid_elements(text):
        return 'https://www.tripadvisor.com.sg/Profile/' + text

    @staticmethod
    def parse_review_rating_element(text):
        return int(text[-2])

    @staticmethod
    def parse_home_location(text, reviewer_name):
        return text[text.find(reviewer_name) + len(reviewer_name):]

    @staticmethod
    def parse_date_of_experience(text): ###
        substring = re.search('Date of experience: (.+)', text).group(1)
        return datetime.strptime(substring, '%B %Y').strftime('%m-%Y')
