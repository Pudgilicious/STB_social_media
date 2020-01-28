import pandas as pd
import mysql.connector
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
                 58]
    poi_name = [#'Singapore Botanic Gardens',
                #'Singapore Zoo',
                #'Singapore Flyer',
                'Night Safari'
               ]
    poi_url = [#'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d310900-Reviews-Singapore_Botanic_Gardens-Singapore.html',
               #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html',
               #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d678639-Reviews-Singapore_Flyer-Singapore.html',
               'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324761-Reviews-Night_Safari-Singapore.html'
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
    fsm = TripAdvisorFSM(chromedriver_path, poi_df, cnx, db_out_flag)
    fsm.start()
    print('Total time taken (min): ' + str(round((fsm.end_time - fsm.start_time)/60, 2)))
