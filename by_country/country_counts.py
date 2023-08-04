import csv
import json
import argparse
from collections import defaultdict


def count_records_by_country(file_path, output_file):
    with open(file_path, 'r') as file:
        records = json.load(file)

    country_counts = defaultdict(int)
    code_to_name = {}
    for record in records:
        country_code = record["country"]["country_code"]
        country_counts[country_code] += 1
        if country_code not in code_to_name:
            code_to_name[country_code] = record["country"]["country_name"]

    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["country_code", "country_name", "count"])
        for country_code, count in country_counts.items():
            country_name = code_to_name[country_code]
            csv_writer.writerow([country_code, country_name, count])


def parse_arguments():
    # Create a new ArgumentParser object. The ArgumentParser object will hold all the information necessary to parse the command-line arguments.
    parser = argparse.ArgumentParser(description='Count records by country.')

    # Add a positional argument. 'input_file' is a mandatory argument, hence 'required=True'. The user needs to specify this while running the script.
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to the input JSON file.')

    # Add an optional argument. If 'output_file' is not specified by the user, the default value 'country_counts.csv' will be used.
    parser.add_argument('-o', '--output_file', type=str, default='country_counts.csv', help='Path to the output CSV file.')
    
    # Parse the command-line arguments and return as a Namespace object. 
    # This object holds the values of all arguments that were specified on the command-line.
    return parser.parse_args()

def main():
    # Parse command-line arguments.
    args = parse_arguments()

    # Use parsed command-line arguments to call 'count_records_by_country'.
    # 'args.input_file' and 'args.output_file' are the input and output file paths specified by the user on the command-line.
    count_records_by_country(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
