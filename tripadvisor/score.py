import yaml
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from time import sleep

from sentiment_scorer import SentimentScorer

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

with open('api_keys.yml') as file:
    api_keys = yaml.load(file, Loader=yaml.FullLoader)['API_Keys']

target_folder = '200126_094431'
target_folder = configs['TripAdvisor']['target_folder']


class SentimentScorerFSM:
    def __init__(self, target_folder):
        self.sentiment_scorer = SentimentScorer(target_folder)
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
        self.api_key_index = 0
        while self.sentiment_scorer.fsm_state != 4:
            self.initialise_nlu()
            self.sentiment_scorer.score_sentiments(self.nlu)
            if self.sentiment_scorer.fsm_state == 2:
                self.api_key_index += 1
                print('\nFSM state is 2, sleeping for 2 seconds.\n')
                sleep(2)
            if self.sentiment_scorer.fsm_state == 3:
                print('\nFSM state is 3, sleeping for 2 seconds.\n')
                sleep(2)
                continue


fsm = SentimentScorerFSM(target_folder)
fsm.start()