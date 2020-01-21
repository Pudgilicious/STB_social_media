import pandas as pd
import re
from selenium import webdriver
from datetime import datetime, timedelta
from time import sleep

class CrawlTripAdvisor:
    attributes_col_names = ['POI_INDEX',
                            'TOTAL_REVIEWS',
                            'RANKING',
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
        if cnx is not None:
            self.cursor = cnx.cursor()
        self.db_out_flag = db_out_flag

        self.number_of_pages = None
        self.earliest_date = None
        self.current_date = None
        self.review_final_page = False
        self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
        self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
        self.reviewers_df = pd.DataFrame(columns=self.reviewers_col_names)

        # Create unique CSVs.
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        self.attributes_df.to_csv('./tripadvisor/output/attributes_{}.csv'.format(self.datetime_string), mode='a', index=False)
        self.reviews_df.to_csv('./tripadvisor/output/reviews_{}.csv'.format(self.datetime_string), mode='a', index=False)
        self.reviewers_df.to_csv('./tripadvisor/output/reviewers_{}.csv'.format(self.datetime_string), mode='a', index=False)

    def add_to_database(self):
        # Read CSVs, add to database, then cnx.commit().
        return

    def crawl_pois(self, number_of_pages=None, earliest_date=None): # earliest_date in 'dd-mm-yyyy'
        if number_of_pages is not None:
            self.number_of_pages = number_of_pages
        if earliest_date is not None:
            self.earliest_date = datetime.strptime(earliest_date, '%d-%m-%Y')

        for _, row in self.poi_df.iterrows():
            print('########## {} ##########'.format(row['poi_name']))
            self.driver.get(row['poi_url'])
            self.crawl_attributes(row['poi_index'])
            self.attributes_df.to_csv('./tripadvisor/output/attributes_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
            self.attributes_df = pd.DataFrame(columns=self.attributes_col_names)
            self.crawl_reviews(row['poi_index'])
            if self.db_out_flag:
                self.add_to_database()

    def crawl_reviews(self, poi_index):
        if self.earliest_date is not None:
            self.current_date = datetime.now()
            page_number = 1
            while self.current_date >= self.earliest_date:
                print('Page {}'.format(page_number))
                self.crawl_reviews_1_page(poi_index)
                self.reviews_df.to_csv('./tripadvisor/output/reviews_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.reviewers_df.to_csv('./tripadvisor/output/reviewers_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
                self.reviewers_df = pd.DataFrame(columns=self.reviewers_col_names)
                page_number += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break
        elif self.number_of_pages is not None:
            for i in range(self.number_of_pages):
                print('Page {}'.format(i+1))
                self.crawl_reviews_1_page(poi_index)
                self.reviews_df.to_csv('./tripadvisor/output/reviews_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.reviewers_df.to_csv('./tripadvisor/output/reviewers_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
                self.reviewers_df = pd.DataFrame(columns=self.reviewers_col_names)
                if self.review_final_page:
                    self.review_final_page = False
                    break
        else:
            page_number = 1
            while not self.review_final_page:
                print('Page {}'.format(page_number))
                self.crawl_reviews_1_page(poi_index)
                self.reviews_df.to_csv('./tripadvisor/output/reviews_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.reviewers_df.to_csv('./tripadvisor/output/reviewers_{}.csv'.format(self.datetime_string), mode='a', header=False, index=False)
                self.reviews_df = pd.DataFrame(columns=self.reviews_col_names)
                self.reviewers_df = pd.DataFrame(columns=self.reviewers_col_names)
                page_number += 1
                if self.review_final_page:
                    self.review_final_page = False
                    break

    def crawl_attributes(self, poi_index):
        driver = self.driver

        # Crawling attributes elements.
        ranking_text = driver.find_element_by_xpath('//span[@class="header_popularity popIndexValidation "]').text
        rating_breakdown_elements = driver.find_elements_by_xpath('//span[@class="location-review-review-list-parts-ReviewRatingFilter__row_num--3cSP7"]')
        address_text = driver.find_element_by_xpath('//span[@class="textAlignWrapper address"]').text
        about_more_button = driver.find_elements_by_xpath('//span[@class="attractions-attraction-detail-about-card-Description__readMore--2pd33"]')
        if about_more_button:
            about_more_button[0].click()
            sleep(0.5)
            about_text = driver.find_element_by_xpath('//div[@class="attractions-attraction-detail-about-card-Description__modalText--1oJCY"]').text
            about_more_close_button = driver.find_element_by_xpath('//div[@class="_2EFRp_bb"]')
            about_more_close_button.click()
            sleep(0.5)
        else:
            about_text = driver.find_element_by_xpath('//div[@class="attractions-attraction-detail-about-card-AttractionDetailAboutCard__section--1_Efg"]').text

        # Parsing attributes.
        rating_breakdown = self.parse_rating_breakdown_elements(rating_breakdown_elements)
        total_reviews = self.calculate_total_reviews(rating_breakdown)
        ranking = self.parse_ranking_text(ranking_text)
        average_rating = self.calculate_average_rating(rating_breakdown)
        about = about_text
        address = address_text

        poi_attributes = [poi_index,
                          total_reviews,
                          ranking,
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

    def crawl_reviews_1_page(self, poi_index):
        driver = self.driver
        sleep(2)

        # To crawl all languages, uncomment the follwing 3 lines:
        # all_languages_button = driver.find_element_by_xpath('//span[@class="location-review-review-list-parts-LanguageFilter__no_wrap--2Dckv"]')
        # all_languages_button.click()
        # sleep(1)

        read_more_button = driver.find_element_by_xpath('//span[@class="location-review-review-list-parts-ExpandableReview__cta--2mR2g"]')
        read_more_button.click()
        sleep(1)

        # Crawling review elements.
        reviewer_url_elements = driver.find_elements_by_xpath('//div[@class="social-member-event-MemberEventOnObjectBlock__event_type--3njyv"]/span/a')
        reviewer_details_elements = driver.find_elements_by_xpath('//div[@class="social-member-event-MemberEventOnObjectBlock__event_wrap--1YkeG"]')
        review_id_elements = driver.find_elements_by_xpath('//div[@class="location-review-review-list-parts-SingleReview__mainCol--1hApa"]')
        review_rating_elements = driver.find_elements_by_xpath('//div[@class="location-review-review-list-parts-RatingLine__bubbles--GcJvM"]/span')
        review_title_elements = driver.find_elements_by_xpath('//a[@class="location-review-review-list-parts-ReviewTitle__reviewTitleText--2tFRT"]')
        review_body_elements = driver.find_elements_by_xpath('//div[@class="location-review-review-list-parts-ExpandableReview__containerStyles--1G0AE"]')

        for i in range(len(reviewer_url_elements)):

            # Parsing review and reviewer details
            reviewer_url = reviewer_url_elements[i].get_attribute('href')
            reviewer_name = reviewer_url_elements[i].text
            review_id = self.parse_review_id_elements(review_id_elements[i].get_attribute('data-reviewid'))
            review_date = self.parse_review_date(reviewer_details_elements[i].text)
            if self.earliest_date is not None and self.current_date < self.earliest_date:
                break
            location_contribution_votes = self.parse_location_contributions_votes(reviewer_details_elements[i].text)
            review_rating = self.parse_review_rating(review_rating_elements[i].get_attribute('class'))
            review_title = review_title_elements[i].text
            review_body = self.parse_review_body(review_body_elements[i].text)
            date_of_experience = self.parse_date_of_experience(review_body_elements[i].text)
            trip_type = self.parse_trip_type(review_body_elements[i].text)

            review_details = [None,  # REVIEW_INDEX
                              1,  # WEBSITE_INDEX (TripAdvisor is '1')
                              poi_index,
                              reviewer_url,
                              review_id,
                              review_date,
                              review_rating,
                              review_title,
                              review_body,
                              date_of_experience,
                              trip_type,
                              datetime.now()
                             ]

            reviewer_details = [reviewer_url,
                                reviewer_name,
                                location_contribution_votes[0],
                                None,  # CLEANED_HOME_LOCATION
                                location_contribution_votes[1],
                                location_contribution_votes[2],
                                datetime.now()
                               ]

            # Inserting reviews into dataframe.
            review_details_dict = dict(zip(self.reviews_col_names, review_details))
            self.reviews_df = self.reviews_df.append(review_details_dict, ignore_index=True)

            # Inserting reviewers into dataframe.
            reviewer_details_dict = dict(zip(self.reviewers_col_names, reviewer_details))
            self.reviewers_df = self.reviewers_df.append(reviewer_details_dict, ignore_index=True)

        next_button_element = driver.find_elements_by_xpath('//a[@class="ui_button nav next primary "]')
        if next_button_element:
            next_button_element[0].click()
        else:
            self.review_final_page = True

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
        average = 0
        for i, j in enumerate(rating_breakdown[::-1]):
            average += (i+1)*j/total
        return average

    @staticmethod
    def parse_rating_breakdown_elements(elements):
        rating_breakdown = []
        for element in elements:
            text = element.text
            rating_breakdown.append(int(text.replace(",", "")))
        return rating_breakdown

    def parse_review_date(self, text):
        date_string = text[text.find('wrote a review ')+15:text.find('\n')]

        if date_string == 'Today':
            date = datetime.now()
            self.current_date = date
            return date.strftime('%d-%m-%Y')
        elif date_string == 'Yesterday':
            date = datetime.now() - timedelta(1)
            self.current_date = date
            return date.strftime('%d-%m-%Y')

        re_search = re.search('(\d+) (\w+)', date_string)
        current_year = datetime.now().strftime('%Y')
        if re_search is not None:
            if len(re_search.group(1)) == 1:
                date = datetime.strptime('0' + date_string + ' ' + current_year, '%d %b %Y')
                self.current_date = date
                return date.strftime('%d-%m-%Y')
            else:
                date = datetime.strptime(date_string + ' ' + current_year, '%d %b %Y')
                self.current_date = date
                return date.strftime('%d-%m-%Y')

        date = datetime.strptime(date_string, '%b %Y')
        self.current_date = date
        return date.strftime('%m-%Y')

    @staticmethod
    def parse_location_contributions_votes(text):
        location, contributions, votes = None, None, None

        votes_search = re.search('((\d+)?,?\d+) helpful votes?', text)
        if votes_search is not None:
            votes = int(votes_search.group(1).replace(",", ""))

        # This field is always present.
        contributions_search = re.search('((\d+)?,?\d+) contributions?', text)
        contributions = int(contributions_search.group(1).replace(",", ""))

        location_search = re.search('(.+?){} contributions?'.format(contributions_search.group(1)), text)
        if location_search is not None:
            location = location_search.group(1)

        return location, contributions, votes

    @staticmethod
    def parse_review_id_elements(text):
        return int(text)

    @staticmethod
    def parse_review_rating(text):
        return int(text[-2:])//10

    @staticmethod
    def parse_review_body(text):
        return text[:text.find('Read less')-1]

    @staticmethod
    def parse_date_of_experience(text):
        substring = re.search('Date of experience: (.+)\n', text).group(1)
        return datetime.strptime(substring, '%B %Y').strftime('%m-%Y')

    @staticmethod
    def parse_trip_type(text):
        if text.find('Trip type: ') == -1:
            return None
        substring = text[text.find('Trip type: ')+11:]
        return substring[:substring.find('\n')]
