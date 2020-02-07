import yaml
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from time import sleep

from sentiment_scorer import SentimentScorer

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

with open('api_keys.yml') as file:
    api_keys = yaml.load(file, Loader=yaml.FullLoader)['API_Keys']

# Amend the following 3 variables to continue from previous API calls.
target_folder = '200126_094431'
continue_in_folder = None
continue_from_poi_index = None
continue_from_index = None


class SentimentScorerFSM:
    def __init__(self):
        self.sentiment_scorer = SentimentScorer(
            target_folder=target_folder,
            continue_in_folder=continue_in_folder,
            continue_from_poi_index=continue_from_poi_index,
            continue_from_index=continue_from_index)
        self.authenticator = None
        self.nlu = None
        self.api_key_index = None

    def initialise_nlu(self):
        self.authenticator = IAMAuthenticator(api_keys[self.api_key_index])
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2019-07-12',
            authenticator=self.authenticator
        )
        self.nlu.set_service_url(
            'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12')

    def start(self):
        self.api_key_index = 2
        while self.sentiment_scorer.fsm_state != 4:
            self.initialise_nlu()
            self.sentiment_scorer.score_sentiments(self.nlu)
            if self.sentiment_scorer.fsm_state == 2:
                self.api_key_index += 1
                print('#######################################')
                print('FSM state is 2, sleeping for 5 seconds.')
                print('#######################################')
                sleep(5)
            if self.sentiment_scorer.fsm_state == 3:
                print('#######################################')
                print('FSM state is 3, sleeping for 5 seconds.')
                print('#######################################')
                sleep(5)
                continue


fsm = SentimentScorerFSM()
fsm.start()