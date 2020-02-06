import yaml
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from sentiment_scorer import SentimentScorer

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

with open('./tripadvisor/IBM_api_keys.yml') as file:
    api_keys = yaml.load(file, Loader=yaml.FullLoader)

target_folder = configs['TripAdvisor']['target_folder']


class SentimentScorerFSM:
    def __init__(self, target_folder):
        self.sentiment_scorer = SentimentScorer(target_folder)
        self.authenticator = None
        self.nlu = None

    def initialise_nlu(self):
        self.authenticator = IAMAuthenticator(api_keys[0])
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2019-07-12',
            authenticator=self.authenticator
        )
        self.nlu.set_service_url(
            'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12')

    def start(self):
        self.initialise_nlu()
        self.sentiment_scorer.score_sentiments(nlu)


if __name__=="__score__":
    fsm = SentimentScorerFSM(target_folder)
    fsm.start()