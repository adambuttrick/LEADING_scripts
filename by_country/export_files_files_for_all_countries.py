import os
import sys
import json

def save_records_by_country_code(country_codes_filepath, data_file_path):
	with open(data_file_path, 'r') as file:
		records = json.load(file)

	#get list of country codes from country_counts.py
	with open(country_codes_filepath, 'r') as country_codes_file:
		country_codes = country_codes_file.read().splitlines()

	for country_code in country_codes:
		filtered_records = [record for record in records if record["country"]["country_code"] == country_code]
		with open(f"{country_code}_records.json", 'w') as output_file:
			json.dump(filtered_records, output_file, indent=2)

if __name__ == '__main__':
	save_records_by_country_code(sys.argv[1], sys.argv[2])
