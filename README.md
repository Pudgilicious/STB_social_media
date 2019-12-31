# Documentation

Linux version of Chromedriver for Chrome version 78.0.3904.108 used (included).

poi.csv currently only contains 100 POIs for testing purposes. Pending updates.

Create MySQL database with the UTF8mb4 encoding, e.g.:  
`CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`

Run .sql files to create the respective MySQL tables (currently the tables `instagram` and `tweets`).

Crawler environment and/or setup described in set_up_crawler_environment.txt.

The following in instagram_twitter_crawler.py found under the functions crawl_twitter() and craw_instagram() should be amended accordingly.  
`host='localhost',`  
`database='sentimentDB',`  
`user='test_user',`  
`password='Password123!'`

Run the following to start crawling from twitter:  
`python -c 'import crawler; crawler.crawl_twitter()'`  

Run the following to start crawling from instagram:  
`python -c 'import crawler; crawler.crawl_instagram()'`
