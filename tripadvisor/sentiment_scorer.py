import pandas as pd
import traceback
import os
from datetime import datetime
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

    def __init__(
            self,
            target_folder,
            continue_in_folder=None,
            continue_from_poi_index=None,
            continue_from_row_index=None
    ):
        # To continue from previous calls
        self.target_folder = target_folder
        self.continue_in_folder = continue_in_folder
        self.continue_from_poi_index = continue_from_poi_index
        self.continue_from_row_index = continue_from_row_index

        # Set up directories
        self.csv_list = os.listdir('./tripadvisor/finalised_output/{}/reviews'.format(target_folder))

        # Read list of POIs to score from target folder
        self.poi_list = sorted([int(i[:i.find('.csv')]) for i in self.csv_list])  # List of POI indexes from file names

        # Creating empty dataframes to store scores
        self.keywords_col_names_df = pd.DataFrame(columns=self.keywords_col_names)
        self.entities_col_names_df = pd.DataFrame(columns=self.entities_col_names)

        # Create output directory
        if self.continue_in_folder is None:
            self.sentiment_folder_path = './tripadvisor/finalised_output/{}/sentiments_{}/'.format(
                self.target_folder,
                datetime.now().strftime('%y%m%d_%H%M%S')
            )
            os.makedirs(self.sentiment_folder_path)
        else:
            self.sentiment_folder_path = './tripadvisor/finalised_output/{}/sentiments_{}/'.format(
                self.target_folder,
                self.continue_in_folder
            )

        # To continue from certain POI index
        if self.continue_from_poi_index is not None:
            self.poi_list = self.poi_list[self.poi_list.index(self.continue_from_poi_index):]

        self.nlu = None
        self.api_calls_made = 0
        self.fsm_state = 0

        # Per-POI variables, reset after every POI
        self.datetime_string = None
        self.current_poi_index = None
        self.current_reviews_df = None
        self.keywords_file_path = None
        self.entities_file_path = None
        self.current_row_index = None

        # Per-review variables, reset after every API call
        self.current_df_row = None
        self.current_review_id = None
        self.current_review_text = None
        self.current_api_response = None
        self.keywords_df = None
        self.entities_df = None

    # Score reviews in target folder
    def score_sentiments(self, nlu):
        self.nlu = nlu
        while self.poi_list or self.current_poi_index is not None:

            # Only create the below if FSM state is not 2 or 3
            if self.fsm_state not in (2, 3):
                self.datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')
                self.current_poi_index = self.poi_list.pop(0)
                self.keywords_file_path = self.sentiment_folder_path + '{}_keywords_{}.csv'.format(
                    self.current_poi_index,
                    self.datetime_string
                )
                self.entities_file_path = self.sentiment_folder_path + '{}_entities_{}.csv'.format(
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

            # End function if error has occurred, preserving per-POI variables
            if self.fsm_state in (2, 3):
                return

            # Reset per-POI variables
            self.reset_per_poi_variables()

        self.fsm_state = 4
        print("Scoring complete.")

    def score_sentiments_1_poi(self):
        if self.current_reviews_df is None:
            self.current_reviews_df = pd.read_csv(
                './tripadvisor/finalised_output/{}/reviews/{}.csv'.format(
                    self.target_folder,
                    self.current_poi_index
                )
            )

        # To continue from certain row index
        if self.continue_from_row_index is not None:
            self.current_row_index = self.continue_from_row_index
            self.continue_from_row_index = None  # Need to reset
        elif self.current_row_index is None:
            self.current_row_index = 0

        # To allow starting from certain row index
        if self.fsm_state not in (2, 3):
            self.current_reviews_df = self.current_reviews_df.iloc[self.current_row_index:]

        # FSM state 1 is the normal running mode
        self.fsm_state = 1

        while len(self.current_reviews_df.index) > 0:
            self.current_df_row = self.current_reviews_df.iloc[0]
            self.current_review_id = self.current_df_row['REVIEW_ID']
            self.current_review_text = self.current_df_row['REVIEW_BODY']
            self.api_calls_made += 1
            print('API calls made: {}, POI index: {}, review ID: {}, row index: {}'.format(
                self.api_calls_made,
                self.current_poi_index,
                self.current_review_id,
                self.current_row_index
            ))

            try:
                self.get_api_response()
            except Exception as e:
                print('Error in API call. Please see log file.')
                log = open(self.sentiment_folder_path + 'log.txt', 'a+')
                log.write('Error in API call.\n')
                log.write('POI index: {}, review ID: {}, row index: {}, time: {}\n'.format(
                    self.current_poi_index,
                    self.current_review_id,
                    self.current_row_index,
                    datetime.now()))
                log.write(traceback.format_exc() + '\n')
                log.close()

                # Unsupported text language case
                if str(e).find('unsupported text language') != -1:
                    self.reset_per_review_variables()
                    self.current_reviews_df = self.current_reviews_df.iloc[1:]
                    self.current_row_index += 1
                    continue

                # API call limit reached case
                elif str(e).find('Forbidden') != -1:
                    self.fsm_state = 2
                    return  # Per-review variables preserved.

                # Any other case
                else:
                    self.fsm_state = 3
                    return  # Per-review variables preserved.

            try:
                self.parse_response()
                self.write_to_csv()
            except Exception as e:
                print('Error in parsing API response or writing to CSV. Please see log file.')
                log = open(self.sentiment_folder_path + 'log.txt', 'a+')
                log.write('Error in parsing API response or writing to CSV.\n')
                log.write('POI index: {}, review ID: {}, row index: {}, time: {}\n'.format(
                    self.current_poi_index,
                    self.current_review_id,
                    self.current_row_index,
                    datetime.now()))
                log.write(traceback.format_exc() + '\n')
                log.close()
                self.fsm_state = 3
                return  # Per-review variables preserved.

            # Reset per-review variables
            self.reset_per_review_variables()

            # Drop first row of reviews_df
            self.current_reviews_df = self.current_reviews_df.iloc[1:]
            self.current_row_index += 1

    def get_api_response(self):
        self.current_api_response = self.nlu.analyze(
            text=self.current_review_text,
            features=Features(
                entities=EntitiesOptions(emotion=True, sentiment=True, limit=10000),
                keywords=KeywordsOptions(emotion=True, sentiment=True, limit=10000)
            )
        ).get_result()

    def parse_response(self):
        # In case 'keywords' not in api response
        if 'keywords' in self.current_api_response.keys():
            self.keywords_df = json_normalize(self.current_api_response['keywords'])\
                .rename(columns=self.keywords_col_names_map)
            self.keywords_df.insert(0, 'REVIEW_ID', self.current_review_id)
            self.keywords_df.insert(0, 'WEBSITE_ID', 1)
            self.keywords_df = self.keywords_col_names_df.append(self.keywords_df, sort=False)

        # In case 'entities' not in api response
        if 'entities' in self.current_api_response.keys():
            self.entities_df = json_normalize(self.current_api_response['entities'])\
                .rename(columns=self.entities_col_names_map)
            if self.entities_df.shape[1] != 0:
                self.entities_df.insert(0, 'REVIEW_ID', self.current_review_id)
                self.entities_df.insert(0, 'WEBSITE_ID', 1)
                self.entities_df = self.entities_col_names_df.append(self.entities_df, sort=False)

    def write_to_csv(self):
        self.keywords_df.to_csv(
            self.keywords_file_path,
            mode='a',
            header=False,
            index=False
        )
        if self.entities_df is None or self.entities_df.shape[1] == 0:
            return
        else:
            self.entities_df.to_csv(
                self.entities_file_path,
                mode='a',
                header=False,
                index=False
            )

    def reset_per_poi_variables(self):
        self.datetime_string = None
        self.current_poi_index = None
        self.current_reviews_df = None
        self.keywords_file_path = None
        self.entities_file_path = None
        self.current_row_index = None

    def reset_per_review_variables(self):
        self.current_df_row = None
        self.current_review_id = None
        self.current_review_text = None
        self.current_api_response = None
        self.keywords_df = None
        self.entities_df = None