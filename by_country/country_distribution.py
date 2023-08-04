import sys
import json
import csv

def get_distribution_by_country(data_filepath):
	with open(data_filepath, 'r') as file:
		records = json.load(file)

	with open('labels_by_country.csv','w', newline='') as outfile:
		csv_writer = csv.writer(outfile)
		csv_writer.writerow([
			"ror_id",
			"name",
			"alias_count",
			"label_count",
			"acronym_count"
			])
		for record in records:
			ror_id = record["id"]
			name = record["name"]
			alias_count = len(record["aliases"])
			label_count = len(record["labels"])
			acronym_count = len(record["acronyms"])
			csv_writer.writerow([ror_id,name,alias_count,label_count,acronym_count])			

if __name__ == '__main__':
	get_distribution_by_country(sys.argv[1])