import yaml
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from sentiment_scorer import SentimentScorer

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

authenticator = IAMAuthenticator(api_key)  # API key
nlu = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
nlu.set_service_url(
    'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12')


class SentimentScorerFSM:
    def __init__(self, target_folder):
        self.sentiment_scorer = SentimentScorer(target_folder)

    def start(self):
        self.sentiment_scorer.score_sentiments(nlu)