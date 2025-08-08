# Run this every week, whereupon this file
# will iterate over all entries in a master.csv of cumulative
# data, compute what is wanted, and then write over the json
# files in /reports


import csv
import datetime
today = datetime.date.today()

CRAIGSLIST_DATA_FILE_PATH = "data/craigslist_data.csv"
PROFILES_FILE_PATH = "data/profiles.csv"
def read_csv_to_dict_list(file_path):
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

profiles = read_csv_to_dict_list(PROFILES_FILE_PATH)
craigslist_data = read_csv_to_dict_list(CRAIGSLIST_DATA_FILE_PATH)

test = craigslist_data[0]
date_string = test["date"].split('T')[0]
date = datetime.date.fromisoformat(date_string)

print(today)
print(date)
print((today - date).days)
'''
for listing in craigslist_data:
    date_string = listing["date"].split('T')[0]

    date = datetime.date.fromiso(date_string)

    print
'''
