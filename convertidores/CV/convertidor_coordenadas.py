import json
from scrapper import Scrapper

# Correct initialization of the Scrapper
scrapper_instance = Scrapper()
scrapper_instance.stablish_connection_and_initialize_variables()
scrapper_instance.set_up_site()


#Set up JSON
file = open('data.json')
data = json.load(file)

# change values to the json
for wrapper in data:
   monument = wrapper["Monumento"]
   monument["longitud"], monument["latitud"] = scrapper_instance.process_data(monument["longitud"], monument["latitud"])
   
# Write the result in a json file called 'result.json'
with open ('result.json', 'w') as file: 
   json.dump(data, file, indent=4)
# close the driver 
scrapper_instance.close_driver()

