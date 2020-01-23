#https://github.com/IBM/watson-discovery-food-reviews

import json
import yaml
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, RelationsOptions
import pandas as pd
from pandas.io.json import json_normalize

with open('api_keys.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

authenticator = IAMAuthenticator(configs['General']['IBM_API_KEY'])

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/d5942ac7-d99a-47e7-a91c-81fe338491c0')

#text = "Zico 33.8 Ounce tastes so good, crisp and pure. It tastes way better than vitacoco which has an odd after taste. My packs were fresh with an expiration of 9 months after I ordered. Shipping was super fast and absolutely no damage to the containers. You have to try out how delicious this brand is!"
text = "Great product . Thanks. These have a wonderful flavor when you brew a cup of coffee. I like getting K-Cups from Amazon and trying new flavors"


#response_entity = natural_language_understanding.analyze(
#                text = text,
#                features=Features(entities=EntitiesOptions(model="2909beba-d2a9-4dca-9ae2-e6808abd9843"))).get_result()

response_entity = natural_language_understanding.analyze(
                  text=text,
                  features=Features(entities=EntitiesOptions(model="2909beba-d2a9-4dca-9ae2-e6808abd9843", \
                                                             emotion=True, sentiment=True, limit=100000), \
                                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=100000))).get_result()



response_relation = natural_language_understanding.analyze(
                    text=text,
                    features=Features(relations=RelationsOptions(model='2909beba-d2a9-4dca-9ae2-e6808abd9843'))).get_result()

#response_relation = natural_language_understanding.analyze(
#                  text=text,
#                  features=Features(relations=RelationsOptions(model="2909beba-d2a9-4dca-9ae2-e6808abd9843", \
#                                                             emotion=True, sentiment=True, limit=100000), \
#                                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=100000))).get_result()




print(json.dumps(response_entity, indent=2))
print(json.dumps(response_relation, indent=2))