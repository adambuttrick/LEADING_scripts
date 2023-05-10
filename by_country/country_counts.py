import csv
import sys
import json
from collections import defaultdict

def count_records_by_country(file_path):
	with open(file_path, 'r') as file:
		records = json.load(file)

	country_counts = defaultdict(int)
	for record in records:
		country_code = record["country"]["country_code"]
		country_counts[country_code] += 1

	with open('country_counts.csv', 'w', newline='') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(["country_code", "count"])

		for country_code, count in country_counts.items():
			csv_writer.writerow([country_code, count])

if __name__ == '__main__':
	count_records_by_country(sys.argv[1])
