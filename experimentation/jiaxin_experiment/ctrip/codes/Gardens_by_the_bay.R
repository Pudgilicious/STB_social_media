library(ggplot2)
library(dplyr)
df_raw <- read.csv("Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/Baidu_API/2.csv")

#number of reviews by month
df <-df_raw[order(df_raw$REVIEW_DATE,df_raw$REVIEW_TIME),]
df$Yr_month=format(as.Date(df$REVIEW_DATE), "%Y-%m")

overall <-(ggplot(df %>% select("Yr_month"),aes(Yr_month))+
           geom_bar(fill='cadetblue3')+
           geom_text(stat='count',aes(label=..count..),vjust=-0.5)+
           theme(axis.text.x = element_text(angle = 45, hjust = 1))+
           ggtitle("review numbers"))
#generally a increasing trend

  
#facet plot of number of reviews
df$by_Yr=format(as.Date(df$REVIEW_DATE), "%Y")
df$by_mth= factor(months(as.POSIXlt(df$REVIEW_DATE, format="%Y-%m-%d")),
                  levels=c("January","February","March","April","May","June","July",
                           "August","September","October","November","December"))
by_Year <- ggplot(df, aes(x=by_mth)) + 
           geom_bar(fill='cadetblue3')+
           geom_text(stat='count',aes(label=..count..),vjust=-0.1)+
           theme(axis.text.x = element_text(angle = 45, hjust = 1))+
           facet_grid(by_Yr~.)
#significant increase in the august 