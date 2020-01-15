import pandas as pd
import mysql.connector
import re
import yaml
import utils
from selenium import webdriver
from datetime import datetime
from time import sleep

with open('config_file.yml') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

cnx = mysql.connector.connect(host=configs['host'],
                              database=configs['database'],
                              user=configs['user'],
                              password=configs['password'])
    
class crawl_trip_advisor:
    def __init__(self, cnx):
        cursor = cnx.cursor()
        self.poi_list = 
        self.reviews = 
        self.driver = webdriver.Chrome('./chromedriver')
    
    def crawl_and_add(self):
        
    
    def crawl_attributes(self):

    
    def crawl_reviews(self):
        
        
    def add_df_reviews(self, reviews):
        
