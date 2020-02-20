#Use this an exercise to implement the whole text mining proceduren from this book -->https://www.tidytextmining.com/tidytext.html
#Use this script to analyze the text data
#First subset the data by English 
#Separate into Strengths and Weakenesses
#Eventually try to use the verbal to predict something
#Clean the corpus


library(tidytext)
library(tidyr)

setwd("C:/Users/huangj/Desktop/items/Styles and climate verbatim research")

#read in the dataset
dat = read.csv("./raw_dat/20170129_include_language_ALLCommentsSC2.csv",stringsAsFactors = F)
names(dat) = c("GroupID","PerID","UserName","Version", "Assessor","Strengths","Weakensses","language")


#subset data by english
dat = subset(dat,dat$language == "english")

#As POC subset out GroupID and Strengths
dat = subset(dat,select = c("GroupID","PerID","UserName","Strengths"))

#Arrnge by unigram
dat_tokens = dat %>%
  unnest_tokens(ngram, Strengths, token = "ngrams", n = 1)

names(dat_tokens)[4] = "word"

#Remove stop words
data(stop_words)

dat_tokens <- dat_tokens %>%
  anti_join(stop_words)

#Count the most common words
dat_tokens %>%
  count(word, sort = TRUE) 







