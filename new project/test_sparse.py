from ingestion.loaders import load_csv_docs
from ingestion.splitters import recursive_split

from retrieval.sparse import build_sparse_retriever


docs = load_csv_docs()

chunks = recursive_split(docs)

retriever = build_sparse_retriever(chunks)

query = "Which company invested in Krafton?"

results = retriever.invoke(query)

for i, doc in enumerate(results):

    print("=" * 50)

    print(f"Result {i+1}")

    print(doc.page_content[:500])