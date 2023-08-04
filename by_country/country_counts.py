import csv
import sys
import json
from collections import defaultdict

def count_records_by_country(file_path):
	with open(file_path, 'r') as file:
		records = json.load(file)

	country_counts = defaultdict(int)
	code_to_name = {}
	for record in records:
		country_code = record["country"]["country_code"]
		country_counts[country_code] += 1
		if country_code not in code_to_name:
			code_to_name[country_code] = record["country"]["country_name"]

	with open('country_counts.csv', 'w', newline='') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(["country_code", "country_name", "count"])
		for country_code, count in country_counts.items():
			country_name = code_to_name[country_code]
			csv_writer.writerow([country_code, country_name, count])

if __name__ == '__main__':
	count_records_by_country(sys.argv[1])
