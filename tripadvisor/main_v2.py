import pandas as pd
import mysql.connector
import time
import yaml

from tripadvisor_fsm_v2 import TripAdvisorFSM

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']

db_in_flag = configs['TripAdvisor']['read_from_database']
db_out_flag = configs['TripAdvisor']['write_to_database']

if db_in_flag == 'csv':

    ### FOR POC ONLY ###
    poi_index = [#2,
                 #3,
                 #7,
                 45,
                 183,
                 287,
                 310
                ]
    poi_name = [#'Singapore Botanic Gardens',
                #'Singapore Zoo',
                #'Singapore Flyer',
                'Wild Wild Wet',
                'Kent Ridge Park',
                'Clementi Mall',
                'Ann Siang Hill Park'
               ]
    poi_url = [#'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d310900-Reviews-Singapore_Botanic_Gardens-Singapore.html',
               #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html',
               #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d678639-Reviews-Singapore_Flyer-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d641343-Reviews-Wild_Wild_Wet-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d2291384-Reviews-Kent_Ridge_Park-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d12309383-Reviews-Clementi_Mall-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d8484024-Reviews-Ann_Siang_Hill_Park-Singapore.html'
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
    start_time = time.time()
    fsm = TripAdvisorFSM(chromedriver_path, poi_df, cnx, db_out_flag)
    fsm.start(earliest_date=configs['TripAdvisor']['earliest_date'],
              number_of_pages=configs['TripAdvisor']['number_of_pages'],
              trip_types = ['Family', 'Couples', 'Solo', 'Business', 'Friends']
              )
    end_time = time.time()
    print('Total time taken (min): ' + str(round((end_time - start_time)/60, 2)))
