from langchain_community.retrievers import BM25Retriever


def build_sparse_retriever(chunks):

    retriever = BM25Retriever.from_documents(chunks)

    retriever.k = 5

    return retriever