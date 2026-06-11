import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import time
import json

from ingestion.loaders import load_csv_docs
from ingestion.splitters import recursive_split

from retrieval.hybrid import build_hybrid_retriever
from chains.rag_chains import ask_rag


docs = load_csv_docs()

chunks = recursive_split(docs)

retriever = build_hybrid_retriever(chunks)

with open("evaluation/testset.json", encoding="utf-8") as f:
    testset = json.load(f)


results = []
times = []

for item in testset:

    start = time.time()

    result = ask_rag(
        item["question"],
        retriever
    )

    end = time.time()

    elapsed = end - start

    times.append(elapsed)

    print(
        f"{item['question']} : {elapsed:.4f}초"
    )

    results.append({
        "question": item["question"],
        "ground_truth": item["ground_truth"],
        "answer": result["answer"],
        "contexts": result["contexts"]
    })
    
    avg_time = sum(times) / len(times)

print("=" * 50)
print(f"평균 응답시간 : {avg_time:.4f}초")

with open(
    "evaluation/hybrid_results.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Hybrid 결과 저장 완료")