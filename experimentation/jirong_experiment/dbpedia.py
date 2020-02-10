# Python
import requests
 
data = requests.get('http://dbpedia.org/data/Matteo_Donati.json').json()
matteo = data['http://dbpedia.org/resource/Matteo_Donati']
 
# matteo is a dictionary with lots of keys
# that correspond to the player's properties.
# Each value is a list of dictionaries itself.
 
height = matteo['http://dbpedia.org/ontology/height'][0]['value']
# 1.88  (float)
birth_year = matteo['http://dbpedia.org/ontology/birthYear'][0]['value']
# '1995'  (string)
hand = matteo['http://dbpedia.org/ontology/plays'][0]['value']
# 'Right-handed (two-handed backhand)'  (string)
singles_rank = matteo['http://dbpedia.org/property/currentsinglesranking'][0]['value']
# 'No. 171'  (string)


for key in sorted(matteo): print(key)