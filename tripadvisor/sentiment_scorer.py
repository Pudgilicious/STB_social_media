import pandas as pd
from datetime import datetime
from pandas.io.json import json_normalize

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# Setup the API caller
authenticator = IAMAuthenticator('bkC6hyTVS4qonY34vS0d8Q5F2YY4Kz9m0fyj1cN-5VFw')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(
    'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12')

# Open CSV containing reviews to score
folder_name = '200125_142611'
poi_index = 1
reviews_df = pd.read_csv('./tripadvisor/finalised_output/{}/reviews/{}.csv'.format(folder_name, poi_index))
row_number = 2776
reviews_df = reviews_df.iloc[row_number:]

# Create CSVs
datetime_string = datetime.now().strftime('%y%m%d_%H%M%S')

keywords_file_path = './tripadvisor/finalised_output/{}/reviews/{}_keywords_{}.csv'.format(
    folder_name,
    poi_index,
    datetime_string
)
keywords_col_names = ['WEBSITE_ID', 'REVIEW_ID', 'TEXT', 'RELEVANCE', 'COUNT',
                     'SENTIMENT_SCORE', 'SENTIMENT_LABEL', 'SADNESS', 'JOY',
                     'FEAR', 'DISGUST', 'ANGER', 'MIXED_SENTIMENT']
keywords_col_names_df = pd.DataFrame(columns=keywords_col_names)
keywords_col_names_df.to_csv(
    keywords_file_path,
    mode='a',
    index=False
)

entities_file_path = './tripadvisor/finalised_output/{}/reviews/{}_entities_{}.csv'.format(
    folder_name,
    poi_index,
    datetime_string
)
entities_col_names = ['WEBSITE_ID', 'REVIEW_ID', 'TYPE', 'TEXT', 'RELEVANCE',
                      'COUNT', 'CONFIDENCE', 'SENTIMENT_SCORE',
                      'SENTIMENT_LABEL', 'SADNESS', 'JOY', 'FEAR', 'DISGUST',
                      'ANGER', 'MIXED_SENTIMENT', 'DISAMBIGUATION_SUBTYPE',
                      'DISAMBIGUATION_NAME', 'DISAMBIGUATION_RESOURCE']
entities_col_names_df = pd.DataFrame(columns=entities_col_names)
entities_col_names_df.to_csv(
    entities_file_path,
    mode='a',
    index=False
)

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

# Making the API calls
while len(reviews_df.index) > 0:
    text = reviews_df.iloc[0][8]
    print('Row number: {}'.format(row_number))
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=1000),
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=1000)
        )
    ).get_result()

    keywords_df = json_normalize(response['keywords']).rename(columns=keywords_col_names_map)
    keywords_df.insert(0, 'REVIEW_ID', reviews_df.iloc[0][4])
    keywords_df.insert(0, 'WEBSITE_ID', 1)
    keywords_df = keywords_col_names_df.append(keywords_df, sort=False)
    """
    # Ensure consistent number of columns for sorting
    if 'MIXED_SENTIMENT' not in keywords_df.columns.values:
        keywords_df['MIXED_SENTIMENT'] = None

    # Sort columns
    keywords_df = keywords_df[keywords_col_names]
    """
    keywords_df.to_csv(
        keywords_file_path,
        mode='a',
        header=False,
        index=False
    )

    if 'entities' in response.keys():
        entities_df = json_normalize(response['entities']).rename(columns=entities_col_names_map)
        if entities_df.shape[1] != 0:
            entities_df.insert(0, 'REVIEW_ID', reviews_df.iloc[0][4])
            entities_df.insert(0, 'WEBSITE_ID', 1)
            entities_df = entities_col_names_df.append(entities_df, sort=False)
            """
            # Ensure consistent number of columns for sorting
            if 'MIXED_SENTIMENT' not in entities_df.columns.values:
                entities_df['MIXED_SENTIMENT'] = None
            if 'DISAMBIGUATION_SUBTYPE' not in entities_df.columns.values:
                entities_df['DISAMBIGUATION_SUBTYPE'] = None
            if 'DISAMBIGUATION_NAME' not in entities_df.columns.values:
                entities_df['DISAMBIGUATION_NAME'] = None
            if 'DISAMBIGUATION_RESOURCE' not in entities_df.columns.values:
                entities_df['DISAMBIGUATION_RESOURCE'] = None
    
            # Sort columns
            entities_df = entities_df[entities_col_names]
            """
            entities_df.to_csv(
                entities_file_path,
                mode='a',
                header=False,
                index=False
            )

    reviews_df = reviews_df.iloc[1:]
    row_number += 1

