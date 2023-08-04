import sys
import json
import sqlite3

def create_sql_database(file_path):

	#load newest version of ror data
	with open(file_path, 'r') as file:
		records = json.load(file)
	
	cxn = sqlite3.connect("ror_data.db")
	cur = cxn.cursor()

	#drop existing table, if it exists, to create a fresh table for ror records
	res = cur.execute("SELECT name FROM sqlite_master WHERE name='ror_records'")
	if res.fetchone() is not None:
		cur.execute("DROP TABLE ror_records")
	cur.execute("CREATE TABLE ror_records(ror_id, inst_type, established, status, city, country)")
	
	#create table for all labels, if it doesn't already exist
	res = cur.execute("SELECT name FROM sqlite_master WHERE name='labels'")
	if res.fetchone() is not None:
		cur.execute("DROP TABLE labels")
	cur.execute("CREATE TABLE labels(label_id, ror_id, label, label_type, lang)")
	
	#create table for external ids, if it doesn't already exist
	res = cur.execute("SELECT name FROM sqlite_master WHERE name='external_ids'")
	if res.fetchone() is not None:
		cur.execute("DROP TABLE external_ids")
	cur.execute("CREATE TABLE external_ids(external_id, ror_id, id_source)")
	
	ror_data = []
	labels = []
	ex_ids = []
	for record in records:
		ror_id = record["id"]
		inst_type = record["types"][0]
		established = record["established"]
		status = record["status"]
		city = record["addresses"][0]["city"]
		country = record["country"]["country_name"]
		#generate data for ror record
		ror_data.append(tuple([ror_id, inst_type, established, status, city, country]))
		
		#generate data for labels
		name = record["name"]
		labels.append(tuple([len(labels), ror_id, name, "name", ""]))
		alias_list = record["aliases"]
		if len(alias_list) > 0:
			for alias in alias_list:
				labels.append(tuple([len(labels), ror_id, alias, "alias", ""]))
		acronym_list = record["acronyms"]
		if len(acronym_list) > 0:
			for acronym in acronym_list:
				labels.append(tuple([len(labels), ror_id, acronym, "acronym", ""]))
		label_list = record["labels"]
		if len(label_list) > 0:
			for label in label_list:
				label_name = label["label"]
				iso = label["iso639"]
				labels.append(tuple([len(labels), ror_id, label_name, "label", iso]))

		#generate data for external ids
		external_id_dict = record["external_ids"]
		if len(external_id_dict) > 0:
			keys = list(external_id_dict.keys())
			for key in keys:
				for identifier in external_id_dict[key]["all"]:
					ex_ids.append(tuple([identifier, ror_id, key]))
	
	#add new data to tables
	cur.executemany("INSERT INTO ror_records VALUES (?, ?, ?, ?, ?, ?)", ror_data)
	cur.executemany("INSERT INTO labels VALUES (?, ?, ?, ?, ?)", labels)
	cur.executemany("INSERT INTO external_ids VALUES (?, ?, ?)", ex_ids)

	cxn.commit()
	cxn.close()

if __name__ == '__main__':
	create_sql_database(sys.argv[1])