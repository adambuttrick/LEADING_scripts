import csv
import requests
import json

def get_wikidata_records():
	url = 'https://query.wikidata.org/sparql'
	
	# Define the SPARQL query
	query = """
	SELECT ?item ?itemLabel ?itemLabel_en ?rorID ?hkcanID WHERE {
	  ?item wdt:P6782 ?rorID.
	  # You can sub in any other claim values you want here for other identifiers present in Wikidata
	  ?item wdt:P5909 ?hkcanID.
	  OPTIONAL {?item rdfs:label ?itemLabel filter (lang(?itemLabel) = "zh").}
	  OPTIONAL {?item rdfs:label ?itemLabel_en filter (lang(?itemLabel_en) = "en").}
	  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
	}
	"""
	
	# Set up headers
	headers = {
		'User-Agent': 'Wikidata Script',
		'Accept': 'application/sparql-results+json'
	}
	response = requests.get(url, headers=headers, params={'query': query})

	# Check if the request was successful
	if response.status_code == 200:
		return response.json()
	else:
		raise Exception(f'Request failed with status code {response.status_code}')


def extract_data(json_response):
	records = []
	# Loop through each record in the API response
	for record in json_response['results']['bindings']:
		data = {}
		data['ROR ID'] = record['rorID']['value'] if 'rorID' in record else None
		data['HKCANID'] = record['hkcanID']['value'] if 'hkcanID' in record else None
		data['Chinese Label'] = record['itemLabel']['value'] if 'itemLabel' in record else None
		data['English Label'] = record['itemLabel_en']['value'] if 'itemLabel_en' in record else None
		records.append(data)
		
	return records


def write_to_csv(records, filename):
	headers = ['ROR ID', 'HKCANID', 'Chinese Label', 'English Label']
	with open(filename, 'w', newline='', encoding='utf-8') as f:
		writer = csv.DictWriter(f, fieldnames=headers)
		writer.writeheader()
		for record in records:
			writer.writerow(record)


def main():
	json_response = get_wikidata_records()
	records = extract_data(json_response)
	write_to_csv(records, 'wikidata_ids_w_ror_hkcan.csv')


if __name__ == "__main__":
	main()