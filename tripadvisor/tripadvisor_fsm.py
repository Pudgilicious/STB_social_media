from time import sleep
from tripadvisor_crawler import TripAdvisorCrawler

class TripAdvisorFSM:
    def __init__(self, chromedriver_path, poi_df, cnx, db_out_flag):
        self.crawler = TripAdvisorCrawler(chromedriver_path, poi_df, cnx, db_out_flag)

    def start(self, start_page=None, number_of_pages=None, earliest_date=None, trip_types=None):
        crawler = self.crawler
        while crawler.fsm_state != 4:
            crawler.crawl_pois(start_page, number_of_pages, earliest_date, trip_types)
            # Case were old TripAdvisor site is loaded, or any crashes on load (nothing crawled)
            if crawler.fsm_state == 3 and crawler.current_page is None:
                sleep(2)  # 2 second window for keyboard interrupt
                crawler.fsm_state = 2
            # Crashes during crawl
            if crawler.fsm_state == 3 and crawler.current_page is not None:
                sleep(2)  # 2 second window for keyboard interrupt
                url_part_1 = crawler.current_poi_url[:crawler.current_poi_url.find("Reviews")+8]
                url_part_2 = 'or' + str(crawler.current_page - 1) + '0-'
                url_part_3 = crawler.current_poi_url[crawler.current_poi_url.find("Reviews")+8:]
                crawler.current_poi_url = url_part_1 + url_part_2 + url_part_3
                crawler.fsm_state = 2
