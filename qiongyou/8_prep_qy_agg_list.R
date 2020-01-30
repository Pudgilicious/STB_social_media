#https://help.memsource.com/hc/en-us/articles/115003461051-Google-Translate-API-Key
#https://translatepress.com/docs/automatic-translation/generate-google-api-key/

library(tidyverse)
library(googleLanguageR)
library(textcat)
library(stringi)
library(translateR)
library(yaml)
library(cld2)

df = read_csv("./qiongyou/20200114_qy_list.csv")
keys = read_yaml("./api_keys.yml")

# df$language = detect_language(df$POI)

#If eng_name is NA and POI is english name
df$eng_name_modified = ifelse(is.na(df$eng_name) & df$poi_is_english == 1, df$POI, df$eng_name)
  
google.dataset.out <- translate(dataset = df,
                                content.field = 'POI',
                                google.api.key = keys$General$google_translate_api,
                                source.lang = 'zh-CN',
                                target.lang = 'en')

google.dataset.out$is_translated = ifelse(is.na(google.dataset.out$eng_name_modified), 1, 0)
google.dataset.out$eng_name_modified = ifelse(is.na(google.dataset.out$eng_name_modified), google.dataset.out$translatedContent, google.dataset.out$eng_name_modified)

google.dataset.out$num_reviews = gsub("[^0-9.-]", "", google.dataset.out$num_reviews)
google.dataset.out$WEBSITE_INDEX = 4

#POI_NAME is modified
names(google.dataset.out) = c("POI_INDEX", "POI_CHINESE_NAME", "POI_RAW_NAME", "URL", "TOTAL_REVIEWS", "POI_CHINESE_NAME_IS_ENGLISH", "POI_NAME", "POI_CHINESE_NAME_TRANSLATED", "POI_NAME_IS_TRANSLATED", "WEBSITE_INDEX")

#write out csv
filename = paste0("./qiongyou/",gsub("-","", Sys.Date()), "_TB_SOCIAL_QY_CRAWL_LIST.csv")
write.csv(google.dataset.out, filename, row.names = F)



