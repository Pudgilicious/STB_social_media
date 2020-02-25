#Documentation: How to use Ctrip Cralwer

##default setting:range of crawling
- crawl all reviews of all POIs 

##customize the range of crawling
- open 'config_file_QY.yml', which should be located at the root folder
- to change RANGE OF REVIEWS, change number_of_pages, int or None(default).
- If 0, only Attributes are crawled. If None, all reviews will be crawled

##running the CtripCrawler
- open terminal from the root file 'STB_social_media_analytics'
- type 'python ./qiongyou/QY_crawler.py'

##finished crawling
- A time indicator should appear at the bottom of the current code, stating the total time take for this round of carwling