import pandas as pd
import mysql.connector
import yaml
import utils
from selenium import webdriver
from datetime import datetime
from time import sleep

cnx = mysql.connector.connect(host='localhost',
                              database='sentimentDB',
                              user='test_user',
                              password='Password123!')
    
class crawl_trip_advisor:
    def __init__(self, cnx):
        cursor = cnx.cursor()
        self.poi_list = 
        self.reviews = 
    
    def crawl_and_add(self):
    
    
    def crawl_attributes(self):
     
    
    def crawl_reviews(self):
        
        
    def add_df_reviews(self, reviews):
        
