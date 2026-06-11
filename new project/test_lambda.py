from ingestion.loaders import load_csv_docs
from ingestion.splitters import recursive_split

from retrieval.dense import build_mmr_retriever

docs = load_csv_docs()

chunks = recursive_split(docs)

query = "Which company invested in Krafton?"

for lam in [0.1, 0.5, 0.9]:

    print("\n")
    print("=" * 60)
    print(f"lambda_mult = {lam}")
    print("=" * 60)

    retriever = build_mmr_retriever(
        chunks,
        lambda_mult=lam
    )

    results = retriever.invoke(query)

    for i, doc in enumerate(results[:3]):
        print(f"\nResult {i+1}")
        print(doc.page_content[:200])