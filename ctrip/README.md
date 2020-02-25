#Documentation: How to use Ctrip Cralwer

##default setting:range of crawling
- crawl ALL reviews of PRIORITIZED POIs (518 POIs with reviews)
- using local IP address, auto switch to proxy when meet authentication
- number of reloading when loading error or lag happens: 3

##customize the range of crawling
- open 'config_file_Ctrip.yml', which should be located at the root folder
- to change RANGE OF REVIEWS, change number_of_pages, int or None(default).
- If 0, only Attributes are crawled. If None, all reviews will be crawled
- to change PROXY SETTING, change proxy_mode,1:local only, 2: local->proxy(default); 3: proxy only
- to change PRIORITY SETTING of crawling, change prioritize, True for crawl prioritized POIs only, False for crawl all
- to change priority of particular POIs, please go to the file stated in csv_input_path
- under column 'IS_PRIORITIZED', 1 for priotizing the POI, 0 for not prioritized


##running the CtripCrawler
- open terminal from the root file 'STB_social_media_analytics'
- type 'python ./ctrip/Ctrip_crawler.py'

##finished crawling
- A time indicator should appear at the bottom of the current code, stating the total time take for this round of carwling