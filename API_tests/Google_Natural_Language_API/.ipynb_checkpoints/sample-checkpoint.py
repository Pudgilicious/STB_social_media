#!/usr/bin/env python

# export GOOGLE_APPLICATION_CREDENTIALS="/home/zyf0717/git_environment/STB_social_media_analytics/API_tests/Google_Natural_Language_API/My First Project-5552e8a7402c.json"

def run_quickstart():
    # [START language_quickstart]
    # Imports the Google Cloud client library
    # [START language_python_migration_imports]
    from google.cloud import language_v1
    from google.cloud.language import enums
    from google.cloud.language import types
    # [END language_python_migration_imports]

    client = language_v1.LanguageServiceClient()

    text = 'What a unique experience. This place is definitely out of this world, one of a kind. Worth a visit. There are a lot of attractions that are probably worth buying the combination passes. We bought a ticket to one attraction which was over quickly and not totally worth the money.'

    document = language_v1.types.Document(
        content=text,
        type='PLAIN_TEXT',
    )

    response = client.analyze_entity_sentiment(document=document,
        encoding_type='UTF32',
    )

    entities = response.entities
    print(entities[0].name)
    print(entities[0].sentiment.magnitude)
    print(entities[0].sentiment.score)

if __name__ == '__main__':
    run_quickstart()