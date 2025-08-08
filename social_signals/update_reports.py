# Run this every week, whereupon this file
# will iterate over all entries in a master.csv of cumulative
# data, compute what is wanted, and then write over the json
# files in /reports


import csv
import datetime
import secrets
import glob
import os
import json

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


reports = {}
for profile in profiles:
    print(profile)
    date = datetime.date.fromisoformat(profile["creation_date"])
    if (today - date).days < 7:
        #report not ready
        reports[profile["dynata_id"]] = {"report_ready": False, "ready_date": (date + datetime.timedelta(days=7)).strftime("%B %-d")}
    else:
        week_range = (today - datetime.timedelta(days=7)).strftime("%B %-d") + " - " + today.strftime("%B %-d")
        reports[profile["dynata_id"]] = {"report_ready": True, "city": profile["city"], "week_range": week_range,
                                         "followup_start": "hello", "followup_end": "goodbye", "total_listings": 205,
                                         "contacted": 25, "responses": 3, "avg_rent": 1420, "private_bathroom_pct": 68,
                                         "below_r_pct": 45, "above_r_pct": 55,}


for listing in craigslist_data:
    date_string = listing["date"].split('T')[0]
    date = datetime.date.fromisoformat(date_string)
    
    if (today - date).days > 7:
        print("entry outdated, won't use")
        continue



#delete all stale reports as well as map
json_files = glob.glob(os.path.join('reports/', '*.json'))
for file_path in json_files:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")


id_to_token = {}
for dynata_id, report in reports.items():
    token = secrets.token_urlsafe(16)
    id_to_token[dynata_id] = token
    with open(f"reports/{token}.json", mode='w') as report_file:
        report_file.write(json.dumps(report))



with open("reports/id_to_token.json", mode='w') as map_file:
    map_file.write(json.dumps(id_to_token))
