import pandas as pd
import mysql.connector
import time
import yaml

from tripadvisor_fsm import TripAdvisorFSM

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

chromedriver_path = configs['General']['chromedriver_path']
csv_input_path = configs['TripAdvisor']['csv_input_path']

db_in_flag = configs['TripAdvisor']['read_from_database']
db_out_flag = configs['TripAdvisor']['write_to_database']

if db_in_flag == 'csv':
    poi_df = pd.read_csv(csv_input_path)
    poi_df['URL'] = poi_df['URL'].apply(lambda x: 'https://tripadvisor.com.sg' + x)
    poi_df = poi_df[69:]
    # poi_df = poi_df.iloc[[12, 23],]

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
