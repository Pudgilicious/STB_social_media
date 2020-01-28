import time
from tripadvisor_crawler_v2 import TripAdvisorCrawler

class TripAdvisorFSM:
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.crawler = TripAdvisorCrawler(chromedriver_path, poi_df, cnx, db_out_flag)
        self.start_time = time.time()
        self.end_time = time.time()

    def start(self):
        crawler = self.crawler
        while crawler.fsm_state != 4:
            crawler.crawl_pois()
            # Case were TripA load old site or crash on load (nothing crawled)
            if crawler.fsm_state == 3 and crawler.current_page is None:
                crawler.fsm_state = 2
            # Crashes during crawling process
            if crawler.fsm_state == 3 and crawler.current_page is not None:
                url_part_1 = crawler.current_poi_url[:crawler.current_poi_url.find("Reviews")+8]
                url_part_2 = 'or' + str((crawler.current_page - 1)*10) + '-'
                url_part_3 = crawler.current_poi_url[crawler.current_poi_url.find("Reviews")+8:]
                crawler.current_poi_url = url_part_1 + url_part_2 + url_part_3
                crawler.fsm_state = 2
