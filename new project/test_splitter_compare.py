from dotenv import load_dotenv
load_dotenv()

from ingestion.loaders import load_csv_docs
from ingestion.splitters import (
    recursive_split,
    semantic_split
)
docs = load_csv_docs()

recursive_chunks = recursive_split(docs)
semantic_chunks = semantic_split(docs)

print("\n===== SPLITTER COMPARISON =====")

print(f"\n원본 문서 수: {len(docs)}")
print(f"Recursive 청크 수: {len(recursive_chunks)}")
print(f"Semantic 청크 수: {len(semantic_chunks)}")

print("\n===== Recursive Example =====")
print(recursive_chunks[0].page_content[:500])

print("\n===== Semantic Example =====")
print(semantic_chunks[0].page_content[:500])