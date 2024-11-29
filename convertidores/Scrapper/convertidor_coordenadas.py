import json
import sys
from scrapper import Scrapper

# Correct initialization of the Scrapper
scrapper_instance = Scrapper()
scrapper_instance.stablish_connection_and_initialize_variables()
scrapper_instance.set_up_site()


#Set up JSON
file = open(sys.argv[1])
data = json.load(file)


for wrapper in data:
   monument = wrapper["Monumento"]
   monument["longitud"], monument["latitud"] = scrapper_instance.process_data(monument["longitud"], monument["latitud"])

with open('data/result.json','w') as f:
   json.dump(data,f,indent=4)
scrapper_instance.close_driver()

