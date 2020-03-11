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
API_options = configs['TripAdvisor']['API_options']
# Initialize FSM object
fsm = IBMSentimentScorerFSM(
    website_name='tripadvisor',
    website_id=1,
    target_folder=target_folder,
    continue_in_folder=continue_in_folder,
    continue_from_poi_index=continue_from_poi_index,
    continue_from_row_index=continue_from_row_index,
    API_options=API_options
)

# Start API calls
fsm.start()
