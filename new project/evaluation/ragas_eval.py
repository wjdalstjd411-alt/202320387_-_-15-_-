from dotenv import load_dotenv

load_dotenv()

import json

from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# 평가할 파일 선택
RESULT_FILE = "evaluation/dense_results.json"
# RESULT_FILE = "evaluation/hybrid_results.json"

with open(RESULT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

dataset = Dataset.from_list(data)

result = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

print(result)