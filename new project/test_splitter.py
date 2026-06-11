from ingestion.loaders import load_csv_docs
from ingestion.splitters import recursive_split

docs = load_csv_docs()

chunks = recursive_split(docs)

print(f"원본 문서 수: {len(docs)}")
print(f"청크 수: {len(chunks)}")

print()
print(chunks[0].page_content)
