import pandas as pd
import mysql.connector
import time
import yaml

from tripadvisor_crawler import TripAdvisorCrawler

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']

db_in_flag = configs['TripAdvisor']['db_in_flag']
db_out_flag = configs['TripAdvisor']['db_out_flag']

if db_in_flag == 'csv':

    ### FOR POC ONLY ###
    poi_index = [40, 242, 660]
    poi_name = ['Henderson Waves',
                'West Coast Plaza',
                'NTU Centre for Contemporary Art'
               ]
    poi_url = ['https://www.tripadvisor.com.sg/Attraction_Review-g294265-d3561693-Reviews-Henderson_Waves-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d12204918-Reviews-West_Coast_Plaza-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d8738861-Reviews-NTU_Centre_for_Contemporary_Art-Singapore.html'
              ]
    poi_df = pd.DataFrame(
        dict(poi_index=poi_index,
             poi_name=poi_name,
             poi_url=poi_url)
            )
    ####################

if db_in_flag != 'csv':
    poi_df = pd.DataFrame()

if db_in_flag != 'csv' or db_out_flag != 'csv':
    cnx = mysql.connector.connect(host=configs['General']['host'],
                                  database=configs['General']['database'],
                                  user=configs['General']['user'],
                                  password=configs['General']['password']
                                 )
else:
    cnx = None

if __name__=="__main__":
    crawler = TripAdvisorCrawler(chromedriver_path, poi_df, cnx, db_out_flag)
    start_time = time.time()  # Time at start.
    crawler.crawl_pois(earliest_date=configs['TripAdvisor']['earliest_date'],
                       number_of_pages=configs['TripAdvisor']['number_of_pages'],
                       trip_types = ['Family', 'Couples', 'Solo', 'Business', 'Friends']
                       )
    end_time = time.time()  # Time at end.
    print('Total time taken (min): ' + str((end_time - start_time)/60))  # Print time difference.
