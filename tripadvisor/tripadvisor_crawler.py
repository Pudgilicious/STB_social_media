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
        self.number_of_pages = None
        self.earliest_date = None
        self.start_page = None
        self.current_date = None
        self.current_page = None
        self.current_trip_type = None
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

        def crawl_pois(self, start_page=None, number_of_pages=None, earliest_date=None, trip_types=None):
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
                self.current_url = row['poi_url']
                self.reviews_df.to_csv('./tripadvisor/output/{}/reviews/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', index=False)
                self.reviewers_df.to_csv('./tripadvisor/output/{}/reviewers/{}.csv'.format(self.datetime_string, self.current_poi_index), mode='a', index=False)

                for trip_type in trip_types:
                    self.current_trip_type = trip_type
                    crawl_poi_by_trip_type()

        ### KIV: WIP ###
        def crawl_poi_by_trip_type(self):
            print('########## {}: {} ##########'.format(self.current_poi_name, self.current_trip_type))

            # Crawl
            try:
                self.driver.get(self.current_poi_url)
                self.crawl_attributes(self.current_poi_index)
                self.attributes_df.to_csv('./tripadvisor/output/{}/attributes.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
                self.crawl_reviews(self.current_poi_index)
                if self.db_out_flag != 'csv':
                    self.add_to_database()
            except Exception as e:
                print("Exception has occurred. Please check log file.")
                log = open('./tripadvisor/output/{}/log.txt'.format(self.datetime_string), 'a+')
                log.write('{}, {}, page: {}, {}, {}\n'.format(row['poi_index'],
                                                                   row['poi_name'],
                                                                   self.current_date,
                                                                   self.current_page,
                                                                   datetime.now()
                                                                   ))
                log.write(traceback.format_exc() + '\n')
                log.close()

