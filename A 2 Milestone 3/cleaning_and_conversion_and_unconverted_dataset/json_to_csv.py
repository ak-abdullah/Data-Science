import json
import csv

# Load JSON data
with open('dba.dk data set.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write to CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    if isinstance(data, list):
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    else:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
