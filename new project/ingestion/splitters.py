from dotenv import load_dotenv
load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

def recursive_split(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(docs)

def semantic_split(docs):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    splitter = SemanticChunker(
        embeddings
    )

    return splitter.split_documents(docs)