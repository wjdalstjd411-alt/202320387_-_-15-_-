import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

try:
    from langchain_chroma import Chroma
except:
    from langchain_community.vectorstores import Chroma

load_dotenv()


def build_vectorstore(chunks):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    return vectorstore


def build_dense_retriever(chunks):

    vectorstore = build_vectorstore(chunks)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever


def build_mmr_retriever(chunks, lambda_mult=0.5):

    vectorstore = build_vectorstore(chunks)

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20,
            "lambda_mult": lambda_mult
        }
    )

    return retriever