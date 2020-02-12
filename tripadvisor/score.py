import sys
sys.path.append('./common_class_functions')

import yaml
from ibm_sentiment_scorer_fsm import IBMSentimentScorerFSM


with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

# Amend the corresponding variables in config_file.yml to continue from previous API calls.
target_folder = configs['TripAdvisor']['target_folder']
continue_in_folder = configs['TripAdvisor']['continue_in_folder']
continue_from_poi_index = configs['TripAdvisor']['continue_from_poi_index']
continue_from_row_index = configs['TripAdvisor']['continue_from_row_index']

# Initialize FSM object
fsm = IBMSentimentScorerFSM(
    site_name='tripadvisor',
    target_folder=target_folder,
    continue_in_folder=continue_in_folder,
    continue_from_poi_index=continue_from_poi_index,
    continue_from_row_index=continue_from_row_index
)

# Start API calls
fsm.start()