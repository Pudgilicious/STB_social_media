#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:46:18 2020

@author: jirong
"""
#https://www.pyimagesearch.com/2019/01/30/ubuntu-18-04-install-tensorflow-and-keras-for-deep-learning/
# NLTK
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.preprocessing import LabelEncoder
#nltk.download('stopwords')

#Spacy
import spacy
nlp = spacy.load("en_core_web_sm")    #python -m spacy download en_core_web_sm -->https://stackoverflow.com/questions/47295316/importerror-no-module-named-spacy-en

# Other
import re
import json
import string
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

#Keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical

#load data
import pandas as pd
reviews_train = pd.read_csv("./experimentation/jirong_experiment/food_reviews/ABSA16_Restaurants_Train_SB1_v2.csv")
reviews_train = reviews_train.drop(['OutOfScope'], axis=1)

#rename the header of dataframe
reviews_train = reviews_train.rename(columns={ "Index": "Index", 
                                               "rid": "rid", 
                                               "id": "id", 
                                               "text": "review", 
                                               "target": "aspect", 
                                               "category": "aspect_category", 
                                               "polarity": "sentiment", 
                                               "from": "from", 
                                               "to": "to"})

#show first 5 records
reviews_train.head()

#Fill previous empty row
reviews_train = reviews_train.fillna(method='ffill')

# reviews_train.columns
print(reviews_train.groupby('aspect_category').size().sort_values(ascending=False))

#how many categories
print("number of categories",reviews_train.aspect_category.nunique())

absa_model = Sequential()
absa_model.add(Dense(512, input_shape=(6000,), activation='relu'))
absa_model.add((Dense(256, activation='relu')))
absa_model.add((Dense(128, activation='relu')))
absa_model.add(Dense(12, activation='softmax'))  #absa_model.add(Dense(13, activation='softmax')). Num of categories
#compile model
absa_model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

vocab_size = 6000 # We set a maximum size for the vocabulary
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(reviews_train.review)
reviews_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(reviews_train.review))

label_encoder1 = LabelEncoder()
integer_category = label_encoder1.fit_transform(reviews_train.aspect_category)
one_hot_labels_aspect = to_categorical(integer_category)

#model architecture
sentiment_model = Sequential()
sentiment_model.add(Dense(512, input_shape=(6000,), activation='relu'))
sentiment_model.add((Dense(256, activation='relu')))
sentiment_model.add((Dense(128, activation='relu')))
sentiment_model.add(Dense(3, activation='softmax'))
#compile model
sentiment_model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

#create a word embedding of reviews data
vocab_size = 6000 # We set a maximum size for the vocabulary
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(reviews_train.review)
reviews_tokenized = pd.DataFrame(tokenizer.texts_to_matrix(reviews_train.review))

#encode the label variable
label_encoder2 = LabelEncoder()
integer_sentiment = label_encoder2.fit_transform(reviews_train.sentiment)
one_hot_labels_sentiment = to_categorical(integer_sentiment)


# For a single-input model with 2 classes (binary classification):
model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])



# For a single-input model with 10 classes (categorical classification):
#model = Sequential()
#model.add(Dense(32, activation='relu', input_dim=100))
#model.add(Dense(10, activation='softmax'))
#model.compile(optimizer='rmsprop',
#              loss='categorical_crossentropy',
#              metrics=['accuracy'])

# Generate dummy data
#import numpy as np
#data = np.random.random((1000, 100))
#labels = np.random.randint(10, size=(1000, 1))

# Convert labels to categorical one-hot encoding
#one_hot_labels = to_categorical(labels, num_classes=10)

# Train the model, iterating on the data in batches of 32 samples
#model.fit(data, one_hot_labels, epochs=10, batch_size=32)



#fit aspect classifier
absa_model.fit(reviews_tokenized, one_hot_labels_aspect, epochs=100, verbose=1)
#fit sentiment classifier-->This works
sentiment_model.fit(reviews_tokenized, one_hot_labels_sentiment, epochs=100, verbose=1)

test_reviews = [
    "Good, fast service.",
    "The hostess was very pleasant.",
    "The bread was stale, the salad was overpriced and empty.",
    "The food we ordered was excellent, although I wouldn't say the margaritas were anything to write home about.",
    "This place has totally weird decor, stairs going up with mirrored walls - I am surprised how no one yet broke their head or fall off the stairs"
]

# Aspect preprocessing
test_reviews = [review.lower() for review in test_reviews]
test_aspect_terms = []
for review in nlp.pipe(test_reviews):
    chunks = [(chunk.root.text) for chunk in review.noun_chunks if chunk.root.pos_ == 'NOUN']
    test_aspect_terms.append(' '.join(chunks))
test_aspect_terms = pd.DataFrame(tokenizer.texts_to_matrix(test_aspect_terms))
                             
# Sentiment preprocessing
test_sentiment_terms = []
for review in nlp.pipe(test_reviews):
        if review.is_parsed:
            test_sentiment_terms.append(' '.join([token.lemma_ for token in review if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
        else:
            test_sentiment_terms.append('') 
test_sentiment_terms = pd.DataFrame(tokenizer.texts_to_matrix(test_sentiment_terms))

# Models output
test_aspect_categories = label_encoder1.inverse_transform(absa_model.predict_classes(test_aspect_terms))
test_sentiment = label_encoder2.inverse_transform(sentiment_model.predict_classes(test_sentiment_terms))
for i in range(5):
    print("Review " + str(i+1) + " is expressing a  " + test_sentiment[i] + " opinion about " + test_aspect_categories[i])
