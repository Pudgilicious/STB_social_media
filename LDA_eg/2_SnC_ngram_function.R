#Create a function to return a data frame. Looking at Strengths or Developmental areas  
#dat(ngrams)

library(tidytext)
library(tidyr)
library(dplyr)
library(stringr)
library(ggplot2)
library(tm)

#setwd("C:/Users/huangj/Desktop/items/Styles and climate verbatim research")
#include option to add stop words (as a list)?

if(Sys.info()[1] == "Linux"){
  setwd("/run/user/1000/gvfs/smb-share:server=sinspfs01,share=asia$/kfi_research_intranet/Styles and climate verbatim research")
}else{
  # setwd("O:/kfi_research_intranet/KF4D competencies analysis")
  setwd("C:/Users/huangj/Desktop/items/Styles and climate verbatim research")
}

dat_snc = function(ngram,StrOrWeak,lang){
  
#read in the dataset
dat = read.csv("20170129_include_language_ALLCommentsSC2.csv",stringsAsFactors = F)
names(dat) = c("GroupID","PerID","UserName","Version", "Assessor","Strengths","Areas_dev","language")

#subset data by english
dat = filter(dat,dat$language == lang)

# As POC subset out GroupID and Strengths/Weakness
if(StrOrWeak == "Strengths"){
  dat = subset(dat,select = c("GroupID","PerID","UserName","Strengths"))
  names(dat)[ncol(dat)] = "text"
}else if(StrOrWeak == "Areas_of_Development"){
  dat = subset(dat,select = c("GroupID","PerID","UserName","Areas_dev"))
  names(dat)[ncol(dat)] = "text"
}

#remove stopwords
dat$text = removeWords(dat$text,stopwords("en"))

#Further data munging to remove punctuation marks and numbers 
#regex for numbers or punctuations-->before unnest -->replace_reg = "[:punct:]|[:digit:]"
replace_reg = "[:punct:]|[:digit:]"
dat$text = str_replace_all(dat$text,replace_reg,"")

#removing stopwords, changed to lower here

#Arrnge by unigram
dat_tokens = dat %>%
  unnest_tokens(ngram, text, token = "ngrams", n = ngram)

names(dat_tokens)[4] = "word"

#merge in the stop words
dat_tokens = dat_tokens %>%
  anti_join(stop_words)  
  
#return a dataframe  
return(dat_tokens)
  
}


#Funnction values
ngram = 1
StrOrWeak = "Strengths"     #"Strengths","Areas_of_Development"
lang = "english"

a = dat_snc(ngram,StrOrWeak,lang)

a %>%
  count(word, sort = TRUE) %>%
  filter(n > 10000) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()




