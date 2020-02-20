#Note
#first recognise the language 
#Then googe translate the langauge. Or subset out first

library("textcat")

setwd("C:/Users/huangj/Desktop/items/Styles and climate verbatim research/raw_dat")

dat = read.csv("20171206_ALLCommentsSC2.csv")
dat$language = textcat(dat$X1)

#Save the data with the language column 
# write.csv(dat,"20170129_include_language_ALLCommentsSC2.csv",row.names = F)
