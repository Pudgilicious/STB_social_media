#Convert xml to excel https://conversiontools.io/convert/xml-to-excel
#http://metashare.ilsp.gr:8080/repository/browse/semeval-2016-absa-restaurant-reviews-english-train-data-subtask-1/cd28e738562f11e59e2c842b2b6a04d703f9dae461bb4816a5d4320019407d23/
#https://heartbeat.fritz.ai/using-aspect-based-sentiment-analysis-to-understand-user-generated-content-2cfd5d3e25bb

import xml.etree.ElementTree as ET
#import os
#os.getcwd()

# use the parse() function to load and parse an XML file
#parsedXML = et.parse("./experimentation/jirong_experiment/food_reviews/ABSA16_Restaurants_Train_SB1_v2.xml");

tree = ET.parse("./experimentation/jirong_experiment/food_reviews/ABSA16_Restaurants_Train_SB1_v2.xml")
root = tree.getroot()

#Returns review id
for child in root: 
    print(child.tag, child.attrib) #tag is the variable, attrib is the value

#returns sentence id
root[0][0][0].attrib
root[0][0][1].attrib

root[0][0][0][0].attrib

root[0][0][0].tag

tree = ET.parse('./experimentation/jirong_experiment/food_reviews/ABSA16_Restaurants_Train_SB1_v2.xml')
root = tree.getroot()
[elem.tag for elem in root.iter()]

for review in root.iter('Review'):
    print(review.attrib)
    
for review in root.iter('Opinion'):
    print(review.attrib)
    
