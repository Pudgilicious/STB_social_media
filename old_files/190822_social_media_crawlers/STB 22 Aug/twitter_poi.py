#For every poi coordinate search for 20 tweets

import twint
import pandas as pd

c = twint.Config()  #define an object here

# Read in the POI file
file = pd.read_csv('trip_poi_xy.csv', index_col=[0])
xy_list = file['coordinates']

# The radius you want to search
r = '0.1km'

for xy in xy_list:
    c.Geo = xy.replace(' ', '') + ',' + r
    c.Store_csv = True
    c.Limit = 20      #this is to limit the number of tweets
    c.Output = 'tweets_by_poi.csv'
    twint.run.Search(c)
    print('Done 1.')
