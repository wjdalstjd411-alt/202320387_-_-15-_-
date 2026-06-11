from langchain_classic.retrievers import EnsembleRetriever

from retrieval.dense import build_dense_retriever
from retrieval.sparse import build_sparse_retriever


def build_hybrid_retriever(chunks):

    dense = build_dense_retriever(chunks)
    sparse = build_sparse_retriever(chunks)

    hybrid = EnsembleRetriever(
        retrievers=[dense, sparse],
        weights=[0.7, 0.3]
    )

    return hybrid