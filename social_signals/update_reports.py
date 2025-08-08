# Run this every week, whereupon this file
# will iterate over all entries in a master.csv of cumulative
# data, compute what is wanted, and then write over the json
# files in /reports


import csv

FILE_PATH = "data/craigslist_data.csv"

def read_csv_to_dict_list(file_path):
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


for listing in read_csv_to_dict_list(FILE_PATH):
    print(listing)
