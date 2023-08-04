import json
import sys

def grab_city_records(city,data_filepath):
	with open(data_filepath,'r') as data_file:
		records = json.load(data_file)
	filtered_records = [record for record in records if record['addresses'][0]['city'] == city]
	with open('{}_city_records.json'.format(city),'w') as city_data_file:
		json.dump(filtered_records, city_data_file, indent=2)

if __name__ == '__main__':
	grab_city_records(sys.argv[1], sys.argv[2])