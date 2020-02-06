library(tidyverse)
library(googleLanguageR)
library(textcat)
library(stringi)
library(translateR)
library(yaml)
library(cld2)


data = read.csv("./ctrip/20200204_Ctrip_shopping_list.csv", stringsAsFactors = F)
data$address = trimws(data$address)

keys = read_yaml("./api_keys.yml")

# df$language = detect_language(df$POI)

google.dataset.out <- translate(dataset = data,
                                content.field = 'POI',
                                google.api.key = keys$General$google_translate_api,
                                source.lang = 'zh-TW',
                                target.lang = 'zh-CN')



write.csv2(google.dataset.out, "./ctrip/20200204_Ctrip_shopping_list_semicolon_delimit.csv", row.names = F)