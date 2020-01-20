import pandas as pd
import mysql.connector
import yaml
import time
from crawl_TripA_POI_attributes_reviews import CrawlTripAdvisor

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']

db_in_flag = configs['TripAdvisor']['db_in_flag']
db_out_flag = configs['TripAdvisor']['db_out_flag']

if not db_in_flag:
    
    ### FOR POC ONLY ###
    poi_index = [1, 2]
    poi_name = ['Gardens by the Bay', 
                'Marina Bay Sands Skypark'
               ]
    poi_url = ['https://www.tripadvisor.com.sg/Attraction_Review-g294265-d2149128-Reviews-Gardens_by_the_Bay-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d1837767-Reviews-Marina_Bay_Sands_Skypark-Singapore.html'
              ]
    poi_df = pd.DataFrame(
        dict(
            poi_index=poi_index,
            poi_name=poi_name,
            poi_url=poi_url)
        )
    ####################

if db_in_flag:
    poi_df = pd.DataFrame()

if db_in_flag == True or db_out_flag == True:
    cnx = mysql.connector.connect(host=configs['General']['host'],
                                  database=configs['General']['database'],
                                  user=configs['General']['user'],
                                  password=configs['General']['password']
                                 )
else:
    cnx = None
    
if __name__=="__main__":
    crawler = CrawlTripAdvisor(chromedriver_path, poi_df, cnx, db_out_flag)
    start_time = time.time()
    crawler.crawl_pois(number_of_pages=100)
    end_time = time.time()
    print('Total time taken (min): ' + str((end_time - start_time)/60))
