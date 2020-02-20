#Extract datasets for Susanne

setwd("C:/Users/huangj/Desktop/items/Styles and climate verbatim research/raw_dat")
dat = read.csv("20170129_include_language_ALLCommentsSC2.csv",stringsAsFactors = F)

# > table(dat$language)
# 
# afrikaans            albanian              basque             bosnian              breton             catalan      croatian-ascii     czech-iso8859_2              danish 
# 312                  13                 547                 117                 404                2863                 110                1607                1198 
# dutch             english           esperanto            estonian             finnish              french             frisian              german     greek-iso8859-7 
# 14405              127266                 219                 111                1059                4718                 291               10362                  12 
# hebrew-iso8859_8           hungarian           icelandic          indonesian               irish             italian               latin             latvian          lithuanian 
# 8                 127                  18                 482                 108               12372                 640                  17                  86 
# malay                manx      middle_frisian              nepali           norwegian              polish          portuguese            romanian           rumantsch 
# 792                 137                 930                3663                 617               12973               14244                1719                 514 
# russian-iso8859_5 russian-windows1251            sanskrit               scots        scots_gaelic       serbian-ascii        slovak-ascii  slovak-windows1250     slovenian-ascii 
# 1166                  12                 236                1471               64201                 126                 872                1530                 127 
# slovenian-iso8859_2             spanish             swahili             swedish             tagalog             turkish    ukrainian-koi8_r               welsh 
# 1653               14824                 422                 671                 205                1856                  33                 224
#danish, swedish, norwegian


dat = subset(dat,dat$language == "swedish"|
               dat$language == "norwegian"|
               dat$language == "danish")


write.csv(dat,"20180130_dat_swedish_norw_dan.csv", row.names = F)
