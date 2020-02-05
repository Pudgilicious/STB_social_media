#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:23:33 2020

@author: jirong
"""
#https://www.nltk.org/book/ch02.html
#https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
#https://stevenloria.com/wordnet-tutorial/
#https://medium.com/@adriensieg/text-similarities-da019229c894
#https://www.kaggle.com/antriksh5235/semantic-similarity-using-wordnet
#https://nlpforhackers.io/wordnet-sentence-similarity/

import nltk
from nltk.corpus import wordnet as wn
#from textblob import Word
word = Word("plant")

#nltk.download('wordnet')
wn.synsets('automobiles')
wn.synsets('automobile')

#Have to pick up first element
s = wn.synsets('flower')[1]
#s.hypernym_paths()   #How far to traverse up?
s.hyponyms

#Wordnet can only read 1 word at a time
s = wn.synsets('flower')[0]
s.hypernym_paths()
s.lemma_names

plant = word.synsets[1]
plant.lemma_names

#nltk.download('wordnet_ic')
from nltk.corpus import wordnet as wn
dog=wn.synsets('dog', pos=wn.NOUN)[0] #get the first noun synonym of the word "dog"
cat=wn.synsets('cat', pos=wn.NOUN)[0]
rose=wn.synsets('rose', pos=wn.NOUN)[0]
flower=wn.synsets('flower', pos=wn.NOUN)
flower=wn.synsets('flower', pos=wn.NOUN)[0]
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat') #load the brown corpus to compute the IC
rose.res_similarity(flower, brown_ic)
#6.0283161048744525
rose.res_similarity(dog, brown_ic)
#2.2241504712318556
cat.res_similarity(dog, brown_ic)
#7.911666509036577