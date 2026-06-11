import json

with open(
    "evaluation/hybrid_results.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

print(data[0])