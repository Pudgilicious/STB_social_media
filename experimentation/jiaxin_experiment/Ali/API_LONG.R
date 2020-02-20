df_raw <- read.csv("~/Desktop/git/STB_social_media_analytics/experimentation/jiaxin_experiment/Ali/200218_090222_sentiment.csv")
summary(df_raw)

#remove invalid API outputs
df <- df_raw[(df_raw$OVERALL == "POS"|
              df_raw$OVERALL == "NEG"|
              df_raw$OVERALL == "NEU"),]

#make all entries string, to turn into list
a <- as.character(df$ASPECTS)
b <- as.character(df$ASPECTS_POLARITIES)

#obtain li_asp: a list containing lists, each list elemnt is the aspects of a review
c <- list()
for (i in 1:length(a)){
  c[i] <- strsplit(a[i],'","')
}

li_asp <- list()
len <- list()
for (i in 1:length(c)){
  li1 <- list()
  for (j in 1:length(c[[i]])){
    li1[j] = str_replace_all(c[[i]][j],"[[:punct:]]","")
  }
  li_asp[[i]]=li1
  len [[i]] = length(li1)
}


#obtain li_pol: a list containing lists, each list element is the polarities of a review
#exactly same length with the li_asp
c <- list()
for (i in 1:length(b)){
  c[i] = strsplit(b[i],'","')
}
li_pol <- list()
for (i in 1:length(c)){
  li1 <- list()
  for (j in 1:length(c[[i]])){
    li1[j] = str_replace_all(c[[i]][j],"[[:punct:]]","")
  }
  li_pol[[i]]=li1
}

#put back to df, delete the rows with empty API output
df$ASPECTS <- li_asp
df$ASPECTS_POLARITIES <- li_pol
