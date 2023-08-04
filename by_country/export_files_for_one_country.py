import os
import sys
import json

def save_records_by_country_code(country_code, file_path):
	if not os.path.exists(country_code):
		os.makedirs(country_code)

	with open(file_path, 'r') as file:
		records = json.load(file)

	filtered_records = [record for record in records if record["country"]["country_code"] == country_code]
	
	with open(f"{country_code}/records_{country_code}.json", 'w') as output_file:
		json.dump(filtered_records, output_file, indent=2)

if __name__ == '__main__':
	save_records_by_country_code(sys.argv[1], sys.argv[2])
