from ingestion.loaders import load_csv_docs
from ingestion.splitters import recursive_split

from retrieval.dense import (
    build_dense_retriever,
    build_mmr_retriever
)

docs = load_csv_docs()

chunks = recursive_split(docs)

query = "Which company invested in Krafton?"

print("\n===================")
print("SIMILARITY SEARCH")
print("===================\n")

dense = build_dense_retriever(chunks)

results = dense.invoke(query)

for i, doc in enumerate(results):
    print(f"\nResult {i+1}")
    print(doc.page_content[:300])


print("\n===================")
print("MMR SEARCH")
print("===================\n")

mmr = build_mmr_retriever(
    chunks,
    lambda_mult=0.5
)

results = mmr.invoke(query)

for i, doc in enumerate(results):
    print(f"\nResult {i+1}")
    print(doc.page_content[:300])