import json

with open("evaluation/dense_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data[0].keys())
print(data[0])