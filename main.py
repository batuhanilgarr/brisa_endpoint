import csv
import json

csv_file = "UBY.TyreListFriendlyPath.csv"
json_file = "UBY.TyreListFriendlyPath.json"

data = []

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("data.json oluşturuldu")
