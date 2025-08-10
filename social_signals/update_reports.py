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

ready_ids = set()
reports = {}
for profile in profiles:
    date = datetime.date.fromisoformat(profile["creation_date"])
    if (today - date).days < 7:
        #report not ready
        reports[profile["dynata_id"]] = {"report_ready": False, "ready_date": (date + datetime.timedelta(days=7)).strftime("%B %-d")}
    else:
        ready_ids.add(profile["dynata_id"])
        week_range = (today - datetime.timedelta(days=7)).strftime("%B %-d") + " - " + today.strftime("%B %-d")
        reports[profile["dynata_id"]] = {"report_ready": True, "city": profile["city"], "week_range": week_range,
                                         "followup_start": "hello", "followup_end": "goodbye", "total_listings": 0,
                                         "contacted": 0, "responses": 0, "avg_rent": 0, "private_bathroom_pct": 0,
                                         "below_r_pct": 0, "above_r_pct": 0, "rents": []}

total = 0
for listing in craigslist_data:
    date_string = listing["date"].split('T')[0]
    date = datetime.date.fromisoformat(date_string)
    
    if (today - date).days > 7:
        print("entry outdated, won't use")
        continue

    total += 1
    if listing["dynata_id1"] in ready_ids:
        reports[listing["dynata_id1"]]["rents"].append(listing["price"])
        if listing["response1"] == "yes":
            reports[listing["dynata_id1"]]["responses"] += 1
        reports[listing["dynata_id1"]]
    if listing["dynata_id2"] in ready_ids:
        reports[listing["dynata_id2"]]["rents"].append(listing["price"])
        if listing["response2"] == "yes":
            reports[listing["dynata_id2"]]["responses"] += 1


for ready_id in ready_ids:
    person = reports[ready_id]
    person["total_listings"] = total
    person["contacted"] = len(person["rents"])

    if len(person["rents"]) == 0:
        continue

    person["avg_rent"] = int(sum([int(x) for x in person["rents"]]) / len(person["rents"]))
    person["below_r_pct"] = int((len(list(filter(lambda rent: int(rent) < person["avg_rent"], person["rents"]))) / len(person["rents"])) * 100)
    person["above_r_pct"] = int(100 - person["below_r_pct"])

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
        print(f'Writing: reports/{token}.json')
        report_file.write(json.dumps(report))



with open("reports/id_to_token.json", mode='w') as map_file:
    map_file.write(json.dumps(id_to_token))
    print(f'Writing: reports/id_to_token.json')
