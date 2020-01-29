library(tidyverse)

df2 = read_csv("./20200117_chinese_ctrip_list.csv")
df2$X1 = 1:nrow(df2)
df2 = df2 %>%
        rename(., id = X1) %>%
        rename(., POI_chinese_name = POI)  

#de-deuplicate df2 first
df2 = df2[!duplicated(df2[c(2,3)]), ]
df2$id = 1:nrow(df2)
#df2 = read.table("./data/input/20200117_chinese_ctrip_list.csv", fileEncoding = "zh")
#To display chinese character
stringi::stri_trans_general(df2$POI_chinese_name, "zh")

df2_1 = read_csv("./20200117_eng_ctrip_list.csv")
df2_1 = df2_1[!duplicated(df2_1[c(2,3)]), ]
df2_1 = df2_1 %>%
          dplyr::rename(id_chinese = X1)
df2_1$id_chinese = 1:nrow(df2_1)
df2_1 = df2_1[-which(df2_1$id_chinese %in% c(862, 864)),]
df2_1$id_chinese = 1:nrow(df2_1)

df2 = df2 %>%
        left_join(., 
                (df2_1 %>%
                  dplyr::select(POI, link, id_chinese) %>%
                  dplyr::rename(POI_english_name = POI)), by = c("link" = "link")
        )


df2$num_reviews = gsub("[^0-9.-]", "", df2$num_reviews)
df2$num_reviews = as.numeric(df2$num_reviews)
df2 = df2[, -which(names(df2) == "id_chinese")]
df2$WEBSITE_INDEX = 2

names(df2) = c("POI_INDEX", "POI_CHINESE_NAME", "URL", "TOTAL_REVIEWS", "POI_NAME", "WEBSITE_INDEX")
filename = paste0(gsub("-","", Sys.Date()), "_TB_SOCIAL_CTRIP_CRAWL_LIST.csv")

write.csv(df2, filename, row.names = F)


