import pandas as pd
import traceback
import yaml
from selenium import webdriver
from datetime import datetime
from time import sleep

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']
csv_input_path = configs['TripAdvisor']['csv_input_path']

poi_df = pd.read_csv(csv_input_path)
poi_df['URL'] = poi_df['URL'].apply(lambda x: 'https://tripadvisor.com.sg' + x)


class TripAdvisorAspectCrawler:
    aspects_col_names = ['POI_INDEX',
                         'ASPECTS',
                         'ATTRACTION_TYPES',
                         'ASPECTS_CRAWLED_TIME'
                         ]
    def __init__(self):
        self.chromedriver_path = chromedriver_path
        self.driver = webdriver.Chrome(self.chromedriver_path)
        self.poi_df = poi_df

        self.current_df_row = None
        self.current_poi_index = None
        self.current_poi_name = None
        self.current_poi_url = None
        self.aspects_df = pd.DataFrame(columns=self.aspects_col_names)

        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
        self.aspects_df.to_csv(
            './tripadvisor/output/aspects_{}.csv'.format(self.datetime_string),
            mode='a',
            index=False
        )

        # Certain aspects are only displayed on maximized window
        self.driver.maximize_window()

    def crawl_aspects(self):
        while len(self.poi_df.index) > 0:
            self.current_df_row = self.poi_df.iloc[0]
            self.current_poi_index = self.current_df_row['POI_INDEX']
            self.current_poi_name = self.current_df_row['POI_NAME']
            self.current_poi_url = self.current_df_row['URL']

            try:
                self.driver.get(self.current_poi_url)
                print("POI index: {}, {}".format(self.current_poi_index, self.current_poi_name))
                sleep(10)
                view_more_elements = self.driver.find_elements_by_xpath('//span[@class="viewMore"]')
                if view_more_elements:
                    view_more_elements[0].click()
                    sleep(1)
                attraction_types = self.driver.find_element_by_xpath(
                    '//span[@class="is-hidden-mobile header_detail attractionCategories"]'
                ).text
                aspects_elements = self.driver.find_elements_by_xpath(
                    '//button[@class="ui_button secondary small location-review-review-list-parts-SearchFilter__word_button_secondary--2p0YL"]'
                )

            except:
                print("Exception has occurred. Please check log file.")
                log = open('./tripadvisor/output/aspects_log_{}.txt'.format(self.datetime_string), 'a+')
                log.write('{}, {}\n'.format(self.current_poi_index,
                                            self.current_poi_name,
                                            datetime.now()
                                            ))
                log.write(traceback.format_exc() + '\n')
                log.close()

                # Restart chromedriver
                self.driver.close()
                sleep(2)  # To allow keyboard interrupt
                self.driver = webdriver.Chrome(self.chromedriver_path)
                self.driver.maximize_window()

                # Reset aspects_df to header-only for next POI
                self.aspects_df = pd.DataFrame(columns=self.aspects_col_names)

                # Remove first row from poi_df
                self.poi_df = self.poi_df.iloc[1:]

                continue

            for element in aspects_elements:
                aspect = element.text
                aspect_details = [self.current_poi_index, aspect, attraction_types, datetime.now()]
                aspect_dict = dict(zip(self.aspects_col_names, aspect_details))
                self.aspects_df = self.aspects_df.append(aspect_dict, ignore_index=True)

            # Write all aspects for 1 POI to csv
            self.aspects_df.to_csv(
                './tripadvisor/output/aspects_{}.csv'.format(
                    self.datetime_string),
                mode='a',
                index=False,
                header=False
            )

            # Reset aspects_df to header-only for next POI
            self.aspects_df = pd.DataFrame(columns=self.aspects_col_names)

            # Remove first row from poi_df
            self.poi_df = self.poi_df.iloc[1:]


crawler = TripAdvisorAspectCrawler()
crawler.crawl_aspects()