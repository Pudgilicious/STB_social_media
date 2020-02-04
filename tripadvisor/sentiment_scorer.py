import pandas as pd
import traceback
import yaml

from datetime import datetime
from pandas.io.json import json_normalize
from time import sleep

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

##### TO BE DONE IN FSM #####
target_folder = configs['TripAdvisor']['target_folder']
api_key = configs['General']['api_key']

authenticator = IAMAuthenticator(api_key)  # API key
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(
    'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12')
#############################

class SentimentScorer:
    keywords_col_names = ['WEBSITE_ID', 'REVIEW_ID', 'TEXT', 'RELEVANCE',
                          'COUNT', 'SENTIMENT_SCORE', 'SENTIMENT_LABEL',
                          'SADNESS', 'JOY', 'FEAR', 'DISGUST', 'ANGER',
                          'MIXED_SENTIMENT']

    entities_col_names = ['WEBSITE_ID', 'REVIEW_ID', 'TYPE', 'TEXT',
                          'RELEVANCE', 'COUNT', 'CONFIDENCE', 'SENTIMENT_SCORE',
                          'SENTIMENT_LABEL', 'SADNESS', 'JOY', 'FEAR',
                          'DISGUST', 'ANGER', 'MIXED_SENTIMENT',
                          'DISAMBIGUATION_SUBTYPE', 'DISAMBIGUATION_NAME',
                          'DISAMBIGUATION_RESOURCE']

    keywords_col_names_map = {
        'text': 'TEXT',
        'relevance': 'RELEVANCE',
        'count': 'COUNT',
        'sentiment.score': 'SENTIMENT_SCORE',
        'sentiment.label': 'SENTIMENT_LABEL',
        'emotion.sadness': 'SADNESS',
        'emotion.joy': 'JOY',
        'emotion.fear': 'FEAR',
        'emotion.disgust': 'DISGUST',
        'emotion.anger': 'ANGER',
        'sentiment.mixed': 'MIXED_SENTIMENT'
    }

    entities_col_names_map = {
        'type': 'TYPE',
        'text': 'TEXT',
        'relevance': 'RELEVANCE',
        'count': 'COUNT',
        'confidence': 'CONFIDENCE',
        'sentiment.score': 'SENTIMENT_SCORE',
        'sentiment.label': 'SENTIMENT_LABEL',
        'emotion.sadness': 'SADNESS',
        'emotion.joy': 'JOY',
        'emotion.fear': 'FEAR',
        'emotion.disgust': 'DISGUST',
        'emotion.anger': 'ANGER',
        'sentiment.mixed': 'MIXED_SENTIMENT',
        'disambiguation.subtype': 'DISAMBIGUATION_SUBTYPE',
        'disambiguation.name': 'DISAMBIGUATION_NAME',
        'disambiguation.dbpedia_resource': 'DISAMBIGUATION_RESOURCE'
    }

    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')


if __name__=="__sentiment_scorer__":
    pass
