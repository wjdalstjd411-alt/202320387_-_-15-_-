from ingestion.loaders import load_csv_docs

docs = load_csv_docs()

print("\n========== 샘플 ==========\n")

for i in range(min(5, len(docs))):
    print(docs[i].page_content[:300])
    print()