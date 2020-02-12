#https://help.memsource.com/hc/en-us/articles/115003461051-Google-Translate-API-Key
#https://translatepress.com/docs/automatic-translation/generate-google-api-key/

library(tidyverse)
library(googleLanguageR)
library(textcat)
library(stringi)
library(translateR)
library(yaml)
library(cld2)

df = read_csv("./mafengwo/20200122_mfw_list.csv")
keys = read_yaml("./api_keys.yml")

# df$language = detect_language(df$POI)

#If eng_name is NA and POI is english name
df$eng_name_modified = ifelse(is.na(df$eng_name) & df$poi_is_english == 1, df$cn_names, df$eng_name)

google.dataset.out <- translate(dataset = df,
                                content.field = 'cn_names',
                                google.api.key = keys$General$google_translate_api,
                                source.lang = 'zh-CN',
                                target.lang = 'en')

google.dataset.out$is_translated = ifelse(is.na(google.dataset.out$eng_name_modified), 1, 0)
google.dataset.out$eng_name_modified = ifelse(is.na(google.dataset.out$eng_name_modified), google.dataset.out$translatedContent, google.dataset.out$eng_name_modified)

google.dataset.out$num_reviews = gsub("[^0-9.-]", "", google.dataset.out$num_reviews)
google.dataset.out$WEBSITE_INDEX = 3
google.dataset.out = google.dataset.out[, -1]

#POI_NAME is modified
names(google.dataset.out) = c("POI_INDEX", "URL", "POI_RAW_NAME", "POI_CHINESE_NAME", "TOTAL_REVIEWS", "POI_CHINESE_NAME_IS_ENGLISH", "POI_NAME", "POI_CHINESE_NAME_TRANSLATED", "POI_NAME_IS_TRANSLATED", "WEBSITE_INDEX")

#write out csv
filename = paste0("./mafengwo/",gsub("-","", Sys.Date()), "_TB_SOCIAL_MFW_CRAWL_LIST.csv")
write.csv(google.dataset.out, filename, row.names = F)



