library(readxl)
library(ggplot2)
library(dplyr)
#read in data
Ali_Data<- read_excel("Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/Baidu_API/STB_Ali.xls")
Baidu_Data<- read.csv("Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/Baidu_API/sentiment.csv",header=T,na.string=c(""))
Ali_Data[is.na(Ali_Data)] <- 0

#unique aspects of each API for availiable 1000 reviews
Baidu_Aspects <- length(unique(Baidu_Data$aspect)) 
Ali_Aspects <- length(unique(Ali_Data$Aspect))

#number of unique aspects that reflects POS,NEG,NEU
B_pos_uni <- length(unique((Baidu_Data[Baidu_Data$sentiment== 'POS',])$aspect))
A_pos_uni <- length(unique((Ali_Data[Ali_Data$Polarity== 'POS',])$Aspect))
B_neg_uni <- length(unique((Baidu_Data[Baidu_Data$sentiment== 'NEG',])$aspect))
A_neg_uni <- length(unique((Ali_Data[Ali_Data$Polarity== 'NEG',])$Aspect))
B_neu_uni <- length(unique((Baidu_Data[Baidu_Data$sentiment== 'NEU',])$aspect))
A_neu_uni <- length(unique((Ali_Data[Ali_Data$Polarity== 'NEU',])$Aspect))

#percentage of aspects that reflects POS,NEG,NEU
B_pos <- (length((Baidu_Data[Baidu_Data$sentiment== 'POS',])$aspect)) / (length(Baidu_Data$aspect))
A_pos <- (length((Ali_Data[Ali_Data$Polarity== 'POS',])$Aspect)) / (length(Ali_Data[Ali_Data$Polarity != 0,]$Aspect))
B_neg <- (length((Baidu_Data[Baidu_Data$sentiment== 'NEG',])$aspect)) / (length(Baidu_Data$aspect))
A_neg <- (length((Ali_Data[Ali_Data$Polarity== 'NEG',])$Aspect)) / (length(Ali_Data[Ali_Data$Polarity != 0,]$Aspect))
B_neu <- (length((Baidu_Data[Baidu_Data$sentiment== 'NEU',])$aspect)) / (length(Baidu_Data$aspect))
A_neu <- (length((Ali_Data[Ali_Data$Polarity== 'NEU',])$Aspect)) / (length(Ali_Data[Ali_Data$Polarity != 0,]$Aspect))

#bar chart for Ali Aspects
(ggplot(Ali_Data[Ali_Data[,'Polarity'] != 0,],aes(Polarity))+
    geom_bar()+
    geom_text(stat='count',aes(label=..count..),vjust=-0.5)+
    scale_x_discrete(limits = c("POS", "NEU", "NEG"))+
    ggtitle("Ali Data Aspect"))
#bar chart for Baidu Aspects
(ggplot(Baidu_Data %>% select('sentiment','aspect'),aes(sentiment))+
    geom_bar()+
    scale_x_discrete(limits = c("POS", "NEU", "NEG"))+
    geom_text(stat='count',aes(label=..count..),vjust=-0.5)+
    ggtitle("Baidu Data Aspect"))