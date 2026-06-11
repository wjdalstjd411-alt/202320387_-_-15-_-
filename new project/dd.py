import json

with open("evaluation/dense_results.json", encoding="utf-8") as f:
    data = json.load(f)

print(len(data))