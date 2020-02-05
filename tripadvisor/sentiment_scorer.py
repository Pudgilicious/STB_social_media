import pandas as pd
import traceback
from datetime import datetime
from os import listdir
from pandas.io.json import json_normalize
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


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
        self.csv_list = listdir('./finalised_output/{}/reviews'.format(target_folder))
        self.poi_list = sorted([int(i[:i.find('.csv')]) for i in self.csv_list])  # List of POI indexes from file names
        self.keywords_col_names_df = pd.DataFrame(columns=self.keywords_col_names)
        self.entities_col_names_df = pd.DataFrame(columns=self.entities_col_names)

        self.nlu = None
        self.fsm_state = 0

        # Fields below change for every POI
        self.datetime_string = None
        self.current_poi_index = None
        self.current_reviews_df = None
        self.keywords_file_path = None
        self.entities_file_path = None

        # Fields below reset for every review
        self.current_df_row = None
        self.current_row_number = None
        self.current_review_id = None
        self.current_review_text = None
        self.current_api_response = None
        self.keywords_df = None
        self.entities_df = None

    def score_sentiments(self, nlu):
        self.fsm_state = 1
        self.nlu = nlu
        while self.poi_list:
            self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
            self.current_poi_index = self.poi_list.pop(0)
            self.keywords_file_path = './tripadvisor/finalised_output/{}/reviews/{}_keywords_{}.csv'.format(
                self.target_folder,
                self.current_poi_index,
                self.datetime_string
            )
            self.entities_file_path = './tripadvisor/finalised_output/{}/reviews/{}_entities_{}.csv'.format(
                self.target_folder,
                self.current_poi_index,
                self.datetime_string
            )

            # Create empty CSVs with all headers
            keywords_col_names_df = pd.DataFrame(columns=self.keywords_col_names)
            keywords_col_names_df.to_csv(
                self.keywords_file_path,
                mode='a',
                index=False
            )
            entities_col_names_df = pd.DataFrame(columns=self.entities_col_names)
            entities_col_names_df.to_csv(
                self.entities_file_path,
                mode='a',
                index=False
            )

            # Scoring
            self.score_sentiments_1_poi()

    def score_sentiments_1_poi(self):
        self.current_reviews_df = pd.read_csv('./tripadvisor/finalised_output/{}/reviews/{}.csv'.format(
            self.target_folder,
            self.current_poi_index
        ))

        while len(self.current_reviews_df.index) > 0:
            self.current_df_row = self.current_reviews_df.iloc[0]
            self.current_review_id = self.current_df_row['REVIEW_ID']
            self.current_review_text = self.current_df_row['REVIEW_BODY']

            try:
                self.get_api_response()
            except:
                self.fsm_state = 2
                print("Error in API call. Please see log file.")
                log = open(
                    './tripadvisor/finalised_output/{}/reviews/log.txt'.format(self.target_folder),
                    'a+')
                log.write('POI index: {}, row number: {}, {}\n'.format(
                    self.current_poi_index,
                    self.current_row_number,
                    datetime.now()))
                log.write(traceback.format_exc() + '\n')
                log.close()

            try:
                self.parse_response()
            except:
                self.fsm_state = 3
                print("Error in parsing API response. Please see log file.")
                log = open(
                    './tripadvisor/finalised_output/{}/reviews/log.txt'.format(self.target_folder),
                    'a+')
                log.write('POI index: {}, row number: {}, {}\n'.format(
                    self.current_poi_index,
                    self.current_row_number,
                    datetime.now()))
                log.write(traceback.format_exc() + '\n')
                log.close()

            self.write_to_csv()
            self.current_df_row = None
            self.current_row_number = None
            self.current_review_id = None
            self.current_review_text = None
            self.current_api_response = None
            self.keywords_df = None
            self.entities_df = None
            self.current_reviews_df = self.current_reviews_df.iloc[1:]

    def get_api_response(self):
        self.current_api_response = self.nlu.analyze(
            text=self.current_review_text,
            features=Features(
                entities=EntitiesOptions(emotion=True, sentiment=True, limit=10000),
                keywords=KeywordsOptions(emotion=True, sentiment=True, limit=10000)
            )
        ).get_result()

    def parse_response(self):
        if 'keywords' in self.current_api_response.keys():
            self.keywords_df = json_normalize(self.current_api_response['keywords'])\
                .rename(columns=self.keywords_col_names_map)
            self.keywords_df.insert(0, 'REVIEW_ID', self.keywords_df.iloc[0]['REVIEW_ID'])
            self.keywords_df.insert(0, 'WEBSITE_ID', 1)
            self.keywords_df = self.keywords_col_names_df.append(self.keywords_df, sort=False)

        if 'entities' in self.current_api_response.keys():
            self.entities_df = json_normalize(self.current_api_response['entities'])\
                .rename(columns=self.entities_col_names_map)
            if self.entities_df.shape[1] != 0:
                self.entities_df.insert(0, 'REVIEW_ID', self.entities_df.iloc[0]['REVIEW_ID'])
                self.entities_df.insert(0, 'WEBSITE_ID', 1)
                self.entities_df = self.entities_col_names_df.append(self.entities_df, sort=False)

    def write_to_csv(self):
        self.keywords_df.to_csv(
            self.keywords_file_path,
            mode='a',
            header=False,
            index=False
        )
        self.entities_df.to_csv(
            self.entities_file_path,
            mode='a',
            header=False,
            index=False
        )
