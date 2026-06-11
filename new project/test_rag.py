from ingestion.loaders import load_csv_docs
from ingestion.splitters import recursive_split

from retrieval.dense import build_dense_retriever
from chains.rag_chains import ask_rag


docs = load_csv_docs()

chunks = recursive_split(docs)

retriever = build_dense_retriever(chunks)

result = ask_rag(
    "Samsung Electronics CEO는 누구인가?",
    retriever
)

print("\n답변:")
print(result["answer"])